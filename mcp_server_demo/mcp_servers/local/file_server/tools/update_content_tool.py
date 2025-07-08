from mcp import Tool
from mcp.types import TextContent, ImageContent, EmbeddedResource

from mcp_server_demo.common.interfaces.custom_tool import CustomTool


class UpdateContentTool(CustomTool):
    # @override
    @staticmethod
    def spec() -> Tool:
        # TODO: use some class with serialize/deserialize method instead of properties dict
        return Tool(
            name='update_content_tool',
            description='Update file content',
            inputSchema={
                'type': 'object',
                'properties': {
                    'file_name': {
                        'type': 'string',
                        'description': 'File name',
                    },
                    'content': {
                        'type': 'string',
                        'description': 'File content',
                        'maxLength': 10,
                        'minLength': 1,
                    }
                },
                'required': ['file_name', 'content']
            }
        )

    # @override
    @staticmethod
    async def execute(file_name: str, content: str) -> list[TextContent | ImageContent | EmbeddedResource]:
        with open(file_name, 'w') as f:
            f.write(content)
        return []  # response objects
