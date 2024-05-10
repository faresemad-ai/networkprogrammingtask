import socket
import threading
import ast

def receive_messages(sock):
    while True:
        try:
            size_bytes = sock.recv(8)
            size = int.from_bytes(size_bytes, 'big')
            data = sock.recv(size).decode('utf-8')
            print(data)
        except socket.error:
            break

def send_message(sock):
    while True:
        message = input()
        recipient = input("Enter recipient address (host:port): ")
        data = f"{recipient}:{message}"
        sock.send(len(data).to_bytes(8,'big'))
        sock.send(data.encode('utf-8'))

def start_chat():
    host = 'localhost'
    port = 8000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port)) # connected to server

    receive_thread = threading.Thread(target=receive_messages, args=(sock,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_message, args=(sock,))
    send_thread.start()

if __name__ == '__main__':
    start_chat()




# server

def handle_client(client_session, client_address):
    while True:
        try:
            size_bytes = client_session.recv(8)
            size = int.from_bytes(size_bytes, 'big')
            data = client_session.recv(size).decode('utf-8')
            if not data:
                break
            print(f"Received from {client_address}: {data} : with size {size}")

            # Extract the recipient client's address from the message
            recipient_address, message = data.split(':', 1)

            # Find the recipient client's socket
            recipient_socket = None
            for client in clients:
                """
                The ast.literal_eval() function safely evaluates a string containing a Python literal 
                (such as a tuple, list, dictionary, number, or string) and returns the corresponding Python 
                object. It ensures that only literals are evaluated, preventing the execution of arbitrary code.
                """
                if client[1] == ast.literal_eval(recipient_address): # or you can convert client[1] to str: if str(client[1]) == recipient_address
                    recipient_socket = client[0]
                    break
            if recipient_socket:
                # Send the message to the recipient client
                
                recipient_socket.send(size_bytes)
                recipient_socket.send(message.encode('utf-8'))
            else:
                print(f"Recipient not found: {recipient_address}")

        except socket.error:
            break

    print(f"Connection closed with {client_address}")
    clients.remove((client_session, client_address))
    client_session.close()

def start_server():
    host = 'localhost'
    port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")
    while True:
        client_session, client_address = server_socket.accept()
        clients.append((client_session, client_address))
        print(f"Connected with {client_address}")
        threading.Thread(target=handle_client, args=(client_session, client_address)).start()

if __name__ == '__main__':
    clients = []
    start_server()
