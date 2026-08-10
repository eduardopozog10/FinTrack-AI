from datetime import date

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.transaction import Transaction
from app.schemas.operation_result import OperationResult


class UniversalQueryService:

    @staticmethod
    def process(
        session: Session,
        query_filter,
        user_id: int | None = None,
    ):

        filters = []

        # ----------------------------
        # Usuario
        # ----------------------------

        filters.append(
            Transaction.user_id == user_id,
        )

        # ----------------------------
        # Tipo de transacción
        # ----------------------------

        if query_filter.transaction_type:

            filters.append(
                Transaction.transaction_type == query_filter.transaction_type,
            )

        # ----------------------------
        # Categoría
        # ----------------------------

        if query_filter.category:

            filters.append(
                Transaction.category == query_filter.category,
            )

        # ----------------------------
        # Período
        # ----------------------------

        today = date.today()

        if query_filter.period == "TODAY":

            filters.append(
                func.date(Transaction.created_at) == today,
            )

        elif query_filter.period == "MONTH":

            filters.append(
                func.extract("year", Transaction.created_at) == today.year,
            )

            filters.append(
                func.extract("month", Transaction.created_at) == today.month,
            )

        # ----------------------------
        # Acciones
        # ----------------------------

        if query_filter.action in [
            "TODAY_EXPENSE",
            "MONTH_EXPENSE",
            "MONTH_INCOME",
            "TOTAL_EXPENSE",
            "TOTAL_INCOME",
        ]:

            total = session.exec(
                select(
                    func.sum(Transaction.amount)
                ).where(
                    *filters
                )
            ).one()

            key = {
                "TODAY_EXPENSE": "today_expense",
                "MONTH_EXPENSE": "month_expense",
                "MONTH_INCOME": "month_income",
                "TOTAL_EXPENSE": "total_expense",
                "TOTAL_INCOME": "total_income",
            }[query_filter.action]

            return OperationResult(
                success=True,
                action=key,
                data={
                    key: total or 0,
                },
            )

        # ----------------------------
        # Máximos
        # ----------------------------

        if query_filter.action in [
            "MAX_EXPENSE",
            "MAX_INCOME",
        ]:

            transaction = session.exec(
                select(Transaction)
                .where(*filters)
                .order_by(
                    Transaction.amount.desc(),
                )
            ).first()

            if transaction is None:

                message = {
                    "MAX_EXPENSE": "No existen gastos registrados.",
                    "MAX_INCOME": "No existen ingresos registrados.",
                }[query_filter.action]

                return {
                    "message": message,
                }

            key = {
                "MAX_EXPENSE": "max_expense",
                "MAX_INCOME": "max_income",
            }[query_filter.action]

            return {
                key: {
                    "description": transaction.description,
                    "amount": transaction.amount,
                    "category": transaction.category,
                }
            }

        # ----------------------------
        # Últimos movimientos
        # ----------------------------

        if query_filter.action in [
            "LAST_EXPENSE",
            "LAST_INCOME",
        ]:

            transaction = session.exec(
                select(Transaction)
                .where(*filters)
                .order_by(
                    Transaction.created_at.desc(),
                )
            ).first()

            if transaction is None:

                message = {
                    "LAST_EXPENSE": "No existen gastos registrados.",
                    "LAST_INCOME": "No existen ingresos registrados.",
                }[query_filter.action]

                return {
                    "message": message,
                }

            key = {
                "LAST_EXPENSE": "last_expense",
                "LAST_INCOME": "last_income",
            }[query_filter.action]

            return {
                key: {
                    "description": transaction.description,
                    "amount": transaction.amount,
                    "category": transaction.category,
                }
            }

        # ----------------------------
        # Historial de gastos
        # ----------------------------

        if query_filter.action == "EXPENSE_HISTORY":

            transactions = session.exec(
                select(Transaction)
                .where(*filters)
                .order_by(Transaction.created_at.desc())
            ).all()

            return {
                "expense_history": [
                    {
                        "description": transaction.description,
                        "amount": transaction.amount,
                        "category": transaction.category,
                        "created_at": transaction.created_at,
                    }
                    for transaction in transactions
                ]
            }

        return {
            "message": "Acción aún no implementada.",
            "action": query_filter.action,
        }