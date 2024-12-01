#!/usr/bin/env python

import asyncio
import http
import signal
from websockets.asyncio.server import serve

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

async def health_check(path):
    return path == "/healthz"

async def handler(websocket, path):
    if await health_check(path):
        await websocket.send("OK\n")
    else:
        await echo(websocket, path)

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with serve(handler, host="", port=8080):
        await stop

if __name__ == "__main__":
    asyncio.run(main())
