import socket
import time 

FILE_DIR = "./file"
BUFFER_SIZE = 4096

def udp_client(host='192.168.235.131', port=8001):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.sendto(b'request_file_list', (host, port)) 
        
        file_list_str, _ = client.recvfrom(BUFFER_SIZE)

        file_list = file_list_str.decode().splitlines()  
        
        print("Available files:")
        for index, file_name in enumerate(file_list):
            print(f"{index}: {file_name}")

        while True:
            try:
                chosen_index = int(input("Enter the index of the file you want to download: ").strip())
                if 0 <= chosen_index < len(file_list):
                    chosen_file = file_list[chosen_index]
                    break
                else:
                    print("Invalid index. Please choose a valid index.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        client.sendto(chosen_file.encode(), (host, port))  

        start_time = time.time()
        with open(f"./download_udp/{chosen_file}", 'wb') as f:
            while True:
                data, addr = client.recvfrom(BUFFER_SIZE)
                if data == b'EOF':
                    break
                f.write(data)
        end_time = time.time()
        print(f"File '{chosen_file}' downloaded successfully in {end_time - start_time:.4f} seconds")

                    
def tcp_client(host='192.168.235.131', port=8000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))

        file_list_str = client.recv(BUFFER_SIZE).decode()
        file_list = file_list_str.splitlines() 
        
        print("Available files:")
        for index, file_name in enumerate(file_list):
            print(f"{index}: {file_name}")

        while True:
            try:
                chosen_index = int(input("Enter the index of the file you want to download: ").strip())
                if 0 <= chosen_index < len(file_list):
                    chosen_file = file_list[chosen_index]
                    break
                else:
                    print("Invalid index. Please choose a valid index.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        client.sendall(chosen_file.encode())

        start_time = time.time()
        with open(f"./download_tcp/{chosen_file}", 'wb') as f:
            while True:
                data = client.recv(BUFFER_SIZE)
                if data == b'EOF':
                    break
                f.write(data)
        end_time = time.time()
        print(f"File '{chosen_file}' downloaded successfully in {end_time - start_time:.4f} seconds")

def start_client():
    while True:
        print("Select connection type:")
        print("1. TCP")
        print("2. UDP")
        print("3. Exit")
        choice = input("Enter 1 for TCP, 2 for UDP, or 3 to exit: ")

        if choice == '1':
            tcp_client()
        elif choice == '2':
            udp_client()
        elif choice == '3':
            print("Exiting client.")
            break
        else:
            print("Invalid choice!")

if __name__ == '__main__':
    start_client()
