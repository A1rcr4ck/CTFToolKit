from abc import ABC, abstractmethod


class Cipher(ABC):
    @abstractmethod
    def encode(self, data: str) -> str:
        pass

    @abstractmethod
    def decode(self, data: str) -> str:
        pass