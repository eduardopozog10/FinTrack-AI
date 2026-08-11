from collections import defaultdict


class AIMemoryService:

    _history = defaultdict(list)

    # Acciones que están esperando confirmación del usuario
    _pending_actions = {}

    # ==========================================
    # HISTORIAL
    # ==========================================

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

        # Conservar únicamente los últimos 10 mensajes
        cls._history[session_id] = cls._history[
            session_id
        ][-10:]

    @classmethod
    def get_history(
        cls,
        session_id: str,
    ):

        return cls._history.get(session_id, [])

    # ==========================================
    # ACCIONES PENDIENTES
    # ==========================================

    @classmethod
    def set_pending_action(
        cls,
        session_id: str,
        action: str,
        data: dict | None = None,
    ):

        cls._pending_actions[session_id] = {
            "action": action,
            "data": data or {},
        }

    @classmethod
    def get_pending_action(
        cls,
        session_id: str,
    ):

        return cls._pending_actions.get(session_id)

    @classmethod
    def clear_pending_action(
        cls,
        session_id: str,
    ):

        cls._pending_actions.pop(session_id, None)

    # ==========================================
    # LIMPIAR MEMORIA COMPLETA
    # ==========================================

    @classmethod
    def clear(
        cls,
        session_id: str,
    ):

        cls._history.pop(session_id, None)
        cls._pending_actions.pop(session_id, None)