import sqlite3

conn = sqlite3.connect('bookkeeping.db')
cursor = conn.cursor()

# Create a table for storing transactions
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    date TEXT,
    category TEXT,
    description TEXT,
    amount REAL
    
)
''')

conn.commit()
conn.close()

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

def view_transactions():
    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM transactions
    ''')
    
    transactions = cursor.fetchall()
    
    for transaction in transactions:
        print(transaction)
    
    conn.close()

def delete_transaction(transaction_id):
    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM transactions WHERE id = ?
    ''', (transaction_id,))
    
    conn.commit()
    conn.close()
    print("Transaction deleted successfully.")

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

def generate_report():
    conn = sqlite3.connect('bookkeeping.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT category, SUM(amount) FROM transactions
    GROUP BY category
    ''')
    
    report = cursor.fetchall()
    
    for row in report:
        print(f"Category: {row[0]}, Total Amount: {row[1]}")
    
    conn.close()

def main():
    while True:
        print("\nBookkeeping System")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Delete Transaction")
        print("4. Update Transaction")
        print("5. Generate Report")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            description = input("Enter description: ")
            amount = float(input("Enter amount: "))
            add_transaction(date, category, description, amount)
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            transaction_id = int(input("Enter transaction ID to delete: "))
            delete_transaction(transaction_id)
        elif choice == '4':
            transaction_id = int(input("Enter transaction ID to update: "))
            date = input("Enter new date (YYYY-MM-DD): ")
            category = input("Enter new category: ")
            description = input("Enter new description: ")
            amount = float(input("Enter new amount: "))
            update_transaction(transaction_id, date, category, description, amount)
        elif choice == '5':
            generate_report()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

