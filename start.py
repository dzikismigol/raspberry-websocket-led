from gpiozero import PWMLED, Button, LED
from time import sleep

import asyncio
import websockets

button = Button(2)
led = PWMLED(17)

commands = {"on", "off"}
state = "off"
level = 0

async def hello(websocket, path):
    while True:
        command = await websocket.recv()

        if command in commands:
            process(command)
            await websocket.send("ok")
            print("> {}".format("ok"))
        else:
            await websocket.send("error")
            print("> error")


def process(command):
    global state
    state = command


async def led_control():
    global level
    while True:
        if state == "on" and level < 1:
            level = min(level + 0.1, 1)
        elif state == "off" and level > 0:
            level = max(level - 0.1, 0)
        led.value = level
        print("led: set to {}", level)
        await asyncio.sleep(0.1)


start_server = websockets.serve(hello, '0.0.0.0', 8765)

loop = asyncio.get_event_loop()
loop.create_task(led_control())
loop.run_until_complete(start_server)
loop.run_forever()
