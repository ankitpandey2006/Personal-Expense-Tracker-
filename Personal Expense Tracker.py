import json
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama (for Windows support)
init(autoreset=True)

class Expense:
    def __init__(self, amount, category, date=None):
        self.amount = amount
        self.category = category
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {"amount": self.amount, "category": self.category, "date": self.date}

class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = self.load_expenses()

    def load_expenses(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [Expense(**e) for e in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_expenses(self):
        with open(self.filename, "w") as f:
            json.dump([e.to_dict() for e in self.expenses], f, indent=2)

    def add_expense(self, amount, category, date=None):
        e = Expense(amount, category, date)
        self.expenses.append(e)
        self.save_expenses()
        print(Fore.GREEN + f"✅ Added expense: ₹{amount} for '{category}' on {e.date}")

    def show_summary(self):
        if not self.expenses:
            print(Fore.YELLOW + "No expenses recorded yet.")
            return
        summary = {}
        for e in self.expenses:
            summary[e.category] = summary.get(e.category, 0) + e.amount
        print(Fore.CYAN + "\n📊 Expense Summary:")
        for cat, amt in summary.items():
            print(f"  {cat}: ₹{amt}")

def welcome_banner():
    print("="*40)
    print(Fore.MAGENTA + "     💰 Personal Expense Tracker 💰")
    print(Fore.MAGENTA + "         Made with Python ❤️")
    print("="*40)

def goodbye_message():
    print(Fore.GREEN + "\n✅ Thank you for using the Expense Tracker!")
    print(Fore.YELLOW + "💡 Tip: Stay on top of your expenses, and keep coding! 💻\n")

def main():
    welcome_banner()
    tracker = ExpenseTracker()

    while True:
        print(Fore.BLUE + "\n📋 What would you like to do?")
        print("1️⃣  Add Expense")
        print("2️⃣  Show Summary")
        print("3️⃣  Exit")
        choice = input(Fore.WHITE + "Choose: ").strip()

        if choice == "1":
            try:
                amt = float(input("Amount: ₹").strip())
                if amt <= 0:
                    print(Fore.RED + "❌ Amount must be positive.")
                    continue
                cat = input("Category: ").strip().capitalize()
                if not cat:
                    print(Fore.RED + "❌ Category can't be empty.")
                    continue
                date = input("Date (YYYY-MM-DD) [Leave blank for today]: ").strip()
                if date:
                    try:
                        # Validate date format
                        datetime.strptime(date, "%Y-%m-%d")
                    except ValueError:
                        print(Fore.RED + "❌ Invalid date format. Use YYYY-MM-DD.")
                        continue
                else:
                    date = None

                tracker.add_expense(amt, cat, date)
            except ValueError:
                print(Fore.RED + "❌ Invalid amount. Please enter a number.")
        elif choice == "2":
            tracker.show_summary()
        elif choice == "3":
            goodbye_message()
            break
        else:
            print(Fore.RED + "❌ Invalid choice. Please select 1, 2 or 3.")

if __name__ == "__main__":
    main()
