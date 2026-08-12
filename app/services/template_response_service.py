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
                f"💸 Registré un gasto de "
                f"${data.amount:,.0f} en "
                f"{data.description}.\n"
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
                    "📊 Presupuesto\n"
                    f"${budget['spent']:,.0f} de "
                    f"${budget['budget']:,.0f} "
                    f"({budget['percentage']:.1f}%)\n"
                    f"Disponible: ${budget['remaining']:,.0f}"
                )

            # ======================================
            # ALERTA DEL PRESUPUESTO
            # ======================================

            if budget_alert:
                response += (
                    "\n"
                    f"{budget_alert['message']}"
                )

            return response

        # ==========================================
        # MÚLTIPLES GASTOS CREADOS
        # ==========================================

        if context.action == "expenses_created":

            if not data:
                return "No pude registrar los gastos."

            response = f"💸 Registré {len(data)} gastos:\n"

            for transaction in data:
                response += (
                    f"\n• ${transaction.amount:,.0f} · "
                    f"{transaction.description}"
                )

            total = sum(
                transaction.amount
                for transaction in data
            )

            response += (
                f"\n\nTotal: ${total:,.0f}"
            )

            return response

        # ==========================================
        # INGRESO CREADO
        # ==========================================

        if context.action == "income_created":

            return (
                f"💰 Registré un ingreso de "
                f"${data.amount:,.0f} por "
                f"{data.description}."
            )

        # ==========================================
        # TRANSACCIÓN ACTUALIZADA
        # ==========================================

        if context.action == "transaction_updated":

            if not context.success:
                return data["message"]

            field = None

            if context.metadata:
                field = context.metadata.get("field")

            if field == "created_at":
                return "📅 Listo. Cambié la fecha de la transacción."

            if field == "amount":
                return (
                    f"💰 Actualicé el monto a "
                    f"${data.amount:,.0f}."
                )

            if field == "category":
                return (
                    f"🏷️ Cambié la categoría a "
                    f"{data.category.capitalize()}."
                )

            if field == "description":
                return (
                    f"✏️ Cambié la descripción a "
                    f"{data.description}."
                )

            return "✏️ Transacción actualizada."

        # ==========================================
        # TRANSACCIÓN ELIMINADA
        # ==========================================

        if context.action == "transaction_deleted":

            if not context.success:
                return data["message"]

            return (
                f"🗑️ Eliminé la transacción "
                f"{data['description']}."
            )

        # ==========================================
        # CONFIRMAR ELIMINACIÓN DE TODOS LOS GASTOS
        # ==========================================

        if context.action == "delete_all_expenses_confirmation":

            if not context.success:
                return data["message"]

            count = data["count"]

            if count == 1:
                return (
                    "⚠️ ¿Seguro que quieres eliminar tu único gasto?\n"
                    "Responde Sí o No."
                )

            return (
                f"⚠️ ¿Seguro que quieres eliminar tus {count} gastos?\n"
                "Responde Sí o No."
            )

        # ==========================================
        # CONFIRMAR ELIMINACIÓN DE TODOS LOS PRESUPUESTOS
        # ==========================================

        if context.action == "delete_all_budgets_confirmation":

            if not context.success:
                return data["message"]

            count = data["count"]

            if count == 1:
                return (
                    "⚠️ ¿Seguro que quieres eliminar tu único presupuesto?\n"
                    "Responde Sí o No."
                )

            return (
                f"⚠️ ¿Seguro que quieres eliminar tus {count} presupuestos?\n"
                "Responde Sí o No."
            )

        # ==========================================
        # CONFIRMAR ELIMINACIÓN DE PRESUPUESTOS
        # ==========================================

        if context.action == "delete_all_budgets_confirmation":

            if not context.success:
                return data["message"]

            count = data["count"]

            if count == 1:
                return (
                    "⚠️ ¿Seguro que quieres eliminar tu único presupuesto?\n"
                    "Responde Sí o No."
                )

            return (
                f"⚠️ ¿Seguro que quieres eliminar tus {count} presupuestos?\n"
                "Responde Sí o No."
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

            if not context.success:
                return data["message"]

            return (
                f"🎯 Presupuesto de "
                f"{data.category.capitalize()} creado por "
                f"${data.amount:,.0f}."
            )

        # ==========================================
        # PRESUPUESTO ACTUALIZADO
        # ==========================================

        if context.action == "budget_updated":

            if not context.success:
                return data["message"]

            return (
                f"✏️ Presupuesto de "
                f"{data.category.capitalize()} actualizado a "
                f"${data.amount:,.0f}."
            )

        # ==========================================
        # PRESUPUESTO ELIMINADO
        # ==========================================

        if context.action == "budget_deleted":

            if not context.success:
                return data["message"]

            return (
                f"🗑️ Presupuesto de "
                f"{data['category'].capitalize()} eliminado."
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
        # ÚLTIMO GASTO
        # ==========================================

        if context.action == "last_expense":

            if not context.success:
                return data["message"]

            created_at = data["created_at"]

            return (
                "💸 Último gasto\n\n"
                f"📝 {data['description'].capitalize()}\n"
                f"💰 Monto: ${data['amount']:,.0f}\n"
                f"🏷️ Categoría: {data['category'].capitalize()}\n"
                f"📅 Fecha: {created_at.strftime('%d/%m/%Y · %H:%M')}"
            )

        # ==========================================
        # ÚLTIMO INGRESO
        # ==========================================

        if context.action == "last_income":

            if not context.success:
                return data["message"]

            created_at = data["created_at"]

            return (
                "💰 Último ingreso\n\n"
                f"📝 {data['description'].capitalize()}\n"
                f"💵 Monto: ${data['amount']:,.0f}\n"
                f"🏷️ Categoría: {data['category'].capitalize()}\n"
                f"📅 Fecha: {created_at.strftime('%d/%m/%Y · %H:%M')}"
            )

        # ==========================================
        # MAYOR GASTO
        # ==========================================

        if context.action == "max_expense":

            if not context.success:
                return data["message"]

            created_at = data["created_at"]

            return (
                "💸 Mayor gasto\n\n"
                f"📝 {data['description'].capitalize()}\n"
                f"💰 Monto: ${data['amount']:,.0f}\n"
                f"🏷️ Categoría: {data['category'].capitalize()}\n"
                f"📅 Fecha: {created_at.strftime('%d/%m/%Y · %H:%M')}"
            )

        # ==========================================
        # MAYOR INGRESO
        # ==========================================

        if context.action == "max_income":

            if not context.success:
                return data["message"]

            created_at = data["created_at"]

            return (
                "💰 Mayor ingreso\n\n"
                f"📝 {data['description'].capitalize()}\n"
                f"💵 Monto: ${data['amount']:,.0f}\n"
                f"🏷️ Categoría: {data['category'].capitalize()}\n"
                f"📅 Fecha: {created_at.strftime('%d/%m/%Y · %H:%M')}"
            )

        # ==========================================
        # HISTORIAL DE GASTOS
        # ==========================================

        if context.action == "expense_history":

            if not context.success:
                return data["message"]

            transactions = data["expense_history"]

            if not transactions:
                return "No tienes gastos registrados."

            response = "📋 Historial de gastos\n"

            for index, transaction in enumerate(
                transactions,
                start=1,
            ):

                created_at = transaction["created_at"]

                response += (
                    f"\n{index}. "
                    f"{transaction['description'].capitalize()}\n"
                    f"   💰 ${transaction['amount']:,.0f} · "
                    f"{transaction['category'].capitalize()}\n"
                    f"   📅 "
                    f"{created_at.strftime('%d/%m/%Y · %H:%M')}\n"
                )

            return response.strip()

        # ==========================================
        # NOMBRE DEL USUARIO ACTUALIZADO
        # ==========================================

        if context.action == "profile_name_updated":

            if not context.success:
                return data["message"]

            return (
                f"👤 ¡Listo! Desde ahora te llamaré "
                f"{data['full_name']}."
            )

        # ==========================================
        # DEFAULT
        # ==========================================

        return "Operación realizada correctamente."