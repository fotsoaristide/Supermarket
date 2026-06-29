class EventBus:
    """
    Lightweight pub/sub system for POS UI sync
    """

    def __init__(self):
        self.listeners = {}

    def subscribe(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def emit(self, event_name, data=None):
        if event_name not in self.listeners:
            return

        for callback in self.listeners[event_name]:
            try:
                callback(data)

            except Exception:
                pass