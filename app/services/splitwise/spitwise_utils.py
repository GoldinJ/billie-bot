from os import getenv
import logging
from splitwise import Splitwise, Expense, Category
from ..invoice_processor.invoice import Invoice

def create_expense(group_id: str, invoice: Invoice) -> Expense:
    expense = Expense()
    category = Category()
    category.setId(invoice.invoice_type.value)
    expense.setGroupId(group_id)
    expense.setCategory(category)
    expense.setCost(str(invoice.cost))
    expense.setCurrencyCode("ILS")
    expense.setDescription(invoice.description)
    expense.setSplitEqually(True)
    return expense

def post_expence(expense: Expense):
    s = Splitwise(
        consumer_key=getenv("SPLITWISE_CONSUMER_KEY"),
        consumer_secret=getenv("SPLITWISE_CONSUMER_SECRET"),
        api_key=getenv("SPLITWISE_API_KEY")
    )
    nExpense, errors = s.createExpense(expense)
    if errors:
        logging.debug(errors)
    else:
        logging.info(f"New expense created: {nExpense.getId()}")
    return nExpense.getId()

