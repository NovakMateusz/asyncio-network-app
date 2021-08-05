import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Using TCP
address = ('localhost', 8000)
server_socket.bind(address)
server_socket.listen()
try:
    connection, client_address = server_socket.accept()
    print(f'Address: {client_address}')

    buffer = connection.recv(2)  # Setting buffer's low capacity
    print(f"Data received: {buffer}")

    while buffer[-1:] != b'\n':
        data = connection.recv(2)
        print(f"Data received: {data}")
        buffer += data

    print(f"Add data: {buffer}")
    connection.sendall(buffer)

finally:
    server_socket.close()
