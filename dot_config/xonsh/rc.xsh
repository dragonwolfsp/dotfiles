#pythonic imports
import json

#Show full python tracebacks.
$XONSH_SHOW_TRACEBACK = True

#change up that color theam.
$XONSH_COLOR_STYLE='dracula'

#make the default prompt a bit more useful.
$PROMPT = '{curr_branch} {env_prefix}{env_name}{env_postfix} {user}@{hostname}:{cwd} {last_return_code}-{prompt_end}'

#plugins
#Get currently usable xontribs first.
xontribs = json.loads($(xontrib list --json))
#replace some corutils with faster equivalents.
xontrib load coreutils
#for starship prompt.
if !(which starship):
	if 'prompt_starship' in xontribs:
		xontrib load prompt_starship
	else:
		echo xontrib-prompt-starship is missing, using xonsh prompt instead.
else:
	echo Starship is missing, using xonsh prompt instead.
#add abbrevs
if 'abbrevs' in xontribs:
	xontrib load abbrevs
	abbrevsAreHere=True
else:
	echo xontrib-abbrevs is missing, abbrevs will be unuseable.
	abbrevsAreHere=False

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

#custom ls functions to use prefered settings and replace ls with eza
def _ls(args):
	if ezaIsHere:
		eza -am1F --color=auto @(args)
	else:
		ls -Amp1 --color=auto @(args)

def _lsLong(args):
	if ezaIsHere:
		eza -almF --color=auto @(args)
	else:
		ls -Almp --color=auto @(args)

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

#define aliases
aliases['ls'] = _ls
aliases['ll'] = _lsLong
aliases['gcom'] = _gcom
aliases['gpush'] = _gpush
aliases['glog'] = _glog
aliases['cd'] = _superCd
aliases['gpip'] = _gpip
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
	if rtn in (2, 126): 
		result = input('rerun as administrator?')
		if result.lower() in ('y','yes'):
			sudo @(cmd)