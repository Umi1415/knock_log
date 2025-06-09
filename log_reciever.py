import socket

LISTEN_IP = "0.0.0.0"   # Mendengarkan semua interface
LISTEN_PORT = 9999      # Port harus sama dengan target port di server

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((LISTEN_IP, LISTEN_PORT))
    server_sock.listen(1)
    print(f"Mendengarkan koneksi di {LISTEN_IP}:{LISTEN_PORT}...")

    conn, addr = server_sock.accept()
    print(f"Koneksi diterima dari {addr}")

    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data.decode(), end='')  # Tampilkan log yang diterima secara real-time

    print("Koneksi terputus")
    server_sock.close()

if __name__ == "__main__":
    main()
