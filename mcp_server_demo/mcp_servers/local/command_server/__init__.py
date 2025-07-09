import asyncio

from server import CommandServer


def main():
    asyncio.run(CommandServer().run())
