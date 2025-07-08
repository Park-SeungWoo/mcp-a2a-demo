import asyncio

from server import main as server_main


def run():
    asyncio.run(server_main())
