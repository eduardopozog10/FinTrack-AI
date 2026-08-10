from app.constants.intents import Intent

from app.services.expense_service import ExpenseService
from app.services.income_service import IncomeService
from app.services.balance_service import BalanceService
from app.services.list_transactions_service import ListTransactionsService
from app.services.query_router import QueryRouter
from app.services.update_transaction_service import UpdateTransactionService
from app.services.delete_transaction_service import DeleteTransactionService
from app.services.budget_service import BudgetService
from app.services.budget_query_service import BudgetQueryService


COMMAND_HANDLERS = {
    Intent.EXPENSE: ExpenseService,
    Intent.INCOME: IncomeService,
    Intent.BALANCE: BalanceService,
    Intent.LIST: ListTransactionsService,
    Intent.QUERY: QueryRouter,
    Intent.UPDATE: UpdateTransactionService,
    Intent.DELETE: DeleteTransactionService,
    Intent.BUDGET: BudgetService,
    Intent.BUDGET_QUERY: BudgetQueryService,
}