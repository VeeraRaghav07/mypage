
import csv
import os
from datetime import datetime
from collections import defaultdict

CSV_FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]


def initialize_file():
    """Create the CSV file with headers if it does not exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()


def load_expenses():
    """Read and return all expenses from the CSV file."""
    initialize_file()
    expenses = []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                datetime.strptime(row["date"], "%Y-%m-%d")
                amount = float(row["amount"])
                if amount <= 0:
                    continue
                if not row["category"].strip():
                    continue

                expenses.append({
                    "date": row["date"],
                    "category": row["category"].strip(),
                    "description": row["description"].strip(),
                    "amount": amount
                })
            except (ValueError, TypeError, KeyError):
                print("Warning: Skipping an invalid row in the CSV file.")

    return expenses


def get_valid_date():
    """Ask for a date in YYYY-MM-DD format."""
    while True:
        date_text = input("Date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text
        except ValueError:
            print("Invalid date. Example: 2026-10-27")


def get_valid_amount():
    """Ask for a positive expense amount."""
    while True:
        try:
            amount = float(input("Amount: "))
            if amount > 0:
                return amount
            print("Amount must be greater than zero.")
        except ValueError:
            print("Enter a valid number, such as 250 or 99.50.")


def add_expense():
    """Collect an expense and append it to the CSV file."""
    print("\n--- Add Expense ---")
    date = get_valid_date()

    while True:
        category = input("Category (Food, Travel, Bills, etc.): ").strip()
        if category:
            break
        print("Category cannot be empty.")

    description = input("Description: ").strip()
    amount = get_valid_amount()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow({
            "date": date,
            "category": category.title(),
            "description": description,
            "amount": f"{amount:.2f}"
        })

    print("Expense saved successfully!")


def display_expenses(expenses):
    """Display a list of expenses."""
    if not expenses:
        print("No expenses found.")
        return

    print("\nDate       | Category     | Description          | Amount")
    print("-" * 66)

    for expense in expenses:
        print(
            f"{expense['date']} | "
            f"{expense['category']:<12} | "
            f"{expense['description']:<20} | "
            f"{expense['amount']:>9.2f}"
        )

    total = sum(expense["amount"] for expense in expenses)
    print("-" * 66)
    print(f"Total expenses: {total:.2f}")


def view_expenses():
    """View every recorded expense."""
    print("\n--- All Expenses ---")
    display_expenses(load_expenses())


def filter_expenses():
    """Filter expenses by category or date."""
    expenses = load_expenses()

    print("\n--- Filter Expenses ---")
    print("1. Filter by category")
    print("2. Filter by date")
    print("3. Filter by date range")

    choice = input("Choose a filter (1-3): ").strip()

    if choice == "1":
        category = input("Enter category: ").strip().casefold()
        results = [
            e for e in expenses
            if e["category"].casefold() == category
        ]
    elif choice == "2":
        date = get_valid_date()
        results = [e for e in expenses if e["date"] == date]
    elif choice == "3":
        start = get_valid_date()
        end = get_valid_date()

        if start > end:
            print("Start date must not be after end date.")
            return

        results = [
            e for e in expenses
            if start <= e["date"] <= end
        ]
    else:
        print("Invalid filter choice.")
        return

    display_expenses(results)


def category_summary():
    """Calculate totals and counts for each category."""
    expenses = load_expenses()

    if not expenses:
        print("No expenses available for summary.")
        return

    totals = defaultdict(float)
    counts = defaultdict(int)

    for expense in expenses:
        category = expense["category"]
        totals[category] += expense["amount"]
        counts[category] += 1

    print("\n--- Category Summary ---")
    print(f"{'Category':<18} {'Count':>6} {'Total':>12}")
    print("-" * 38)

    for category in sorted(totals):
        print(
            f"{category:<18} "
            f"{counts[category]:>6} "
            f"{totals[category]:>12.2f}"
        )

    print("-" * 38)
    print(f"{'Overall total':<18} {sum(totals.values()):>18.2f}")


def main():
    """Run the expense tracker menu."""
    initialize_file()

    while True:
        print("\n===== Personal Expense Tracker =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Category summary")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            print("Expenses saved. Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
