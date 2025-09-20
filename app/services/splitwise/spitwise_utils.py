import logging
from os import getenv
from splitwise import Splitwise, Expense, Category
from ..invoice_processor.invoice import Invoice, InvoiceType


def create_expense(group_id: str, invoice: Invoice, file_path: str) -> Expense:
    if invoice.invoice_type == InvoiceType.UNSUPPORTED:
        logging.error("Failed to create expense - unsupported invoice type")
        return

    expense = Expense()
    category = Category()
    category.setId(invoice.invoice_type.value)
    
    expense.setGroupId(group_id)
    expense.setCategory(category)
    expense.setCost(str(invoice.cost))
    expense.setCurrencyCode("ILS")
    expense.setDescription(invoice.description)
    expense.setSplitEqually(True)
    expense.setReceipt(file_path)
    expense.setDetails(invoice.get_details())
    return expense


def post_expense(expense: Expense):
    s = Splitwise(
        consumer_key=getenv("SPLITWISE_CONSUMER_KEY"),
        consumer_secret=getenv("SPLITWISE_CONSUMER_SECRET"),
        api_key=getenv("SPLITWISE_API_KEY"),
    )
    try:
        nExpense, errors = s.createExpense(expense)
        if errors:
            logging.debug(errors.getErrors())
        else:
            logging.info(f"New expense created: {nExpense.getId()}")
        return nExpense.getId(), errors
    except Exception as e:
        logging.error(str(e), exc_info=True)
        raise e

