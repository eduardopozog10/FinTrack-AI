from collections import defaultdict


class AIMemoryService:

    _history = defaultdict(list)

    @classmethod
    def add(
        cls,
        session_id: str,
        role: str,
        message: str,
    ):

        cls._history[session_id].append(
            {
                "role": role,
                "message": message,
            }
        )

        # conservar únicamente los últimos 10 mensajes
        cls._history[session_id] = cls._history[
            session_id
        ][-10:]


    @classmethod
    def get_history(
        cls,
        session_id: str,
    ):

        return cls._history.get(session_id, [])


    @classmethod
    def clear(
        cls,
        session_id: str,
    ):

        cls._history.pop(session_id, None)