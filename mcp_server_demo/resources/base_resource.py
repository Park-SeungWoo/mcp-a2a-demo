import re
from abc import ABCMeta, abstractmethod

from mcp_server_demo.exceptions.resource_exceptions import ResourceUriFormatException


class Resource(metaclass=ABCMeta):
    def __init__(self, uri: str, name: str, description: str = None, mime_type: str = None):
        self.uri: str = self.check_uri(uri)
        self.name: str = name
        self.description: str = description
        self.mime_type: str = mime_type

    @staticmethod
    def check_uri(uri) -> str:
        """
        URI pattern match
        :param uri: string
        :return: validated uri string
        :raises ResourceUriFormatException: If URI pattern does not match
        """
        uri_format: str = r'\b\w+:\/\/[^\s]+'

        if re.match(uri_format, uri):
            return uri

        raise ResourceUriFormatException()

    @classmethod
    def from_content(cls, content: 'ResourceContents') -> 'Resource':
        """
        [NotRecommended]\n
        save definition of contents
        :param content: ResourceContents
        :return: an instance of 'Resource'
        """
        return cls(content.uri, name="", mime_type=content.mime_type)


class ResourceContents(metaclass=ABCMeta):
    def __init__(self, uri: str, mime_type: str = None):
        self.uri: str = Resource.check_uri(uri)
        self.mime_type: str = mime_type

    @classmethod
    @abstractmethod
    def from_definition(cls, resource: 'Resource') -> 'ResourceContents':
        """
        Retrieve contents from resource definition\n
        This must be implemented by subclasses
        :param resource:
        :return: subclass of 'ResourceContents'
        :rtype: ResourceContents
        """
        raise NotImplementedError()


"""
굳이 Resource, ResourceContents를 나눠 구현해 둔 이유는 아래와 같음
실제 사용 환경에서 resource는 수도 없이 많음
메모리에 정의 부분만 올려두고 resource를 참조한 뒤 contents가 필요한 경우 해당 정보를 이용해 contents를
꺼내서 사용하면 성능 하락 없이 이용 가능
"""
