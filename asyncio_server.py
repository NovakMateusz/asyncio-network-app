import asyncio
from asyncio import AbstractEventLoop
import socket


async def echo(client_socket: socket,
               loop: AbstractEventLoop) -> None:
    while data := await loop.sock_recv(client_socket, 1024):
        await loop.sock_sendall(client_socket, data)


async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        client_socket, client_address = await loop.sock_accept(server_socket)
        client_socket.setblocking(False)
        print(f"Address: {client_address}")
        asyncio.create_task(echo(client_socket, loop))


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    await listen_for_connection(server_socket, asyncio.get_event_loop())


asyncio.run(main())
