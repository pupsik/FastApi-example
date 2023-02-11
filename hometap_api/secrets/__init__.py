import os
from typing import Callable

from hometap_api.v1.exceptions import CredentialFileError


class SecretStore:
    @classmethod
    def get_secret(
        cls, secret_name: str, get_method: Callable[..., str] = None, *args, **kwargs
    ) -> str:
        if get_method is None:
            get_method = cls.read_from_file

        return get_method(secret_name, *args, **kwargs)

    @staticmethod
    def read_from_file(name: str, directory: str) -> str:
        filename = os.path.join(directory, f"{name}.txt")
        try:
            with open(filename, "r") as f:
                return f.read()
        except Exception:
            raise CredentialFileError("Failed to read default credentials from file")
