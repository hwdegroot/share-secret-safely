from dataclasses import dataclass
from json import JSONEncoder


@dataclass
class SecretModel(JSONEncoder):
    secret: str

    def __init__(self, secret):
        self.secret = secret

    def default(self, o):
        return o.__dict__


@dataclass
class StoredSecretModel(JSONEncoder):
    id: str =  None
    api_link: str = None
    link: str = None
    expires_after_days: str = None

    def __init__(
        self,
        id: str,
        api_link: str,
        link: str,
        expires_after_days: int
    ):
        self.id = id
        self.api_link = api_link
        self.link = link
        self.expires_after_days = expires_after_days

    def default(self, o):
        return o.__dict__


@dataclass
class VersionModel(JSONEncoder):
    version: str
    build: str
    sha: str
    description: str

    def __init__(
        self,
        version: str=None,
        build: str=None,
        sha: str=None,
        description: str=None
    ):
        version: str
        build: str
        sha: str
        description: str

    def default(self, o):
        return o.__dict__

