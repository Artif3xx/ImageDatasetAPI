"""
This file contains the hash tools for the api.
"""

from __future__ import annotations
import hashlib


class HashTools:
    __sha256_hash: str = None

    def __init__(self, filepath: str):
        self.filepath = filepath

    def __hash_image(self):
        with open(self.filepath, "rb") as f:
            image_bytes = f.read()  # read entire file as bytes
            self.__sha256_hash = hashlib.sha256(image_bytes).hexdigest()

    def get_hash(self):
        if self.__sha256_hash is None:
            self.__hash_image()
        return self.__sha256_hash
