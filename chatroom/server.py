import asyncio
import json
import logging
import websockets

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(10)

STATE = {"value": 0}

USERS = set()

USERNAMES = set()

class colors:
    reset = "\033[0m"
    red = "\033[31;1m"

def state_event():
    return json.dumps({"type": "state", **STATE})

def users_event():
    return json.dumps({"type": "users", "count": len(USERS)})

def message_event(message):
    return json.dumps({"type": "message", "message": message})

async def counter(websocket, path):
    try:
        # Register new user
        USERS.add(websocket)
        websockets.broadcast(USERS, users_event())

        # Send current state to user
        await websocket.send(state_event())

        # Manage state changes
        async for message in websocket:
            data = json.loads(message)
            if data["action"] == "minus":
                STATE["value"] -= 1
                websockets.broadcast(USERS, state_event())
            elif data["action"] == "plus":
                STATE["value"] += 1
                websockets.broadcast(USERS, state_event())
            elif data["action"] == "message":
                if data["username"] in USERNAMES:
                    logger.log(20, f" Chat from {data['username']}: {data['message']}")
                    websockets.broadcast(USERS, message_event(f"{data['username']} >> {data['message']}"))
                else:
                    logger.error(f"{colors.red}Unregistered user tried sending message{colors.reset}: {data['message']}")
            elif data["action"] == "register":
                if data["username"] not in USERNAMES:
                    USERNAMES.add(data["username"])
                else:
                    await websocket.send(message_event("ERROR >> That username is taken, but security go brrrr... you logged in"))
            else:
                logger.error(f"Unsupported event: {data}")
    finally:
        USERS.remove(websocket)
        websockets.broadcast(USERS, users_event())

async def main():
    async with websockets.serve(counter, "localhost", 6789):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
