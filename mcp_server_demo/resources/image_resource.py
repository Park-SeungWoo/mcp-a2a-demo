from base_resource import ResourceContents
from mcp_server_demo.resources import Resource

__all__ = ['ImageResourceContent']


class ImageResourceContent(ResourceContents):
    def __init__(self, blob: str, uri: str, mime_type: str = None):
        """
        :param blob: base64 encoded blob
        :param uri: str
        :param mime_type: content type e.g., image/png
        """
        super().__init__(uri, mime_type)
        self.blob: str = blob

    @classmethod
    def from_definition(cls, resource: 'Resource') -> 'ResourceContents':
        pass
