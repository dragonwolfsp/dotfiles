import json
import os
import select
import socket
import ssl
import sys
import time
sys.path.append(os.path.dirname(__file__))
import miniupnpc
del sys.path[-1]
from logHandler import log
from . import socket_utils
from dataclasses import dataclass

class Server:
	PING_TIME: int = 300
	running: bool = False
	port: int
	password: str

	def __init__(self, port, password, bind_host='', bind_host6='[::]', UPNP=False):
		self.port = port
		self.password = password
		#Maps client sockets to clients
		self.clients = {}
		self.client_sockets = []
		self.invalid_join_attempts: dict[str, InvalidJoinAttempt] = {}
		self.running = False
		self.server_socket = self.create_server_socket(socket.AF_INET, socket.SOCK_STREAM, bind_addr=(bind_host, self.port))
		self.server_socket6 = self.create_server_socket(socket.AF_INET6, socket.SOCK_STREAM, bind_addr=(bind_host6, self.port))
		self.upnp = None
		if UPNP:
			self.upnp = miniupnpc.UPnP()

	def create_server_socket(self, family, type, bind_addr):
		server_socket = socket.socket(family, type)
		certfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.pem')
		server_socket = socket_utils.wrap_socket(server_socket, certfile=certfile)
		server_socket.bind(bind_addr)
		server_socket.listen(5)
		return server_socket

	def run(self):
		self.running = True
		if self.upnp:
			try:
				self.upnp.discoverdelay = 200
				self.upnp.discover()
				self.upnp.selectigd()
				self.upnp.addportmapping(self.port, 'TCP', self.upnp.lanaddr, self.port, 'TeleNVDA', '', 3600)
			except:
				self.upnp = None
		self.last_ping_time = time.monotonic()
		log.info("TeleNVDA direct connection server started")
		while self.running:
			r, w, e = select.select(self.client_sockets+[self.server_socket, self.server_socket6], [], self.client_sockets, 60)
			if not self.running:
				break
			for sock in r:
				if sock is self.server_socket or sock is self.server_socket6:
					self.accept_new_connection(sock)
					continue
				self.clients[sock].handle_data()
			if time.monotonic() - self.last_ping_time >= self.PING_TIME:
				if self.upnp:
					self.upnp.addportmapping(self.port, 'TCP', self.upnp.lanaddr, self.port, 'TeleNVDA', '', 3600)
				for client in self.clients.values():
					if client.authenticated:
						client.send(type='ping')
				self.last_ping_time = time.monotonic()

	def accept_new_connection(self, sock):
		try:
			client_sock, addr = sock.accept()
			log.info("New incoming connection from "+addr[0])
		except (ssl.SSLError, socket.error, OSError):
			return
		client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		client = Client(server=self, socket=client_sock)
		self.add_client(client)
		log.info("Created client "+str(client.id))

	def add_client(self, client):
		self.clients[client.socket] = client
		self.client_sockets.append(client.socket)
		if client.addr in self.invalid_join_attempts:
			a = self.invalid_join_attempts[client.addr]
			# The number of invalid attempts not subject to rate limiting
			FREE_ATTEMPTS: int = 3
			ban_for = (
				0 if a.attempts < FREE_ATTEMPTS
				else min(2 ** (a.attempts - FREE_ATTEMPTS), 2**6)
			)
			if  time.monotonic() - a.last_invalid_attempt_time <= ban_for:
				ban_remaining = round(
					ban_for - (time.monotonic() - a.last_invalid_attempt_time)
				)
				log.warning(
					f"Client {client.addr} banned for {ban_remaining} "
					f"seconds due to {a.attempts} invalid join attempts"
				)
				client.send(type='error', message='too_many_attempts')
				client.close()
				return

	def remove_client(self, client):
		del self.clients[client.socket]
		self.client_sockets.remove(client.socket)

	def client_disconnected(self, client):
		self.remove_client(client)
		if client.authenticated:
			client.send_to_others(type='client_left', user_id=client.id, client=client.as_dict())
		log.info("client "+str(client.id)+" has disconnected")

	def close(self):
		self.running = False
		self.server_socket.close()
		self.server_socket6.close()
		if self.upnp:
			self.upnp.deleteportmapping(self.port, 'TCP')
		log.info("TeleNVDA direct connection server stopped")

