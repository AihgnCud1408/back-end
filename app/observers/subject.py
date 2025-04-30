from sqlalchemy.orm import Session

class Observer:
    def update(self, event: str, data: dict):
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

    def notify(self, event: str, data: dict):
        for observer in self._observers:
            observer.update(event, data)

event_subject = Subject()
