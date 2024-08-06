#! /usr/bin/env python3

r"""TeamTalk configuration file converter

Usage:
ttconv (without arguments) to migrate servers from Classic to Qt.
This mode prompts for all required information and pauses before exiting to allow all messages to be read.

ttconv -h or --help
Prints this information and exits (without pausing). See also the ttconv.htm user guide.

ttconv [-a|-u] srcfile [srcfile...] destfile
Takes one or more sources of TeamTalk host entries and writes or appends them into a destination file.
Warning: -a, -u, and multiple sources for one destination are not tested and may not be supported yet.

Tested uses of this utility:
* Conversion of TeamTalk Classic .xml files into TeamTalk Qt .ini files.
* Updating of non-primary Qt client profile server listss from the main configuration.
* Creation of .tt and .htm files from .ini or .xml files.
* Filling the Server Entries section of a TeamTalk Qt .ini file from an HTML file.

Supported file specifications, where "read" means usable as a source and "write" means usable as a destination:
filename.ini or just .ini (read/write): .ini file for MacOS and Windows QT (non-classic) TeamTalk clients.
   Add :l to use the latest-hosts section instead of the host list section.
   .ini.1, .ini.2, etc. also work; these are non-primary profiles.
filename.xml or just .xml (read only): .xml file for Windows classic TeamTalk client.
   Add :l to use the latest-hosts section instead of the host list section.
   .xml.1, .xml.2, etc. also work; these are non-primary profiles.
folder/.tt (write only): One .tt file for each host.
   Append :version to specify a version number; e.g., tt_folder/.tt:5.1.
filename.htm or filename.html (read/write): An HTML file containing a launch link for each host.

Note that extensions without filenames mean use the appropriate file from the installed TeamTalk instance.

Examples:
Copy installed TeamTalk Classic servers to the QT client on the same machine: ttconv .xml .ini
Make tt.htm from the installed TeamTalk Qt .ini file: ttconv .ini c:/Dropbox/tt.htm
Update secondary profile server list from main: ttconv .ini .ini.1
Make .tt files for every server in TeamTalk classic and put them in C:\tt: ttconv .xml c:/tt/.tt

Author: Doug Lee
Copyright 2013-2024 Doug Lee
License: GNU Affero General Public License (AGPL) v3; see copying.txt and http://gnu.org/licenses
iniparse, included in its entirety, comes with its own license (also included).
"""

import os, sys, re
from xml.dom import minidom
from iniparse import INIConfig
from iniparse.config import Undefined
from collections import OrderedDict
from urllib.parse import urlencode, quote, urlparse, parse_qs
from mplib.conpause import pauseAndExit, confirm, input

def machineType():
	"""Returns "mac", "linux, windows," or sys.platform."""
	plat = sys.platform.lower()
	if plat[:3] in ["mac", "dar"]:
		return "mac"
	elif "linux" in plat:  # e.g., linux2
		# Users must set APPDATA in WSL for this to work.
		if os.environ.get("APPDATA"):
			return "windows"
		return "linux"
	elif "win" in plat:  # windows, win32, cygwin
		return "windows"
	return plat

_confpath = ""
def confpath():
	"""The path to this machine's TeamTalk configuration file(s), if known.
	This value is calculated once and cached thereafter.
	Raises a ValueError on failure to determine the path.
	"""
	global _confpath
	if _confpath: return _confpath
	confpath = None
	mtype = machineType()
	if mtype == "windows":
		confpath = os.environ["APPDATA"]
		confpath = os.path.join(confpath, "BearWare.dk")
	else:
		confpath = os.environ["HOME"]
		confpath = os.path.join(confpath, ".config", "BearWare.dk")
	if not confpath or not os.path.exists(confpath):
		raise ValueError("TeamTalk configuration path required but not known.")
	_confpath = confpath
	return confpath

