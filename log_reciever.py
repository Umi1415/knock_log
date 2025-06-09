import socket

LISTEN_IP = "0.0.0.0"   # Listen on all interfaces
LISTEN_PORT = 9999      # Must match the sender's target port

def main():
    print(f"[+] Starting log receiver on {LISTEN_IP}:{LISTEN_PORT}...")
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((LISTEN_IP, LISTEN_PORT))
    server_sock.listen(1)
    print("[+] Waiting for incoming connection...")

    conn, addr = server_sock.accept()
    print(f"[+] Connection established from {addr[0]}:{addr[1]}")

    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    print("\n[*] Connection closed by sender.")
                    break
                log_line = data.decode(errors="ignore")
                print(f"[LOG] {log_line}", end='')  # Real-time display of received logs
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        conn.close()
        server_sock.close()
        print("[*] Receiver socket closed.")

if _name_ == "_main_":
    main()
