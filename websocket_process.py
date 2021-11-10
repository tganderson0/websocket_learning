import asyncio
import websockets
from aioconsole import ainput

class colors:
    reset = "\033[0m"
    blue = "\033[34m"
    green = "\033[32m"

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        print("Connection complete, type 'exit' to stop")
        
        while True:
            await websocket.send("$PWD")
            cwd = await websocket.recv()
            command = await ainput(f"{colors.green}{uri}{colors.reset}:{colors.blue}{cwd}{colors.reset}$ ")
            if command == "exit":
                print("Good bye!")
                break;

            await websocket.send(command)
            result = await websocket.recv()
            print(f"{result}")

asyncio.run(hello())