class TTHost:
	"""A single TeamTalk server configuration entry, independent of its file origin.
	Each object in this class must have a unique shortname.
	Attributes in this class are named after their counterparts in the .ini format:
	name, hostaddr, tcpport, udpport, srvpassword, username, password, channel, chanpassword, encrypted.
	In the TT classic XML format, hostaddr is address and chanpassword is cpassword.
	shortname is added but is usually equal to name here.
	iniIndex is the numeric prefix for the entry's fields in the ini format.
	"""
	def __init__(self, shortname, *args, **kwargs):
		#print(f"Creating {shortname} from {kwargs}")
		self.name = kwargs["name"]
		self.hostaddr = kwargs["hostaddr"]
		self.tcpport = int(kwargs.get("tcpport") or 0)
		self.udpport = int(kwargs.get("udpport") or self.tcpport)
		# This is obsolete in TeamTalk5 and comes from TeamTalk4.
		self.srvpassword = kwargs.get("srvpassword") or ""
		self.username = kwargs.get("username") or ""
		self.password = kwargs.get("password") or ""
		self.channel = kwargs.get("channel") or ""
		self.chanpassword = kwargs.get("chanpassword") or ""
		self.encrypted = kwargs.get("encrypted") or ""
		self.shortname = shortname
		if not self.shortname: self.shortname = self.name
		if not self.shortname:
			# The first part of this strategy is used by at least TeamTalk5Classic for Windows to construct server names.
			self.shortname = "{0}:{1:d}".format(self.hostaddr, self.tcpport)
			if self.username: self.shortname = "{0}@{1}".format(self.username, self.shortname)
			# But this part is my own addition. [DGL, 2018-12-30]
			if self.channel: self.shortname += self.channel

	@property
	def url(self):
		"""This host's launch URL based on its properties.
		"""
		# Build the link for this host as a list of parts, then convert to a string when done collecting parts.
		# The 'ascii' byte encoding is recommended by Python docs.
		lnk = []
		if self.tcpport and self.tcpport != 10333: lnk.append(("tcpport", self.tcpport),)
		if self.udpport and (self.tcpport != 10333 or self.udpport != 10333): lnk.append(("udpport", self.udpport),)
		if self.username: lnk.append(("username", self.username),)
		if self.password: lnk.append(("password", self.password),)
		if self.channel: lnk.append(("channel", self.channel),)
		if self.chanpassword: lnk.append(("chanpasswd", self.chanpassword),)
		if self.encrypted: lnk.append(("encrypted", self.encrypted),)
		if lnk: lnk = urlencode(lnk, quote_via=quote, safe='/')
		url = "tt://" +self.hostaddr
		if lnk: url = "?".join([url, lnk])
		return url

	@staticmethod
	def id(d):
		"""Calculated id for a server, meant to uniquely identify it.
		This is similar but not identical to the URL for this server.
		Note that the channel is included here if not empty,
		whereas TeamTalk itself omits this when producing default server entry names.
		d should be a dict or orderedDict or TTHost object.
		"""
		user = f'{d["username"]}@' if d["username"] else ""
		id = f'{user}{d["hostaddr"]}:{d["tcpport"]}{d["channel"]}'
		return id

	def __hash__(self):
		"""For sets.
		"""
		return hash(self.shortname.lower())

	def __eq__(self, other):
		"""Implements ==.
		"""
		return self.shortname == other.shortname

	def __ne__(self, other):
		"""Makes comparison for equality work reasonably.
		"""
		return not self.__eq__(other)

	@property
	def sortKey(self):
		"""Return the sorting key for this host.
		"""
		k = self.shortname.lower()
		# Disabled because this next trick is very me-specific, for handling names like 1simon for secondary servers by one person. [DGL, 2020-04-27]
		#if k[0].isdigit() and not k[1].isdigit(): k = k[1:] +k[0]
		return k

