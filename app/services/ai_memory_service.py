from collections import defaultdict


class AIMemoryService:

    _history = defaultdict(list)

    # Acciones que están esperando confirmación del usuario
    _pending_actions = {}

    # Contexto estructurado de la conversación
    _context = defaultdict(dict)

    # Cantidad máxima de transacciones recientes
    _max_recent_transactions = 10

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

        return cls._history.get(
            session_id,
            [],
        )

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

        return cls._pending_actions.get(
            session_id
        )

    @classmethod
    def clear_pending_action(
        cls,
        session_id: str,
    ):

        cls._pending_actions.pop(
            session_id,
            None,
        )

    # ==========================================
    # CONTEXTO CONVERSACIONAL
    # ==========================================

    @classmethod
    def set_context(
        cls,
        session_id: str,
        key: str,
        value,
    ):

        cls._context[session_id][key] = value

    @classmethod
    def get_context(
        cls,
        session_id: str,
        key: str,
        default=None,
    ):

        return cls._context.get(
            session_id,
            {},
        ).get(
            key,
            default,
        )

    @classmethod
    def clear_context(
        cls,
        session_id: str,
    ):

        cls._context.pop(
            session_id,
            None,
        )

    # ==========================================
    # TRANSACCIONES RECIENTES
    # ==========================================

    @classmethod
    def add_recent_transaction(
        cls,
        session_id: str,
        transaction_id: int,
    ):

        recent_transactions = cls.get_context(
            session_id=session_id,
            key="recent_transaction_ids",
            default=[],
        )

        recent_transactions = list(
            recent_transactions
        )

        # Si ya existe, la movemos al inicio.
        if transaction_id in recent_transactions:

            recent_transactions.remove(
                transaction_id
            )

        # La transacción más recientemente utilizada
        # queda al comienzo de la lista.
        recent_transactions.insert(
            0,
            transaction_id,
        )

        recent_transactions = recent_transactions[
            :cls._max_recent_transactions
        ]

        cls.set_context(
            session_id=session_id,
            key="recent_transaction_ids",
            value=recent_transactions,
        )

        # La transacción pasa a ser también
        # el foco actual de la conversación.
        cls.set_context(
            session_id=session_id,
            key="last_transaction_id",
            value=transaction_id,
        )

    @classmethod
    def get_recent_transactions(
        cls,
        session_id: str,
    ):

        return cls.get_context(
            session_id=session_id,
            key="recent_transaction_ids",
            default=[],
        )

    # ==========================================
    # GRUPO ACTUAL DE TRANSACCIONES
    # ==========================================

    @classmethod
    def set_transaction_group(
        cls,
        session_id: str,
        transaction_ids: list[int],
    ):

        cls.set_context(
            session_id=session_id,
            key="current_transaction_group",
            value=list(transaction_ids),
        )

    @classmethod
    def get_transaction_group(
        cls,
        session_id: str,
    ):

        return cls.get_context(
            session_id=session_id,
            key="current_transaction_group",
            default=[],
        )

    @classmethod
    def clear_transaction_group(
        cls,
        session_id: str,
    ):

        context = cls._context.get(
            session_id,
            {},
        )

        context.pop(
            "current_transaction_group",
            None,
        )

    # ==========================================
    # RESOLVER REFERENCIAS DE TRANSACCIONES
    # ==========================================

    @classmethod
    def resolve_transaction_reference(
        cls,
        session_id: str,
        reference: str,
    ) -> int | None:

        if not reference:
            return None

        reference = reference.strip().lower()

        recent_transactions = list(
            cls.get_recent_transactions(
                session_id=session_id,
            )
        )

        transaction_group = list(
            cls.get_transaction_group(
                session_id=session_id,
            )
        )

        last_transaction_id = cls.get_context(
            session_id=session_id,
            key="last_transaction_id",
        )

        # ==========================================
        # CONTEXTO / ÚLTIMA TRANSACCIÓN
        # ==========================================

        if reference in [
            "contexto",
            "ultima",
            "última",
            "ultimo",
            "último",
        ]:

            return last_transaction_id

        # ==========================================
        # TRANSACCIÓN ANTERIOR
        # ==========================================

        if reference in [
            "anterior",
            "la anterior",
            "el anterior",
        ]:

            if len(recent_transactions) >= 2:

                return recent_transactions[1]

            return None

        # ==========================================
        # REFERENCIAS POSICIONALES
        # DEL GRUPO ACTUAL
        # ==========================================

        positional_references = {
            "primera": 1,
            "primero": 1,
            "la primera": 1,
            "el primero": 1,

            "segunda": 2,
            "segundo": 2,
            "la segunda": 2,
            "el segundo": 2,

            "tercera": 3,
            "tercero": 3,
            "la tercera": 3,
            "el tercero": 3,
        }

        position = positional_references.get(
            reference
        )

        if position is not None:

            index = position - 1

            if index < len(transaction_group):

                return transaction_group[index]

            return None

        # ==========================================
        # REFERENCIA NO RESUELTA
        # ==========================================

        return None

    # ==========================================
    # LIMPIAR MEMORIA COMPLETA
    # ==========================================

    @classmethod
    def clear(
        cls,
        session_id: str,
    ):

        cls._history.pop(
            session_id,
            None,
        )

        cls._pending_actions.pop(
            session_id,
            None,
        )

        cls._context.pop(
            session_id,
            None,
        )   