import socket
import pyfiglet
from colorama import init, Fore, Style
import time
from datetime import datetime

init()  # Initialize colorama

LISTEN_IP = "0.0.0.0"   # Mendengarkan semua interface
LISTEN_PORT = 9999      # Port harus sama dengan target port di server

def print_banner():
    banner = pyfiglet.figlet_format("KnockLog Receiver", font="slant")
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    print(Fore.GREEN + " * Knock Sequence Log Monitor Receiver" + Style.RESET_ALL)
    print(Fore.GREEN + f" * Listening on: {LISTEN_IP}:{LISTEN_PORT}" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + "\n" + Style.RESET_ALL)

def main():
    print_banner()
    
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((LISTEN_IP, LISTEN_PORT))
    server_sock.listen(1)
    print(Fore.CYAN + "[*] Waiting for connection..." + Style.RESET_ALL)

    conn, addr = server_sock.accept()
    print(Fore.GREEN + f"[+] Connection accepted from {addr}" + Style.RESET_ALL)

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(Fore.WHITE + f"[{timestamp}] " + Fore.YELLOW + data.decode().strip() + Style.RESET_ALL)

    print(Fore.RED + "\n[-] Connection closed" + Style.RESET_ALL)
    server_sock.close()

if _name_ == "_main_":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n[-] Server stopped by user" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n[-] Error: {str(e)}" + Style.RESET_ALL)
