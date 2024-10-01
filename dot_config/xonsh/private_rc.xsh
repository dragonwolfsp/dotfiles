#pythonic imports
import json
import threading


#functions to simplify setup.

def promptSetUp():
	if shellPrompt == 1:
		if  not !(which starship):
			echo Starship is missing, using xonsh prompt instead.
		elif 'prompt_starship' in xontribs==False:
			echo xontrib-prompt-starship is missing, using xonsh prompt instead.
		else:
			xontrib load prompt_starship
	elif shellPrompt == 2:
		if not !(which oh-my-posh):
			echo oh-my-posh is missing, using xonsh prompt instead.
		else:
			execx($(oh-my-posh init xonsh --config "$POSH_THEMES_PATH/powerline.omp.json" ))

#Show full python tracebacks.
$XONSH_SHOW_TRACEBACK = True

#change up that color theam.
$XONSH_COLOR_STYLE='dracula'

#make the default prompt a bit more useful.
$PROMPT = '{curr_branch} {env_prefix}{env_name}{env_postfix} {user}@{hostname}:{cwd} {last_return_code}-{prompt_end}'

#Set linux accessibility variables.
$QT_LINUX_ACCESSIBILITY_ALWAYS_ON=1
$ACCESSIBILITY_ENABLED=1
$QT_ACCESSIBILITY=1
$GNOME_ACCESSIBILITY=1

# ensure that command output is captured, warning: this breakse some interactiv commands.
$XONSH_CAPTURE_ALWAYS = True


# Set variables to easily change settings later on.
# 0 = built in xonsh prompt, 1 = starship, 2 = oh-my-posh
shellPrompt = 1

#add things to path
if not '~/.local/bin' in $PATH:
	$PATH.append('~/.local/bin')

#plugins
#Get currently usable xontribs first.
xontribs = json.loads($(xontrib list --json))
#replace some corutils with faster equivalents.
xontrib load coreutils
#add abbrevs
if 'abbrevs' in xontribs:
	xontrib load abbrevs
	abbrevsAreHere=True
else:
	echo xontrib-abbrevs is missing, abbrevs will be unuseable.
	abbrevsAreHere=False
#better tab completion thrue fish shell.
if 'fish_completer' in xontribs: 
	if not !(which fish):
		echo "Fish is missing, many tab completions will be unavailable."
	else:
		xontrib load fish_completer
else:
	echo "xontrib-fish-completer is missing, many tab completions will be unavailable"
#Automaticly run ssh-agent.
if "ssh_agent" in xontribs:
	if not !(which ssh-agent):
		echo "ssh-agent is not installed, ssh keys can not be remembered."
	xontrib load ssh_agent
else:
	echo "xontrib-ssh-agent is missing, ssh keys can not be remembered."

#Enable onepath so xonsh will be smart about files and directories.
if 'onepath' in xontribs:
	xontrib load onepath
else:
	echo "xontrib_onepath is missing, xonsh will not be smart about files and directories."

# Run function to set up prompt.
promptSetUp()

#set up other shell utilities.
#Zoxide, the way smarter version of cd.
if not !(which zoxide):
	echo zoxide is missing, using cd instead.
	zoxideIsHere=False
else:
	execx($(zoxide init xonsh), 'exec', __xonsh__.ctx, filename='zoxide')
	zoxideIsHere=True

#Use eza instead of ls if available.
if not !(which eza):
	ezaIsHere = False
	echo eza is missing, using ls instead.
else:
	ezaIsHere = True

#For greate tab completion thrue carapace-bin 
if not !(which carapace):
	echo Carapace is missing, many tab completions will be unavailable.
else:
	exec($(carapace _carapace))

# Start the fastfetch
def ffthread():
	print($(fastfetch))
fastThread=threading.Thread(target = ffthread)
fastThread.start()

#custom ls functions to use prefered settings and replace ls with eza
def _ls(args):
	if ezaIsHere:
		eza -am1F --color=auto --sort=Name  @(args)
	else:
		ls -Amp1 --color=auto --sort=version @(args)

def _lsLong(args):
	if ezaIsHere:
		eza -almF --color=auto --sort=Name @(args)
	else:
		ls -Almp --color=auto --sort=version @(args)

#quick git commands.
def _gcom(args):
	git add .
	git commit -m @(args)

def _gpush(args):
	git add .
	git commit -m @(args)
	git push

def _glog(args):
	git --no-pager log --oneline @(args)

#greate littel directory backjump shortcut, this also takes care of zoxide.
def _superCd(args):
	arguments = ''
	if len(args)>0:
		if args[0].startswith('...'):
			arguments = '../' * len(args[0])
		else:
			arguments=args
	if zoxideIsHere:
		z @(arguments)
	else:
		chdir @(arguments)

#Get public ip adress.
def _gpip():
#we print because starship likes to eat the curl output on some systems.
	print($(curl -s http://ifconfig.me/ip))

# unlock bitwarden and set BW_SESSION in one command.
def _pitwarden():
	$BW_SESSION = $(bw unlock --raw)

#define aliases
aliases['ls'] = _ls
aliases['ll'] = _lsLong
aliases['gcom'] = _gcom
aliases['gpush'] = _gpush
aliases['glog'] = _glog
aliases['cd'] = _superCd
aliases['gpip'] = _gpip
aliases['pitwarden'] = _pitwarden
if zoxideIsHere:
	aliases['cdi'] = 'zi'

#define abreevs
if abbrevsAreHere:
	abbrevs['gst'] = 'git status'
	abbrevs['gch'] = 'git checkout <edit>'
	abbrevs['ariac'] = 'aria2c -x 16 -s 16 <edit>'

#Ask to rerun if a command requires administrator permitions.
@events.on_postcommand
def on_postcommand(cmd: str, rtn: int, out: str || None, ts: list):
	subs = ('administrator', 'root', 'admin')
	if rtn in (2, 126) or (rtn>0 and out is not None and any(sub in out.lower() for sub in subs)):
		result = input('rerun as administrator?')
		if result.lower() in ('y','yes'):
			#Rerun with sudo, we have to use rstrip and split to make the flags not count as one string.
			sudo @(arg for arg in cmd.rstrip().split(' '))