class TTHosts(OrderedDict):
	"""A collection of Hosts. This collection may be built up from one or more file origins and/or merges from other TTHosts instances.
	"""
	def __init__(self, *args, **kwargs):
		super(TTHosts, self).__init__(*args, **kwargs)

	def read(self, src, mode="af"):
		"""Read one file into the existing set of hosts.
		See the updateHosts method for a description of mode.
		"""
		handler = TTFile.getFileHandler(src)
		if not handler.canRead: raise ValueError("{0}: Reading not supported".format(src))
		hosts = handler.read()
		self.updateHosts(hosts, mode)

	def write(self, dest):
		"""Write a file from this set of hosts.
		"""
		handler = TTFile.getFileHandler(dest)
		if not handler.canWrite: raise ValueError("{0}: Writing not supported".format(dest))
		handler.write(self)

	def updateHosts(self, tthosts, mode):
		"""Update this set of hosts from another TTHosts object.
		mode: Any non-null combination of these:
			a: Add hosts from the new set that are not already present.
			d: Delete hosts already present but not found in the new set.
			f: Freshen existing hosts by updating them from the new set.
		"""
		if not mode or mode.replace("a","").replace("d","").replace("f",""):
			raise ValueError('Invalid updateHosts update mode: "' +mode +'"')
		curlen = len(self)
		newlen = len(tthosts)
		if not newlen:
			# Efficiency shortcuts for null tthosts.
			if "d" in mode: self.clear()
			return
		flags = set(mode)
		if ("a" in flags and "f" in flags) or ("a" in flags and not curlen):
			# Shortcuts for Replace and Python-style Update operation cases:
			# af means refresh and add, which is Python update().
			# Adding d makes this a Replace, which is a clear and then an update.
			if "d" in flags: self.clear()
			self.update(tthosts)
			return
		# Brute force approaches for whatever was not optimized already.
		if "d" in flags:
			for k in list(self.keys()):
				if k not in tthosts: del self[k]
		if "a" in flags:
			for k in list(tthosts.keys()):
				if k not in self: self[k] = tthosts[k]
		if "f" in flags:
			for k in list(tthosts.keys()):
				if k in self: self[k] = tthosts[k]

	def add(self, other):
		"""Add a single host to this set.
		"""
		if not isinstance(other, TTHost): other = TTHost("", **other)
		self[other.shortname] = other

class TTFile:
	"""Information for one TeamTalk file to access (read or write).
	Creating an instance of this class actually returns a subclass based on the spec given, for the appropriate type of file.
	"""
	def __init__(self, spec, useLatest):
		"""This runs for each TTFile subclass instance created.
		"""
		self.spec = spec
		self.useLatest = useLatest
		# type is set by each subclass directly, not even in __init__.
		# subclass __init__ methods must set path and then call super to set exists and basename.
		# Note that this method assumes that .tt is the only type for which the spec is a folder rather than a file.
		self.exists = os.path.exists(self.path)
		if self.type == "tt":
			# The only type that uses a folder instead of a file.
			if self.exists and not os.path.isdir(self.path):
				raise ValueError("{0} is not a folder".format(self.path))
			self.basename = ""
		else:
			if self.exists and not os.path.isfile(self.path):
				raise ValueError("{0} is not a file".format(self.path))
			self.basename = os.path.basename(self.path)

	@property
	def canRead(self):
		"""True if this file handler supports reading.
		"""
		return hasattr(self, "read")

	@property
	def canWrite(self):
		"""True if this file handler supports writing.
		"""
		return hasattr(self, "write")

	@staticmethod
	def getFileHandler(spec):
		"""Create and return an appropriate subclass instance, initialized, for the given spec, based on its file type.
		To add a supported file type, update this method and add a subclass for it.
		# Note also though that this class's __init__ method assumes that .tt is the only type for which the spec is a folder rather than a file.
		Each subclass must inherit from this class (TTFile) and accept two __init__ parameters: spec (with any ":l" trailer removed), and useLatest (boolean).
		Note that the optional trailing ":l" part of specs are handled and removed here before the spec is passed on to a subclass.
		Subclasses may raise an error if useLatest is True and the file format does not support the idea.
		"""
		spec0 = spec
		useLatest = False
		if spec.endswith(":l"):
			useLatest = True
			spec = spec[:-2]
		# The following code defines the spec-to-subclass mapping.
		base = os.path.basename(spec).lower()
		if base.endswith(".htm") or base.endswith(".html"):
			return TTFileHTML(spec, useLatest)
		elif base.endswith(".tt") or ".tt:" in base:
			return TTFileTT(spec, useLatest)
		if re.search(r'\.\d+$', base):
			# This allows profiles ending with .1, .2, etc. to be classified based on the original file type.
			base = base.rsplit(".", 1)[0]
		if base.endswith(".ini"):
			return TTFileIni(spec, useLatest)
		elif base.endswith(".xml"):
			return TTFileXML(spec, useLatest)
		else: raise ValueError("{0}: Unrecognized file type".format(spec))

