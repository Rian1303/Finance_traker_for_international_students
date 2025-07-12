def login():
    username = input("Username: ")
    password = input("Password: ")
    return username == "admin" and password == "1234"

def add_transaction(transactions):
    while True:
        value = input("Enter transaction value: ")
        try:
            value_float = float(value)
            transactions.append(value_float)
            print("Transaction added!")
        except ValueError:
            print("Please enter a valid number.")
            continue
        continuation = input("Do you want to continue? (yes/no): ").strip().lower()
        if continuation == "no":
            break
#this is function for add new trasactions

def view_transactions(transactions):
    if transactions:
        print("Transactions:")
        print(f"Total transactions: {len(transactions)}")
        total = sum(transactions)
        for t in transactions:
            print("-", t)
        print(f"Sum of transactions: {total}")
    else:
        print("No transactions.")
#and this is for view trasactions and sum
def create_relatory(transactions):
    if transactions:
        with open("relatory.txt", "w") as file:
            file.write("Transactions:\n")
            file.write(f"Total transactions: {len(transactions)}\n")
            total = sum(transactions)
            for t in transactions:
                file.write(f"- {t}\n")
            file.write(f"Sum of transactions: {total}\n")
    else:
        print("No transactions to generate relatory.")
#this function is for create relatory, .txt 

def main():
    transactions = []
    print("Login")
    if not login():
        print("Login failed.")
        return
    print("Login successful!")
    while True:
        print("\nMenu:")
        print("1. Add New Transaction")
        print("2. View Transactions")
        print("3. Generate Relatory")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            add_transaction(transactions)
        elif choice == "2":
            view_transactions(transactions)
        elif choice == "3":
            if transactions:
                create_relatory(transactions)
                print("Relatory generated successfully!")
            else:
                print("No transactions to generate relatory.")
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
# This code implements a simple transaction management system with login functionality.4

