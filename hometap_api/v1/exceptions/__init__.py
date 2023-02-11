from fastapi.exceptions import HTTPException


class EnvironmentNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CredentialFileError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class HouseCanaryApiException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)