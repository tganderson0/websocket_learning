import asyncio
import websockets
import pathlib
import ssl
import subprocess
import os

USERS = set()

async def run_process(websocket, path):
    print("A user connected")
    currDir = os.getcwd()
    try: 
        USERS.add(websocket)
        async for message in websocket:
            print("Message received {message}")
            print(f"Running {message}")
            if "$PWD" in message:
                await websocket.send(currDir)
            elif "cd" in message:
                command = message.split()
                if (len(command) > 1):
                    command = command[1:]
                    print(command)
                    for path_part in command:
                        print(path_part)
                        currDir = os.path.join(currDir, path_part)
                    currDir = os.path.normpath(currDir)
                else:
                    currDir = os.getcwd()
                await websocket.send(" ")
            elif message == "close":
                await websocket.close()
            else:
                try:
                    process = subprocess.run(message.split(), capture_output=True, text=True, cwd=currDir)
                    await websocket.send(process.stdout)
                except (Exception) as e:
                    await websocket.send(str(e))
    finally:
        USERS.remove(websocket)

# This section gets the self signed certificate for using secure (wss)
# ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
# ssl_context.load_cert_chain(localhost_pem)


async def main():
    async with websockets.serve(run_process, "localhost", 8765):
        print(f"Starting server on localhost:8765")
        await asyncio.Future()

asyncio.run(main())
