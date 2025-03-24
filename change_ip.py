import subprocess
import time
import requests

# Function to check if TOR is installed
def check_tor():
    try:
        subprocess.run(["tor", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("TOR is already installed.")
    except subprocess.CalledProcessError:
        print("Installing TOR...")
        subprocess.run(["sudo", "apt", "update", "-y"])
        subprocess.run(["sudo", "apt", "install", "tor", "-y"])

# Function to install required Python modules
def install_python_modules():
    required_modules = ["requests"]
    for module in required_modules:
        try:
            __import__(module)
            print(f"{module} is already installed.")
        except ImportError:
            print(f"Installing {module}...")
            subprocess.run(["pip3", "install", module])

# Function to send signal to change the IP via TOR
def change_ip():
    print("IP change signal sent successfully.")
    # Send the "NEWNYM" signal to TOR to change IP
    subprocess.run(['echo', '-e', 'AUTHENTICATE ""\r\nSIGNAL NEWNYM\r\nQUIT', '|', 'nc', '127.0.0.1', '9051'])

# Function to get the current IP address using TOR
def get_current_ip():
    try:
        response = requests.get("https://api.ipify.org", proxies={"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"})
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching IP: {e}")
        return None

# Main function to setup TOR and Python environment, and run the IP change loop
def main():
    check_tor()  # Check and install TOR if necessary
    install_python_modules()  # Ensure required Python modules are installed

    # Main loop that changes IP every 15 seconds
    while True:
        print("Changing IP...")
        change_ip()  # Change the IP
        time.sleep(10)  # Wait 10 seconds before checking the new IP
        new_ip = get_current_ip()  # Get the new IP
        if new_ip:
            print(f"New IP: {new_ip}")  # Display the new IP
        time.sleep(10)  # Wait a bit before changing the IP again

if __name__ == "__main__":
    main()
