class SecretNotFoundException(Exception):
    pass


class SecretAlreadyViewedException(Exception):
    pass


class InvalidSecretIdentifierException(Exception):
    pass


class SecretExpiredException(Exception):
    pass
