import inspect
from abc import ABCMeta

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, Tool, TextContent, ImageContent, EmbeddedResource
from pydantic import AnyUrl

from mcp_server_demo.common.exceptions.errors import McpPrimitiveImportError
from mcp_server_demo.common.exceptions.tool_exceptions import ToolNotExistException
from mcp_server_demo.common.interfaces.custom_tool import CustomTool
from mcp_server_demo.common.utils import string_utils as strutil


class McpServer(metaclass=ABCMeta):
    def __init__(self):
        self.server: Server = Server(f"{strutil.pascal_to_snake(self.__class__.__name__)}")
        self.__dynamic_import()

    def __dynamic_import(self):
        from pathlib import Path
        import sys

        base_path = Path(__file__).parent.absolute()
        try:
            sys.path.append(str(base_path))

            self.tools = __import__('tools')
            self.resources = __import__('resources')
            self.prompts = __import__('prompts')
        except ModuleNotFoundError:
            raise McpPrimitiveImportError()
        finally:
            sys.path.remove(str(base_path))

    def set_handlers(self):
        @self.server.list_resources()
        async def list_resources() -> list[Resource]:
            # TODO: resources, prompts 혹은 추가적인 primitives 들 handler 관련 부분 이와 같이 등록되도록 관리
            # custom한 구조로 우선 package based architecture(PBA) 이라고 명명
            # 추가 작업들이 마무리 된 후 다시 여기 관련 작업 수행하자
            # define kinda api specs
            return [
                Resource(
                    uri=AnyUrl("file:///logs/app.log"),
                    name="app log",
                    mimeType="text/plain",
                )  # sample
            ]

        @self.server.read_resource()
        async def read_resource(uri: AnyUrl) -> str:
            # kinda view methods
            if str(uri) == 'file:///logs/app.log':  # sample
                pass

            raise ValueError(f"URI not found: {uri}")  # replace with custom exception

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            tool_cls: list = inspect.getmembers(self.tools, inspect.isclass)
            return [tool.spec() for _, tool in tool_cls if issubclass(tool, CustomTool)]

        @self.server.call_tool()
        async def call_tool(name: str, kwargs: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
            tool: CustomTool = getattr(self.tools, strutil.snake_to_pascal(name), None)
            if tool:
                return await tool.execute(**kwargs)  # must handle arg error -> generate custom exception to handle it
            raise ToolNotExistException(name)

    async def run(self):
        print(f"\033[94mMCP-{self.__class__.__name__} now running!\033[0m")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )
