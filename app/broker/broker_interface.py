from abc import ABC, abstractmethod


class BrokerInterface(ABC):

    @abstractmethod
    def publish(self, topic: str, message: str) -> None:
        pass

    @abstractmethod
    def subscribe(self, topic: str):
        pass