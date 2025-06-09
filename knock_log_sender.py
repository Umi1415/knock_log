import socket
import time
import os

LOG_FILE = "/var/log/auth.log"      # Log file to monitor (SSH/authentication logs)
TARGET_IP = "192.168.1.200"         # Replace with the IP of the log receiver
TARGET_PORT = 9999                  # TCP port to send the log data

def tail_f(file):
    """Generator that mimics tail -f behavior."""
    file.seek(0, os.SEEK_END)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

def main():
    print(f"[+] Connecting to {TARGET_IP}:{TARGET_PORT} ...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((TARGET_IP, TARGET_PORT))
        print("[+] Connection established. Sending logs...\n")
    except Exception as e:
        print(f"[!] Failed to connect: {e}")
        return

    try:
        with open(LOG_FILE, "r") as f:
            for line in tail_f(f):
                try:
                    sock.sendall(line.encode())
                    print(f"[SENT] {line.strip()}")
                except Exception as send_err:
                    print(f"[!] Error while sending data: {send_err}")
                    break
    except FileNotFoundError:
        print(f"[!] Log file not found: {LOG_FILE}")
    except PermissionError:
        print(f"[!] Permission denied when trying to read {LOG_FILE}. Try running as root.")
    finally:
        sock.close()
        print("[*] Connection closed.")

if _name_ == "_main_":
    main()
