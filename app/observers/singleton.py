from app.observers.subject import Observer

ObserverMeta = type(Observer)

class SingletonMeta(ObserverMeta):
    _instances: dict[type, object] = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            ObserverMeta.__call__(cls, *args, **kwargs)
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    