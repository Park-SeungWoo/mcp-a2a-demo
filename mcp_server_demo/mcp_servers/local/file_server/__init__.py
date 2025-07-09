import asyncio

# from server import main as server_main
#
#
# def run():
#     asyncio.run(server_main())

from server import FileServer


def main():
    asyncio.run(FileServer().run())


main()