class TTFileHTML(TTFile):
	"""Handler for one HTML file of TT links.
	spec must be a full absolute or relative path to a file.
	useLatest is not supported and will raise an error if True..
	"""
	type = "html"
	def __init__(self, spec, useLatest):
		if useLatest: raise ValueError('{0}: There is no "latest" section in an HTML file'.format(spec))
		self.path = spec
		super(TTFileHTML, self).__init__(spec, useLatest)

	def read(self):
		"""Read one HTML file and return the results as a TTHosts structure.
		Note that this uses all tt://... links regardless of context and uses their text as names.
		"""
		hosts = TTHosts()
		with open(self.path) as f: txt = f.read()
		links = re.findall(r'(?i)<a\s+href="tt://.*?</a>', txt)
		for link in links:
			link = link.split('"', 1)[1]
			url,link = link.split('"', 1)
			d = {}
			d["url"] = url
			link = link.split(">", 1)[1]
			name = link.split("<", 1)[0]
			d["name"] = name
			u = urlparse(url)
			d["hostaddr"] = u.hostname
			q = parse_qs(u.query)
			q.setdefault("tcpport", "10333")
			q.setdefault("udpport", "10333")
			for k,v in q.items():
				if isinstance(v, list):
					if len(v) > 1: raise ValueError("More than one "+k)
					v = v[0]
				if k == "chanpasswd": k = "chanpassword"
				d[k] = v
			hosts.add(d)
		return hosts

	def write(self, hosts):
		"""Write out this HTML file from the given set of hosts. This is a full file create or replace operation.
		"""
		ttl = "TeamTalk Server Links"
		links = []
		for host in sorted(hosts.values(), key=lambda h: h.sortKey):
			name = host.shortname
			lnk = '<a href="' +host.url +'">' +name +'</a>'
			links.append(lnk)
		with open(self.path, "w", encoding="utf-8") as f:
			f.write(
"""<!DOCTYPE HTML>
<html><head>
<title>
""" +ttl +"""
</title>
</head><body>
<h1>""" +ttl +"""</h1>
""" +"\n".join([lnk+"<br/>" for lnk in links]) +"""
</body></html>
""")

class TTFileIni(TTFile):
	"""Handler for one .ini file of TT links.
	These come from TeamTalk for MacOS, Linux, etc., and TeamTalk QT (non-classic) for Windows.
	spec may be a full or relative path to a file or just".ini" to construct the path from standard folder and file name for this type and OS.
	.ini.1, .ini.2, etc., also work for non-primary profiles.
	useLatest determines which section in the file to use.
	"""
	type = "ini"
	def __init__(self, spec, useLatest):
		base = os.path.basename(spec).lower()
		if base == ".ini" or re.match(r'\.ini\.\d+$', base):
			self.path = "TeamTalk5" + base
			self.path = os.path.join(confpath(), self.path)
		else: self.path = spec
		self.useLatest = useLatest
		self.sect = "serverentries"
		if useLatest: self.sect = "latesthosts"
		super(TTFileIni, self).__init__(spec, useLatest)

	def read(self):
		"""Return a TTHosts collection from this ini file.
		"""
		# There are two sections of interest in this file format: latesthosts and serverentries.
		# latesthosts entries have no name field whereas serverentries entries do.
		# Format of both: <idx>_<key>=<val>. <idx> starts at 0 and counts up.
		# <key>: name (serverentries only), hostaddr, tcpport, etc.
		data = {}
		# First collect all k/v pairs into config parameter sets by index.
		with open(self.path, encoding="utf-8") as f: ini = INIConfig(f)
		isect = ini[self.sect]
		# This happens if the user did not make any of one of the two entry types.
		if isinstance(isect, Undefined): return TTHosts()
		curIdx = "-1"
		d = None
		for k in sorted(isect):
			v = isect[k]
			idx,k = k.split("_", 1)
			if idx != curIdx:
				d = OrderedDict()
				data[idx] = d
				d["iniIndex"] = idx
				curIdx = idx
			if k in d:
				raise ValueError(f"Duplicate key {k} at index {idx}")
			d[k] = v
		if max([int(idx) for idx in list(data.keys())]) != len(data) - 1:
			print("Warning: Gaps in host entry indices.", file=sys.stderr)
		hosts = TTHosts()
		for idx in sorted(list(data.keys()), key=lambda ki: int(ki)):
			confdata = data[idx]
			if self.useLatest:
				confdata["name"] = TTHost.id(confdata)
			d = TTHost(confdata["name"], **confdata)
			hosts[confdata["name"]] = d
		return hosts

	def write(self, hosts, latest=False):
		"""Write to this .ini file all host entries in hosts.
		If latest is True, uses the latest-hosts section instead of the regular server list section.
		Warning: Also forces out spaces around equal signs.
		"""
		sect = self.sect
		try:
			with open(self.path, encoding="utf-8") as f: ini = INIConfig(f)
		except IOError: ini = INIConfig()
		try:
			for k in ini[sect]: del ini[sect][k]
		except TypeError: pass
		for idx,(shortname,host) in enumerate(hosts.items()):
			for k,v in host.__dict__.items():
				if k.lower() in ["iniindex", "shortname", "srvpassword", "url"]: continue
				if latest and k.lower() == "name": continue
				ki = str(idx) +"_" +k
				ini[sect][ki] = v
		with open(self.path, "w", encoding="utf-8", newline='\r\n') as f:
			ini = str(ini).splitlines(True)
			for i,line in enumerate(ini):
				if not line or line[0] in ";#[" or not " = " in line: continue
				ini[i] = line.replace(" = ", "=")
			f.write("".join(ini))

