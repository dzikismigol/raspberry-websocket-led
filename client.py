import asyncio
import websockets

commands = {"1": "on", "0": "off"}


async def hello():
    async with websockets.connect('ws://192.168.31.20:8765') as websocket:
        while True:
            command = input("")
            if command in commands.keys():
                command = commands[command]
                await websocket.send(command)
                print("> {}".format(command))
                response = await websocket.recv()
                print("< {}".format(response))
            else:
                print("error")


asyncio.get_event_loop().run_until_complete(hello())
