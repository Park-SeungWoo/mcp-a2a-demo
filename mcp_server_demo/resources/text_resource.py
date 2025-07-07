from base_resource import ResourceContents
from mcp_server_demo.resources import Resource

__all__ = ['TextResourceContent']


class TextResourceContent(ResourceContents):
    def __init__(self, text: str, uri: str, mime_type: str = None):
        """
        :param text: str type text data
        :param uri: str
        :param mime_type: content type e.g., text/plain
        """
        super().__init__(uri, mime_type)
        self.text = text

    @classmethod
    def from_definition(cls, resource: 'Resource') -> 'ResourceContents':
        pass