class TTFileTT(TTFile):
	"""Full absolute or relative path to a folder, not a file, where .tt files reside or will reside.
	useLatest is not supported and will raise an error if True..
	"""
	type = "tt"
	def __init__(self, spec, useLatest):
		if useLatest: raise ValueError('{0}: There is no "latest" section in a .tt file'.format(spec))
		self.version = "5.0"
		if "/.tt:" in spec:
			spec,ver = spec.split("/.tt:", 1)
			self.version = ver
		elif spec.endswith("/.tt"):
			spec = spec[:-4]
		else:
			raise ValueError(".tt file specs must end with /.tt or /.tt:versionNumber (e.g., /.tt:5.1)")
		if not os.path.exists(spec):
			raise ValueError("Path " +spec +" does not exist")
		self.path = spec
		super(TTFileTT, self).__init__(spec, useLatest)

	def write(self, hosts):
		"""Write to the previously given folder one .tt file for each of the hosts in hosts.
		"""
		# ToDo: No check for duplicates.
		tmpl = (
"""<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE teamtalk>
<teamtalk version="%version%">
    <host>
        <name>%(name)s</name>
        <address>%(hostaddr)s</address>
        <tcpport>%(tcpport)s</tcpport>
        <udpport>%(udpport)s</udpport>
            <encrypted>%(encrypted)s</encrypted>
        <auth>
            <username>%(username)s</username>
            <password>%(password)s</password>
        </auth>
        <join>
            <channel>%(channel)s</channel>
            <password>%(chanpassword)s</password>
        </join>
    </host>
</teamtalk>
""".replace("%version%", self.version))
		for idx,(shortname,host) in enumerate(hosts.items()):
			fname = host.name
			# TeamTalk does the first of these, to allow ports to be part of a name.
			# The second is my way of including channel paths when the host does. [DGL, 2021-12-03]
			fname = fname.replace(":", "_").replace("/", "_")
			fname = os.path.join(self.path, fname+".tt")
			buf = tmpl % host.__dict__
			with open(fname, "w", encoding="utf-8") as f: f.write(buf)

class TTFileXML(TTFile):
	"""Handler for one .xml file of TT links. These come from TeamTalk classic for Windows.
	spec may be a full or relative path to a file or just".xml" to construct the path from standard folder and file name for this type and OS.
	.xml.1, .xml.2, etc., also work for non-primary profiles.
	useLatest determines which section in the file to use.
	"""
	type = "xml"
	def __init__(self, spec, useLatest):
		base = os.path.basename(spec).lower()
		if base == ".xml" or re.match(r'\.xml\.\d+$', base):
			self.path = "TeamTalk5Classic" + base
			self.path = os.path.join(confpath(), self.path)
		else: self.path = spec
		self.sect = "hostmanager"
		if useLatest: self.sect = "latesthosts"
		super(TTFileXML, self).__init__(spec, useLatest)

	def read(self):
		"""Read one XML file and return the results as a TTHosts structure. self.useLatest determines which file section to use.
		"""
		hosts = TTHosts()
		with open(self.path, encoding="utf-8") as f: doc = minidom.parse(f)
		try: hostParent = doc.getElementsByTagName(self.sect)[0]
		except IndexError:
			return hosts
		hostInfo = hostParent.getElementsByTagName("host")
		for i,host in enumerate(hostInfo):
			if self.useLatest: 
				# LatestHosts does not include a name.
				name = ""
			else: name = host.attributes["name"].nodeValue
			d = {}
			d["name"] = name
			for c in host.childNodes:
				if c.nodeName == "#text": continue
				k = c.nodeName
				try: v = c.childNodes[0].nodeValue
				except IndexError: v = ""
				if k == "address": k = "hostaddr"
				elif k == "cpassword": k = "chanpassword"
				d[k] = v
			hosts.add(d)
		return hosts

