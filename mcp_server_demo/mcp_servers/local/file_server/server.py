import inspect

from pydantic import AnyUrl
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource, TextContent, ImageContent, EmbeddedResource, Tool

import tools
from mcp_server_demo.common.exceptions.tool_exceptions import ToolNotExistException
from mcp_server_demo.common.interfaces.custom_tool import CustomTool
from mcp_server_demo.common.utils.string_utils import snake_to_pascal

app = Server('file-server')


# TODO: 각 단에서 exception handling 할까
# TODO: logging도
# TODO: caching도 가능 하면

# TODO: resource도 각 mcp 서버 내에 resources folder 만들어 두고 그 내부 구조 바탕 uri 및 read resource function 작성
# FileResourceHandler, DBResourceHandler 등등 handler로 해당 action 받고,
# 뒤에 붙은 path 기반 내부에서 데이터 처리하도록 할까
# 그러면 Tool도 ToolHandler class를 만들어서 관리할까
# command pattern 적용 고려
@app.list_resources()
async def list_resources() -> list[Resource]:
    # define kinda api specs
    return [
        Resource(
            uri=AnyUrl("file:///logs/app.log"),
            name="app log",
            mimeType="text/plain",
        )  # sample
    ]


@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    # kinda view methods
    if str(uri) == 'file:///logs/app.log':  # sample
        pass

    raise ValueError(f"URI not found: {uri}")  # replace with custom exception


@app.list_tools()
async def list_tools() -> list[Tool]:
    tool_cls: list = inspect.getmembers(tools, inspect.isclass)
    return [tool.spec() for _, tool in tool_cls if issubclass(tool, CustomTool)]


@app.call_tool()
async def call_tool(name: str, kwargs: dict) -> list[TextContent | ImageContent | EmbeddedResource]:
    tool: CustomTool = getattr(tools, snake_to_pascal(name), None)
    if tool:
        return await tool.execute(**kwargs)  # must handle arg error -> generate custom exception to handle it
    raise ToolNotExistException(name)


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )
