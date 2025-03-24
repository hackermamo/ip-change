import subprocess
import time
import requests
import os

# Function to print banner
def print_banner():
    os.system('clear')
    print("\033[38;5;208m")  # Orange color
    print(r"""
 ██╗██████╗      ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
 ██║██╔══██╗    ██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
 ██║██████╔╝    ██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
 ██║██╔═══╝     ██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
 ██║██║         ╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║
 ╚═╝╚═╝          ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                                                                         
    """)
    print("\033[0m")
    print("\033[1;36m" + "Version: 1.0" + "\033[0m")
    print("\033[1;33m" + "Code Author: hackermamo" + "\033[0m")
    print("\033[1;36m" + "GitHub Profile : https://github.com/hackermamo" + "\033[0m")
    print("\033[1;31m" + "YouTube Channel: https://www.youtube.com/@TRIPURAJOBSTUDYINFORMATION11" + "\033[0m\n")

# Function to check if TOR is installed
def check_tor():
    try:
        subprocess.run(["tor", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("\033[1;34m[*] TOR is already installed.\033[0m")
    except subprocess.CalledProcessError:
        print("\033[1;33m[!] Installing TOR...\033[0m")
        subprocess.run(["sudo", "apt", "update", "-y"])
        subprocess.run(["sudo", "apt", "install", "tor", "-y"])

# Function to install required Python modules
def install_python_modules():
    required_modules = ["requests"]
    for module in required_modules:
        try:
            __import__(module)
            print(f"\033[1;34m[*] {module} is already installed.\033[0m")
        except ImportError:
            print(f"\033[1;33m[!] Installing {module}...\033[0m")
            subprocess.run(["pip3", "install", module])

# Function to send signal to change the IP via TOR
def change_ip():
    print("\033[1;32m[+] Sending IP change signal...\033[0m")
    subprocess.run(['echo', '-e', 'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT', '|', 'nc', '127.0.0.1', '9051'])

# Function to get the current IP address using TOR
def get_current_ip():
    try:
        response = requests.get("https://api.ipify.org", proxies={"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"})
        return response.text
    except requests.RequestException as e:
        print(f"\033[1;31m[!] Error fetching IP: {e}\033[0m")
        return None

# Main function to setup TOR and Python environment, and run the IP change loop
def main():
    print_banner()
    check_tor()  # Check and install TOR if necessary
    install_python_modules()  # Ensure required Python modules are installed

    print("\033[1;36m[*] Changing your IP every 15 seconds...\033[0m")
    print("\033[1;33m[!] Press Ctrl + C to stop.\033[0m\n")

    try:
        while True:
            print("\033[1;34m[*] Changing IP...\033[0m")
            change_ip()  # Change the IP
            time.sleep(10)  # Wait 10 seconds before checking the new IP
            new_ip = get_current_ip()  # Get the new IP
            if new_ip:
                print(f"\033[1;32m[+] New IP: {new_ip}\033[0m")
            time.sleep(10)  # Wait before changing again
    except KeyboardInterrupt:
        print("\n\033[1;31m[!] Exiting... Stopping TOR service.\033[0m")
        subprocess.run(["sudo", "systemctl", "stop", "tor"])

if __name__ == "__main__":
    main()
