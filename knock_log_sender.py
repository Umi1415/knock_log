SENDER

import socket
import time
import pyfiglet
from colorama import init, Fore, Style
from datetime import datetime

init()  # Initialize colorama

LOG_FILE = "/var/log/auth.log"     # Lokasi log akses SSH
TARGET_IP = "192.168.161.109"      # IP server penerima
TARGET_PORT = 9999                 # Port TCP server penerima

def print_banner():
    banner = pyfiglet.figlet_format("SSH Log Hack", font="slant")
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    print(Fore.GREEN + " * Real-time SSH Access Log Monitor" + Style.RESET_ALL)
    print(Fore.GREEN + f" * Target: {TARGET_IP}:{TARGET_PORT}" + Style.RESET_ALL)
    print(Fore.GREEN + f" * Source Log File: {LOG_FILE}" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + "\n" + Style.RESET_ALL)

def tail_f(file):
    file.seek(0, 2)  # Baca dari akhir file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def is_ssh_related(line):
    # Cek apakah baris log terkait sshd (dapat disesuaikan lebih lanjut)
    keywords = ["sshd", "Accepted", "Failed", "authentication failure", "Connection closed"]
    return any(kw.lower() in line.lower() for kw in keywords)

def main():
    print_banner()
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(Fore.CYAN + f"[*] Connecting to {TARGET_IP}:{TARGET_PORT} ..." + Style.RESET_ALL)
    
    try:
        sock.connect((TARGET_IP, TARGET_PORT))
        print(Fore.GREEN + "[+] Connected successfully!" + Style.RESET_ALL)
        print(Fore.CYAN + "[*] Starting to monitor SSH access logs..." + Style.RESET_ALL)

        with open(LOG_FILE, "r") as f:
            loglines = tail_f(f)
            for line in loglines:
                if is_ssh_related(line):
                    try:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(Fore.WHITE + f"[{timestamp}] " + Fore.YELLOW + "SSH Log: " + line.strip() + Style.RESET_ALL)
                        sock.sendall(line.encode())
                    except Exception as e:
                        print(Fore.RED + f"[-] Error sending data: {e}" + Style.RESET_ALL)
                        break

    except ConnectionRefusedError:
        print(Fore.RED + "[-] Connection refused. Ensure the receiver is running." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[-] Error: {str(e)}" + Style.RESET_ALL)
    finally:
        sock.close()

if _name_ == "_main_":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] Program stopped by user." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n[-] Fatal error: {str(e)}" + Style.RESET_ALL)
