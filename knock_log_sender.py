import socket
import time

LOG_FILE = "/var/log/knockd.log"   # Lokasi file log knockd
TARGET_IP = "192.168.1.200"        # Ganti dengan IP target penerima log
TARGET_PORT = 9999                 # Port TCP untuk kirim log

def tail_f(file):
    file.seek(0, 2)  # ke akhir file
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def main():
    # Setup koneksi socket ke target
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"Mencoba konek ke {TARGET_IP}:{TARGET_PORT} ...")
    sock.connect((TARGET_IP, TARGET_PORT))
    print("Terhubung, mulai kirim log...")

    with open(LOG_FILE, "r") as f:
        loglines = tail_f(f)
        for line in loglines:
            try:
                sock.sendall(line.encode())
            except Exception as e:
                print("Error kirim data:", e)
                break

    sock.close()

if __name__ == "__main__":
    main()
