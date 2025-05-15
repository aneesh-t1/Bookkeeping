import sqlite3

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
def view_transactions():
    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()

    print("\n--- Transaction List ---")
    for transaction in transactions:
        print(transaction)

    conn.close()

# Delete a transaction by ID
def delete_transaction(transaction_id):
    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
    conn.commit()
    conn.close()
    print("🗑️ Transaction deleted successfully.")

# Update an existing transaction
def update_transaction(transaction_id, date, category, description, amount):
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
        print("6. Exit")

        choice = input("Enter your choice (1–6): ").strip()

        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = get_valid_category()
            description = input("Enter description: ")
            amount = get_valid_amount()
            add_transaction(date, category, description, amount)

        elif choice == '2':
            view_transactions()

        elif choice == '3':
            try:
                transaction_id = int(input("Enter transaction ID to delete: "))
                delete_transaction(transaction_id)
            except ValueError:
                print("Invalid ID.")

        elif choice == '4':
            try:
                transaction_id = int(input("Enter transaction ID to update: "))
                date = input("Enter new date (YYYY-MM-DD): ")
                category = get_valid_category()
                description = input("Enter new description: ")
                amount = get_valid_amount()
                update_transaction(transaction_id, date, category, description, amount)
            except ValueError:
                print("Invalid input.")

        elif choice == '5':
            generate_report()

        elif choice == '6':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
