import asyncio
import websockets
import pathlib
import ssl

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")


# This section gets the self signed certificate for using secure (wss)
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
# ssl_context.load_cert_chain(localhost_pem)


async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
