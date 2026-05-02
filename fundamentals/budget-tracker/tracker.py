import json

def print_menu():
        print("=== Budget Tracker ===")
        print("1. Add transaction")
        print("2. Show all transactions")
        print("3. Show balance")
        print("4. Quit")

def add_transaction():
    try:
        with open("budget.json", "r") as f:
            transactions = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        transactions = []

    while True:
        try:
            description = input("Spending type: ")
            amount = float(input("Amount: "))
            break
        except(ValueError):
            print("Amount has to be a number")

    while True:
        spending_type = input("income or expense: ")
        if spending_type in ['income', 'expense']:
            break
        print("Has to be 'income' or 'expense'!")

    transactions_dict = {
        "description": description,
        "amount": amount,
        "spending_type": spending_type
    }


    transactions.append(transactions_dict)

    with open("budget.json", "w") as f:
        json.dump(transactions, f)

def show_transactions():
    try:
        with open("budget.json", "r") as f:
            transactions = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        transactions = []
    
    if not transactions:
        print("no transactions found!")
    else:
        for i, transaction in enumerate(transactions):
            print(f"{i+1}. {transaction['description']}, {transaction['amount']} - {transaction['spending_type']}")

def calculate_budget():
    try:
        with open("budget.json", "r") as f:
            transactions = json.load(f)
    except(FileNotFoundError, json.JSONDecodeError):
        transactions = []

    total_income = 0
    total_expense = 0

    for t in transactions:
        if t['spending_type'] == 'income':
            total_income += t['amount']
        elif t['spending_type'] == 'expense':
            total_expense += t['amount']

    budget = total_income - total_expense

    print(f"Balance: {budget:.2f}")

user_input = ''

while user_input != '4':
    print_menu()
    user_input = input("Choose: ")
    if user_input == '1':
        add_transaction()
    elif user_input == '2':
        show_transactions()
    elif user_input == '3':
        calculate_budget()
    elif user_input == '4':
        print('Quitting...')
    else:
        print("not a valid option! - try again")
