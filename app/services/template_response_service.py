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

            response = (
                f"💸 ¡Listo! Registré un gasto de "
                f"${data.amount:,.0f} en "
                f"{data.description}.\n\n"
                f"Categoría: {data.category.capitalize()}."
            )

            budget = None
            budget_alert = None

            if context.metadata:
                budget = context.metadata.get("budget")
                budget_alert = context.metadata.get("budget_alert")

            # ======================================
            # ESTADO DEL PRESUPUESTO
            # ======================================

            if budget:

                response += (
                    "\n\n"
                    "📊 Presupuesto\n\n"
                    f"Utilizado: ${budget['spent']:,.0f} de "
                    f"${budget['budget']:,.0f} "
                    f"({budget['percentage']:.1f}%)\n"
                    f"Disponible: ${budget['remaining']:,.0f}"
                )

            # ======================================
            # ALERTA DEL PRESUPUESTO
            # ======================================

            if budget_alert:

                response += (
                    "\n\n"
                    f"{budget_alert['message']}"
                )

            return response

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

            if not context.success:
                return data["message"]

            return (
                f"🗑️ Eliminé la transacción "
                f"{data['description']} correctamente."
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
        # CONSULTAR PRESUPUESTO
        # ==========================================

        if context.action == "budget_status":

            if not context.success:
                return data["message"]

            response = (
                f"📊 Presupuesto de "
                f"{data['category'].capitalize()}\n\n"
                f"Presupuesto: ${data['budget']:,.0f}\n"
                f"Utilizado: ${data['spent']:,.0f}\n"
                f"Disponible: ${data['remaining']:,.0f}\n"
                f"Progreso: {data['percentage']:.1f}%"
            )

            if data["exceeded"]:
                response += (
                    "\n\n"
                    f"🚨 Has superado tu presupuesto por "
                    f"${abs(data['remaining']):,.0f}."
                )

            elif data["percentage"] == 100:
                response += (
                    "\n\n"
                    "🚨 Has utilizado el 100% de tu presupuesto."
                )

            elif data["percentage"] >= 80:
                response += (
                    "\n\n"
                    f"⚠️ Ya utilizaste el "
                    f"{data['percentage']:.1f}% de tu presupuesto."
                )

            elif data["percentage"] >= 50:
                response += (
                    "\n\n"
                    f"💡 Ya utilizaste el "
                    f"{data['percentage']:.1f}% de tu presupuesto."
                )

            return response

        # ==========================================
        # CONSULTAR TODOS LOS PRESUPUESTOS
        # ==========================================

        if context.action == "budget_status_all":

            if not context.success:
                return data["message"]

            response = "📊 Tus presupuestos\n"

            for budget in data:

                response += (
                    "\n"
                    f"{budget['category'].capitalize()}\n"
                    f"${budget['spent']:,.0f} de "
                    f"${budget['budget']:,.0f} "
                    f"({budget['percentage']:.1f}%)\n"
                    f"Disponible: ${budget['remaining']:,.0f}\n"
                )

                if budget["exceeded"]:
                    response += "🚨 Presupuesto superado\n"

            return response.strip()

        # ==========================================
        # GASTOS DE HOY
        # ==========================================

        if context.action == "today_expense":

            return (
                f"💸 Hoy has gastado "
                f"${data['today_expense']:,.0f}."
            )

        # ==========================================
        # GASTOS DEL MES
        # ==========================================

        if context.action == "month_expense":

            return (
                f"💸 Este mes has gastado "
                f"${data['month_expense']:,.0f}."
            )

        # ==========================================
        # INGRESOS DEL MES
        # ==========================================

        if context.action == "month_income":

            return (
                f"💰 Este mes has recibido "
                f"${data['month_income']:,.0f}."
            )

        # ==========================================
        # DEFAULT
        # ==========================================

        return "Operación realizada correctamente."