import streamlit as st
from datetime import datetime
import numpy as np

class User:
    def __init__(self, name, income):
        self.name = name
        self.income = income

class Transaction:
    def __init__(self, amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

class FinanceTracker:
    def __init__(self, user):
        self.user = user
        self.transactions = []
        self.categories = {}

    def add_transaction(self, amount, category, date):
        transaction = Transaction(amount, category, date)
        self.transactions.append(transaction)
        if category in self.categories:
            self.categories[category] += amount
        else:
            self.categories[category] = amount

    def get_total_expenses(self):
        return sum([t.amount for t in self.transactions])

    def get_expense_by_category(self):
        return self.categories

    def generate_summary(self):
        total_expenses = self.get_total_expenses()
        balance = self.user.income - total_expenses
        return {
            'income': self.user.income,
            'total_expenses': total_expenses,
            'balance': balance,
            'expense_by_category': self.get_expense_by_category()
        }

# Streamlit UI
st.title("Finance Tracker")

# Input user income
user_name = st.text_input("Enter your name", "John Doe")
user_income = st.number_input("Enter your monthly income", value=3000.0)
user = User(user_name, user_income)
tracker = FinanceTracker(user)

st.header("Add Transaction")
amount = st.number_input("Transaction Amount")
category = st.text_input("Transaction Category")
date = st.text_input("Transaction Date (DD-MM-YYYY)", "01-01-2023")

if st.button("Add Transaction"):
    try:
        datetime.strptime(date, '%d-%m-%Y')
        tracker.add_transaction(amount, category, date)
        st.success("Transaction added successfully!")
    except ValueError:
        st.error("Invalid date format. Use DD-MM-YYYY.")

if st.button("Show Summary"):
    summary = tracker.generate_summary()
    st.write(f"Income: ${summary['income']}")
    st.write(f"Total Expenses: ${summary['total_expenses']}")
    st.write(f"Balance: ${summary['balance']}")
    st.write("Expense by Category:")
    for cat, amt in summary['expense_by_category'].items():
        st.write(f"{cat}: ${amt}")
