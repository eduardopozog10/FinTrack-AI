from datetime import date

from sqlalchemy import func
from sqlmodel import Session, select

from app.models.transaction import Transaction


class UniversalQueryService:

    @staticmethod
    def process(
        session: Session,
        query_filter,
    ):

        filters = []

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

            return {
                key: total or 0,
            }

        return {
            "message": "Acción aún no implementada.",
            "action": query_filter.action,
        }