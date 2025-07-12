import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QListWidget, QMessageBox, QFileDialog
)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.check_login)
        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)
        self.success = False

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "admin" and password == "1234":
            self.success = True
            self.close()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials.")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transaction Management")
        self.transactions = []
        layout = QVBoxLayout()

        # Add transaction
        add_layout = QHBoxLayout()
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Transaction value")
        self.add_btn = QPushButton("Add Transaction")
        self.add_btn.clicked.connect(self.add_transaction)
        add_layout.addWidget(self.value_input)
        add_layout.addWidget(self.add_btn)
        layout.addLayout(add_layout)

        # Transactions list
        self.list_widget = QListWidget()
        layout.addWidget(QLabel("Transactions:"))
        layout.addWidget(self.list_widget)

        # Info
        self.info_label = QLabel("Total transactions: 0 | Sum: 0")
        layout.addWidget(self.info_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.relatory_btn = QPushButton("Generate Relatory")
        self.relatory_btn.clicked.connect(self.create_relatory)
        self.exit_btn = QPushButton("Exit")
        self.exit_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.relatory_btn)
        btn_layout.addWidget(self.exit_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def add_transaction(self):
        value = self.value_input.text()
        try:
            value_float = float(value)
            self.transactions.append(value_float)
            self.list_widget.addItem(str(value_float))
            self.update_info()
            self.value_input.clear()
            QMessageBox.information(self, "Success", "Transaction added!")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid number.")

    def update_info(self):
        total = sum(self.transactions)
        self.info_label.setText(
            f"Total transactions: {len(self.transactions)} | Sum: {total}"
        )

    def create_relatory(self):
        if not self.transactions:
            QMessageBox.warning(self, "Error", "No transactions to generate relatory.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save Relatory", "relatory.txt", "Text Files (*.txt)")
        if path:
            with open(path, "w") as file:
                file.write("Transactions:\n")
                file.write(f"Total transactions: {len(self.transactions)}\n")
                total = sum(self.transactions)
                for t in self.transactions:
                    file.write(f"- {t}\n")
                file.write(f"Sum of transactions: {total}\n")
            QMessageBox.information(self, "Success", "Relatory generated successfully!")

def main():
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    app.exec()
    if login.success:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    main()