class Client:
	id: int = 0

	def __init__(self, server, socket):
		self.server = server
		self.socket = socket
		self.addr: str = self.socket.getpeername()[0]
		self.buffer = b''
		self.authenticated = False
		self.id = Client.id + 1
		self.connection_type = None
		self.protocol_version = 1
		Client.id += 1

	def handle_data(self):
		sock_data: bytes = b''
		try:
			# 16384 is 2^14 self.socket is a ssl wrapped socket.
			# Perhaps this value was chosen as the largest value that could be received [1] to avoid having to loop
			# until a new line is reached.
			# However, the Python docs [2] say:
			# "For best match with hardware and network realities, the value of bufsize should be a relatively
			# small power of 2, for example, 4096."
			# This should probably be changed in the future.
			# See also transport.py handle_server_data in class TCPTransport.
			# [1] https://stackoverflow.com/a/24870153/
			# [2] https://docs.python.org/3.7/library/socket.html#socket.socket.recv
			buffSize = 16384
			sock_data = self.socket.recv(buffSize)
		except:
			self.close()
			return
		if not sock_data: #Disconnect
			self.close()
			return
		data = self.buffer + sock_data
		if b'\n' not in data:
			self.buffer = data
			return
		self.buffer = b""
		while b'\n' in data:
			line, sep, data = data.partition(b'\n')
			try:
				self.parse(line)
			except ValueError:
				self.close()
				return
		self.buffer += data

	def parse(self, line):
		parsed = json.loads(line)
		if 'type' not in parsed:
			return
		if self.authenticated:
			self.send_to_others(**parsed)
			return
		fn = 'do_'+parsed['type']
		if hasattr(self, fn):
			getattr(self, fn)(parsed)

	def as_dict(self):
		return dict(id=self.id, connection_type=self.connection_type)

	def do_join(self, obj):
		password = obj.get('channel', None)
		if password != self.server.password:
			if self.addr not in self.server.invalid_join_attempts:
				self.server.invalid_join_attempts[self.addr] = InvalidJoinAttempt(self.addr)
			self.server.invalid_join_attempts[self.addr].last_invalid_attempt_time = time.monotonic()
			self.server.invalid_join_attempts[self.addr].attempts += 1
			self.send(type='error', message='incorrect_password')
			log.info("Client "+str(self.id)+" rejected due to wrong password. Password used: "+password)
			self.close()
			return
		elif self.addr in self.server.invalid_join_attempts:
			# This is a valid attempt, so reset the counter
			del self.server.invalid_join_attempts[self.addr]
		self.connection_type = obj.get('connection_type')
		self.authenticated = True
		clients = []
		client_ids = []
		for c in list(self.server.clients.values()):
			if c is self or not c.authenticated:
				continue
			clients.append(c.as_dict())
			client_ids.append(c.id)
		self.send(type='channel_joined', channel=self.server.password, user_ids=client_ids, clients=clients)
		self.send_to_others(type='client_joined', user_id=self.id, client=self.as_dict())
		log.info("Client joined current session")

	def do_protocol_version(self, obj):
		version = obj.get('version')
		if not version:
			return
		self.protocol_version = version

	def close(self):
		self.socket.close()
		self.server.client_disconnected(self)

	def send(self, type, origin=None, clients=None, client=None, **kwargs):
		msg = dict(type=type, **kwargs)
		if self.protocol_version > 1:
			if origin:
				msg['origin'] = origin
			if clients:
				msg['clients'] = clients
			if client:
				msg['client'] = client
		msgstr = json.dumps(msg)+'\n'
		try:
			self.socket.sendall(msgstr.encode('UTF-8'))
		except:
			self.close()

	def send_to_others(self, origin=None, **obj):
		if origin is None:
			origin = self.id
		for c in self.server.clients.values():
			if c is not self and c.authenticated:
				c.send(origin=origin, **obj)


@dataclass
class InvalidJoinAttempt:
	addr: str
	last_invalid_attempt_time: int = 0
	attempts: int = 0
