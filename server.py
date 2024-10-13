import os
import socket
import threading 

FILE_DIR = "./file"
BUFFER_SIZE = 4096

def udp_server(host='192.168.235.131', port=8001):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((host, port))
        print(f"UDP Server listening on {host}:{port}")
        
        while True:
            file_list = os.listdir(FILE_DIR)
            file_list_str = "\n".join(file_list)
            data, addr = server.recvfrom(BUFFER_SIZE)
            
            server.sendto(file_list_str.encode(), addr)
            
            chosen_file, addr = server.recvfrom(BUFFER_SIZE)
            chosen_file = chosen_file.decode().strip()
            print(f"Client chose file: {chosen_file} via UDP")
            
            if chosen_file in file_list:
                file_path = os.path.join(FILE_DIR, chosen_file)

                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(BUFFER_SIZE)
                        if not data:
                            break
                        server.sendto(data, addr)
                server.sendto(b'EOF', addr)
                print(f"File '{chosen_file}' sent successfully to {addr} via UDP")
            else:
                server.sendto(b"ERROR: File not found", addr)


def tcp_server(host='192.168.235.131', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(1)
        print(f"TCP Server listening on {host}:{port}")

        while True:
            conn, addr = server.accept()
            with conn:
                print(f"TCP Connected by {addr}")

                file_list = os.listdir(FILE_DIR)
                file_list_str = "\n".join(file_list)

                conn.sendall(file_list_str.encode())
                print(f"Sent file list to {addr}")

                chosen_file = conn.recv(BUFFER_SIZE).decode().strip()
                print(f"Client chose file: {chosen_file} via TCP")

                if chosen_file in file_list:
                    file_path = os.path.join(FILE_DIR, chosen_file)

                    with open(file_path, 'rb') as f:
                        while True:
                            data = f.read(BUFFER_SIZE)
                            if not data:
                                break
                            conn.sendall(data) 
                    print(f"File '{chosen_file}' sent successfully to {addr} via TCP")
                else:
                    conn.sendall(b"ERROR: File not found")

def start_servers():
    tcp_thread = threading.Thread(target=tcp_server, daemon=True)
    udp_thread = threading.Thread(target=udp_server, daemon=True)
    
    tcp_thread.start()
    udp_thread.start()
    
    print("Servers are running...\n")

if __name__ == '__main__':
    os.makedirs(FILE_DIR, exist_ok=True)
    start_servers()
    input("Press Enter to exit...\n")
