class BudgetAlertListener:

    @staticmethod
    def handle(event):

        if event.metadata is None:
            return

        budget = event.metadata.get("budget")

        if budget is None:
            return

        percentage = budget.get("percentage")

        if percentage is None:
            return

        alert = None

        if percentage > 100:
            alert = {
                "level": "exceeded",
                "message": (
                    "🚨 Has superado tu presupuesto para esta categoría."
                ),
            }

        elif percentage == 100:
            alert = {
                "level": "limit_reached",
                "message": (
                    "🚨 Has utilizado el 100% de tu presupuesto."
                ),
            }

        elif percentage >= 80:
            alert = {
                "level": "warning",
                "message": (
                    f"⚠️ Ya utilizaste el "
                    f"{percentage:.1f}% de tu presupuesto."
                ),
            }

        elif percentage >= 50:
            alert = {
                "level": "notice",
                "message": (
                    f"💡 Ya utilizaste el "
                    f"{percentage:.1f}% de tu presupuesto."
                ),
            }

        if alert is not None:
            event.metadata["budget_alert"] = alert