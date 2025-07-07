from base_resource import ResourceContents
from mcp_server_demo.resources import Resource

__all__ = ['DBResourceContent']


class DBResourceContent(ResourceContents):
    def __init__(self, uri: str, mime_type: str = None):
        # TODO: the content type might be the queryset type
        super().__init__(uri, mime_type)

    @classmethod
    def from_definition(cls, resource: 'Resource') -> 'ResourceContents':
        pass
