class EventBus:

    _listeners = {}

    @classmethod
    def subscribe(
        cls,
        event_type,
        listener,
    ):

        if event_type not in cls._listeners:
            cls._listeners[event_type] = []

        cls._listeners[event_type].append(listener)

    @classmethod
    def dispatch(
        cls,
        event,
    ):

        listeners = cls._listeners.get(
            type(event),
            [],
        )

        for listener in listeners:
            listener.handle(event)