import streamlit as st
import numpy as np
from datetime import date

# Define User and Transaction classes
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

    def calculate_savings_goal(self, goal):
        balance = self.user.income - self.get_total_expenses()
        return balance >= goal

    def expense_statistics(self):
        expenses = np.array([t.amount for t in self.transactions])
        return {
            'mean_expense': np.mean(expenses) if expenses.size > 0 else 0,
            'median_expense': np.median(expenses) if expenses.size > 0 else 0
        }

# Initialize session state for persistent data
if "tracker_initialized" not in st.session_state:
    st.session_state["tracker_initialized"] = False

# Header with logo and menu
def display_header():
    st.markdown(
        """
        <style>
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 1rem 0;
            }
            .menu {
                display: flex;
                gap: 1rem;
            }
            .menu a {
                color: #ffffff;
                text-decoration: none;
            }
            .menu a:hover {
                text-decoration: none;
            }
            .button-container {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }
        .button {
            padding: 0.5rem 1rem;
            font-size: 18px;
            color: #ffffff !important;
            background-color:#3e52d4;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            text-align: center;            
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #6c665a;
            color: #FFD700;
        }


        </style>
        <div class="header">
            <a href="https://imgbb.com/"><img src="https://i.ibb.co.com/tb4XCdx/logov2.png" alt="logov2" width="75" border="0"></a>
            <div class="button-container">
                <a href="/" class="button">Home</a>
                <a href="https://github.com/jubairsiyum/finance-tracker-python/" target="_blank" class="button">GitHub Repository</a>            
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Footer with submission information
def display_footer():
    st.markdown(
        """
        <hr>
        <div style="text-align: center;">
            <p><strong>Submitted to:</strong> Ms. Nasima Islam Bithi</p>
            <p><strong>Submitted by:</strong> Jubair Amin Siyum, SHAKIB., Mahir Labib</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    display_header()

    st.title("Personal Finance Tracker")

    # User input section
    if not st.session_state["tracker_initialized"]:
        name = st.text_input("Enter your name:")
        income = st.number_input("Enter your monthly income:", min_value=0.0)

        if name and income > 0:
            # Create User and FinanceTracker objects and store them in session state
            st.session_state.user = User(name, income)
            st.session_state.tracker = FinanceTracker(st.session_state.user)
            st.session_state["tracker_initialized"] = True
            st.success("User created successfully!")
        else:
            st.stop()
    else:
        st.write(f"Welcome back, {st.session_state.user.name}!")
        st.write(f"Your monthly income: ${st.session_state.user.income}")

    # Finance Tracker instance
    tracker = st.session_state.tracker

    st.header("Add a Transaction")
    amount = st.number_input("Enter the transaction amount:", min_value=0.0)
    category = st.text_input("Enter the transaction category:")
    transaction_date = st.date_input("Enter the transaction date:", value=date.today())

    if st.button("Add Transaction"):
        if amount > 0 and category:
            tracker.add_transaction(amount, category, transaction_date)
            st.success("Transaction added successfully!")
        else:
            st.warning("Please enter valid transaction details.")

    # Display Monthly Summary
    st.header("Monthly Summary")
    summary = tracker.generate_summary()
    st.write(f"**Income:** ${summary['income']}")
    st.write(f"**Total Expenses:** ${summary['total_expenses']}")
    st.write(f"**Balance:** ${summary['balance']}")

    # Show expenses by category
    st.subheader("Expense by Category")
    for cat, amt in summary['expense_by_category'].items():
        st.write(f"**{cat}:** ${amt}")

    # Set a savings goal
    st.header("Set Savings Goal")
    goal = st.number_input("Enter your savings goal:", min_value=0.0)
    if st.button("Check Savings Goal"):
        if tracker.calculate_savings_goal(goal):
            st.success("Congratulations! You have met your savings goal.")
        else:
            st.error("You have not met your savings goal.")

    # Display Expense Statistics
    st.header("Expense Statistics")
    stats = tracker.expense_statistics()
    st.write(f"**Mean Expense:** ${stats['mean_expense']:.2f}")
    st.write(f"**Median Expense:** ${stats['median_expense']:.2f}")

    display_footer()
    print("HELLO")

if __name__ == "__main__":
    main()


