import sqlite3
import pandas as pd

# Allowed categories
ALLOWED_CATEGORIES = ['Income', 'Food', 'Transport', 'Expense', 'Health', 'Other']

# Initialize database and create table
def initialize_database():
    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

# Add a transaction
def add_transaction(date, category, description, amount):
    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO transactions (date, category, description, amount)
    VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))

    conn.commit()
    conn.close()
    print("Transaction added successfully.")

# View all transactions
def view_transactions_with_index():
    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()

    print("\n--- Transaction List ---")
    for index, transaction in enumerate(transactions):
        print(f"{index + 1}: {transaction}")

    conn.close()
    return transactions

# Delete a transaction by ID
def delete_transaction(transactions):
    while True:
        try:
            transaction_index = int(input("Enter transaction index to delete: ")) - 1
            if 0 <= transaction_index < len(transactions):
                transaction_id = transactions[transaction_index][0]
                break
            else:
                print("Invalid index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()
    print("Transaction deleted successfully.")

# Update an existing transaction
def update_transaction(transactions):
    while True:
        try:
            transaction_index = int(input("Enter transaction index to update: ")) - 1
            if 0 <= transaction_index < len(transactions):
                transaction_id = transactions[transaction_index][0]
                break
            else:
                print("Invalid index. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    date = input("Enter new date (YYYY-MM-DD): ")
    category = get_valid_category()
    description = input("Enter new description: ")
    amount = get_valid_amount()

    # Update the transaction in the database

    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()

    cursor.execute('''
    UPDATE transactions
    SET date = ?, category = ?, description = ?, amount = ?
    WHERE id = ?
    ''', (date, category, description, amount, transaction_id))

    conn.commit()
    conn.close()
    print("Transaction updated successfully.")

# Generate summary report
def generate_report():
    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT category, SUM(amount) FROM transactions
    GROUP BY category
    ''')
    report = cursor.fetchall()

    total_income = 0
    total_expense = 0

    print("\n--- Category Report ---")
    for category, amount in report:
        print(f"{category}: ${amount:.2f}")
        if category == 'Income':
            total_income += amount
        else:
            total_expense += amount

    net_income = total_income - total_expense
    print("\n--- Summary ---")
    print(f"Total Income:  ${total_income:.2f}")
    print(f"Total Expenses: ${total_expense:.2f}")
    print(f"Net Income:     ${net_income:.2f}")

    conn.close()

# Input helpers
def get_valid_category():
    while True:
        category = input(f"Enter category ({', '.join(ALLOWED_CATEGORIES)}): ")
        if category in ALLOWED_CATEGORIES:
            return category
        print("Invalid category.")

def get_valid_amount():
    while True:
        try:
            return float(input("Enter amount: "))
        except ValueError:
            print("Invalid amount. Please enter a number.")

def export_to_excel(filename='transactions.xlsx'):
    conn = sqlite3.connect('bookkeeping.db')
    query = 'SELECT * FROM transactions'
    df = pd.read_sql_query(query, conn)
    conn.close()

    df.to_excel(filename, index=False)
    print(f"Data exported to {filename} successfully.")

# CLI Menu
def main():
    initialize_database()

    while True:
        print("\n=== Bookkeeping Menu ===")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Delete Transaction")
        print("4. Update Transaction")
        print("5. Generate Report")
        print("6. Export to Excel")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = get_valid_category()
            description = input("Enter description: ")
            amount = get_valid_amount()
            add_transaction(date, category, description, amount)

        elif choice == '2':
            view_transactions_with_index()

        elif choice == '3':
            transactions = view_transactions_with_index()
            if transactions:
                delete_transaction(transactions)

        elif choice == '4':
            transactions = view_transactions_with_index()
            if transactions:
                update_transaction(transactions)

        elif choice == '5':
            generate_report()

        elif choice == '6':
            export_to_excel()

        elif choice == '7':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
