from os import getenv
from splitwise import Splitwise, Expense

def create_expense(group_id: str, data: dict) -> Expense:
    s = Splitwise(getenv("SPLITWISE_CONSUMER_KEY"), getenv("SPLITWISE_CONSUMER_SECRET"))
    # Example: Create 

