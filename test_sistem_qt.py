import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QComboBox, QTableWidget, QTableWidgetItem,
    QTextEdit, QFileDialog
)
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt

TRANSACTION_TYPES = [
    "Income", "Expense", "Transfer", "Investment", "Loan", "Other"
]

def save_to_json(transactions, filename="transactions.json"):
    with open(filename, "w") as f:
        json.dump(transactions, f, indent=4)

def load_from_json(filename="transactions.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QVBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.check_login)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.user_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.pass_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)
        self.success = False

    def check_login(self):
        if self.user_input.text() == "admin" and self.pass_input.text() == "1234":
            self.success = True
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password.")

class FinanceTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Tracker")
        self.transactions = load_from_json()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Add Transaction Section
        add_layout = QHBoxLayout()
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Transaction Value")
        self.type_combo = QComboBox()
        self.type_combo.addItems(TRANSACTION_TYPES)
        self.add_btn = QPushButton("Add Transaction")
        self.add_btn.clicked.connect(self.add_transaction)
        add_layout.addWidget(self.value_input)
        add_layout.addWidget(self.type_combo)
        add_layout.addWidget(self.add_btn)
        layout.addLayout(add_layout)

        # Transactions Table
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Value", "Type"])
        layout.addWidget(self.table)
        self.refresh_table()

        # Filter Section
        filter_layout = QHBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(TRANSACTION_TYPES)
        self.filter_btn = QPushButton("Filter")
        self.filter_btn.clicked.connect(self.filter_transactions)
        filter_layout.addWidget(QLabel("Filter by Type:"))
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addWidget(self.filter_btn)
        layout.addLayout(filter_layout)

        # Relatory Section
        self.relatory_btn = QPushButton("Generate Relatory")
        self.relatory_btn.clicked.connect(self.generate_relatory)
        layout.addWidget(self.relatory_btn)

        # Chart Section
        self.chart_btn = QPushButton("Show Transaction Type Chart")
        self.chart_btn.clicked.connect(self.show_chart)
        layout.addWidget(self.chart_btn)

        # Save Section
        self.save_btn = QPushButton("Save Transactions to JSON")
        self.save_btn.clicked.connect(self.save_transactions)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def add_transaction(self):
        value = self.value_input.text()
        try:
            value_float = float(value)
            trans_type = self.type_combo.currentText()
            self.transactions.append({"value": value_float, "type": trans_type})
            self.refresh_table()
            self.value_input.clear()
            QMessageBox.information(self, "Success", f"Transaction added as {trans_type}!")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid number.")

    def refresh_table(self, filtered=None):
        data = filtered if filtered is not None else self.transactions
        self.table.setRowCount(len(data))
        for row, t in enumerate(data):
            self.table.setItem(row, 0, QTableWidgetItem(str(t["value"])))
            self.table.setItem(row, 1, QTableWidgetItem(t["type"]))

    def filter_transactions(self):
        t_type = self.filter_combo.currentText()
        filtered = [t for t in self.transactions if t["type"] == t_type]
        self.refresh_table(filtered)

    def generate_relatory(self):
        if not self.transactions:
            QMessageBox.information(self, "Info", "No transactions to generate relatory.")
            return
        fname, _ = QFileDialog.getSaveFileName(self, "Save Relatory", "relatory.txt", "Text Files (*.txt)")
        if fname:
            with open(fname, "w") as file:
                file.write("Transactions:\n")
                file.write(f"Total transactions: {len(self.transactions)}\n")
                total = sum(t["value"] for t in self.transactions)
                for t in self.transactions:
                    file.write(f"- {t['value']} ({t['type']})\n")
                file.write(f"Sum of transaction values: {total}\n")
            QMessageBox.information(self, "Success", "Relatory generated successfully!")

    def show_chart(self):
        if not self.transactions:
            QMessageBox.information(self, "Info", "No transactions to plot.")
            return
        type_counts = {}
        for t in self.transactions:
            t_type = t["type"]
            type_counts[t_type] = type_counts.get(t_type, 0) + 1
        labels = list(type_counts.keys())
        sizes = list(type_counts.values())
        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.title("Transaction Type Distribution")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

    def save_transactions(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Save Transactions", "transactions.json", "JSON Files (*.json)")
        if fname:
            save_to_json(self.transactions, fname)
            QMessageBox.information(self, "Success", "Transactions saved to JSON file.")

def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    app.exec()
    if login.success:
        window = FinanceTracker()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