def do_migrate(path=None):
	"""Implementation of the migrate mode.
	"""
	tasks = (
		("recent servers", ".xml:l", ".ini:l"),
		("named servers", ".xml", ".ini"),
	)
	if path:
		fn1 = os.path.join(path, "TeamTalk5Classic.xml")
		fn2 = os.path.join(path, "TeamTalk5.ini")
		tasks = (
			("recent servers", fn1+":l", fn2+":l"),
			("named servers", fn1, fn2),
		)
	for label,src,dest in tasks:
		hosts = TTHosts()
		hosts.read(src)
		print("Transferring {:d} {}".format(len(hosts), label))
		hosts.write(dest)

def do_wizard():
	"""The app behavior when given no arguments.
	"""
	portable = False
	if confirm("Are you migrating a portable TeamTalk instance (y for yes, n for a regular installation)?"):
		portable = True
	path = None
	if portable:
		while not path:
			path = input("Enter the path containing the TeamTalk files: ")
			path = path.strip()
			if not path:
				pauseAndExit("No path entered, aborting")
			if not os.path.exists(path):
				print("That folder does not exist")
				path = ""
				continue
			elif not os.path.isdir(path):
				print("That is not a folder")
				path = ""
				continue
	print("Scanning TeamTalk configurations for server entries ...")
	counts = {}
	if portable:
		fn1 = os.path.join(path, "TeamTalk5Classic.xml")
		fn2 = os.path.join(path, "TeamTalk5.ini")
		flist = (
			("cr", "Classic recent", fn1+":l"),
			("cn", "Classic named", fn1),
			("qr", "QT recent", fn2+":l"),
			("qn", "QT named", fn2),
		)
		del fn1, fn2
	else:
		flist = (
			("cr", "Classic recent", ".xml:l"),
			("cn", "Classic named", ".xml"),
			("qr", "QT recent", ".ini:l"),
			("qn", "QT named", ".ini"),
		)
	for id,label,src in flist:
		hosts = TTHosts()
		try:
			hosts.read(src)
			l = len(hosts)
			err = ""
		except Exception as e:
			l = 0
			err = f"{e.__class__.__name__}: {str(e)}"
			print(f"Error reading {label} servers: {err}")
			raise
		counts[id] = l
	print(f'Found {counts["qn"]} named and {counts["qr"]} unnamed recent servers in the QT client')
	print(f'Found {counts["cn"]} named and {counts["cr"]} unnamed recent servers in the classic client')
	prompt = "Migrate classic servers to QT client (y/n)?"
	if counts["qn"] > 0 or counts["qr"] > 0:
		prompt = "Replace QT servers with classic servers (y/n)?"
	if ((counts["cr"] > 0 or counts["cn"] > 0)
	and confirm(prompt)):
		do_migrate(path)

if __name__ == "__main__":
	args = sys.argv
	progname = args.pop(0)
	if not args:
		do_wizard()
		pauseAndExit(0)
	elif len(args) == 1 and args[0] in ["-h", "--help"]:
		pauseAndExit(__doc__)
	mode = ""
	while len(args):
		if args[0] == "-a": mode = "a"
		elif args[0] == "-u": mode = "u"
		else: break
		args.pop(0)
	if len(args) < 2: pauseAndExit(__doc__)
	dest = args[-1]
	# To append, read dest file just before updating it.
	if mode == "a": pass
	# To update (append and let other files change entries that are already in dest), read dest first.
	elif mode == "u": args.insert(0, args.pop(-1))
	# For replace, don't read the dest file at all before writing.
	else: args.pop(-1)
	sources = args
	hosts = TTHosts()
	for src in sources:
		hosts.read(src)
	hosts.write(dest)
