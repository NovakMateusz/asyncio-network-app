import socket
import selectors

selector = selectors.DefaultSelector()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Using TCP

address = ('localhost', 8000)
server_socket.bind(address)
server_socket.setblocking(False)
server_socket.listen()


selector.register(server_socket, selectors.EVENT_READ)

try:
    while True:
        events_list = selector.select(timeout=5)
        if not events_list:
            print("No events, waiting 5 seconds")

        for event, _ in events_list:
            event_socket = event.fileobj

            if event_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                client_socket.setblocking(False)
                client_socket.send(b'Welcome\n')
                selector.register(client_socket, selectors.EVENT_READ)  # registering new client socket
                print(f'Address: {client_address}')
            else:
                buffer = event_socket.recv(2)  # Setting buffer's low capacity
                print(f"Data received: {buffer}")
                while buffer[-1:] != b'\n':
                    data = event_socket.recv(2)
                    print(f"Data received: {data}")
                    buffer += data

                print(f"Add data: {buffer}")
                event_socket.send(buffer)
finally:
    server_socket.close()
