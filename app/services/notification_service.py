import json
from app.core.rabbit_manager import RabbitManager

class NotificationService:
    def __init__(self):
        self._manager = RabbitManager()

    def send_message(self, queue_name: str, payload: dict) -> None:
        message = json.dumps(payload)
        self._manager.publish(queue_name, message)

    def close(self) -> None:
        self._manager.close()

_notification_service: NotificationService | None = None
def get_notification_service() -> NotificationService:
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service
