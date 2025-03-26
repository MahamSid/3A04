from abc import ABC, abstractmethod

class Account(ABC):
    @abstractmethod
    def authenticate(self, loginID: str, password: str) -> bool:
        pass