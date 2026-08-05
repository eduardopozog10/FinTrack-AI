from app.schemas.conversation_context import ConversationContext


class TemplateResponseService:

    @staticmethod
    def build(
        context: ConversationContext,
    ) -> str:

        data = context.data

        # ==========================================
        # GASTO CREADO
        # ==========================================

        if context.action == "expense_created":

            return (
                f"💸 ¡Listo! Registré un gasto de "
                f"${data.amount:,.0f} en "
                f"{data.description}.\n\n"
                f"Categoría: {data.category.capitalize()}."
            )

        # ==========================================
        # INGRESO CREADO
        # ==========================================

        if context.action == "income_created":

            return (
                f"💰 ¡Perfecto! Registré un ingreso de "
                f"${data.amount:,.0f} por "
                f"{data.description}."
            )

        # ==========================================
        # TRANSACCIÓN ACTUALIZADA
        # ==========================================

        if context.action == "transaction_updated":

            field = None

            if context.metadata:
                field = context.metadata.get("field")

            if field == "created_at":
                return "📅 Listo. Cambié la fecha de la transacción."

            if field == "amount":
                return (
                    f"💰 Listo. Actualicé el monto a "
                    f"${data.amount:,.0f}."
                )

            if field == "category":
                return (
                    f"🏷️ Listo. Cambié la categoría a "
                    f"{data.category.capitalize()}."
                )

            if field == "description":
                return (
                    f"✏️ Listo. Cambié la descripción a "
                    f"{data.description}."
                )

            return "✏️ La transacción fue actualizada correctamente."

        # ==========================================
        # TRANSACCIÓN ELIMINADA
        # ==========================================

        if context.action == "transaction_deleted":

            return (
                f"🗑️ Eliminé la transacción "
                f"{data.description} correctamente."
            )

        # ==========================================
        # BALANCE
        # ==========================================

        if context.action == "balance":

            return (
                f"💰 Balance actual\n\n"
                f"Ingresos: ${data['income']:,.0f}\n"
                f"Gastos: ${data['expense']:,.0f}\n"
                f"Saldo: ${data['balance']:,.0f}"
            )

        # ==========================================
        # PRESUPUESTO CREADO
        # ==========================================

        if context.action == "budget_created":

            return (
                f"🎯 Presupuesto creado para "
                f"{data.category.capitalize()} por "
                f"${data.amount:,.0f}."
            )

        # ==========================================
        # PRESUPUESTO ACTUALIZADO
        # ==========================================

        if context.action == "budget_updated":

            return (
                f"✏️ Presupuesto actualizado para "
                f"{data.category.capitalize()}.\n\n"
                f"Nuevo monto: ${data.amount:,.0f}."
            )

        # ==========================================
        # DEFAULT
        # ==========================================

        return "Operación realizada correctamente."