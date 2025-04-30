from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class Observer(ABC):
    @abstractmethod
    def update(self, db: Session, event: str, data: dict):
        pass

class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, db: Session, event: str, data: dict):
        for observer in self._observers:
            observer.update(db, event, data)

event_subject = Subject()
