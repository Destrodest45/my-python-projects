class Calculator:
    def __init__(self):
        self.last_result = None

    def add(self, a, b):
        result = a + b
        self.last_result = result
        return result, f"{a} + {b} = {result}"

    def subtract(self, a, b):
        result = a - b
        self.last_result = result
        return result, f"{a} - {b} = {result}"

    def multiply(self, a, b):
        result = a * b
        self.last_result = result
        return result, f"{a} * {b} = {result}"

    def divide(self, a, b):
        if b == 0:
            return None, "Cannot divide by zero"
        result = round(a / b, 2)
        self.last_result = result
        return result, f"{a} / {b} = {result}"

    def modulus(self, a, b):
        if b == 0:
            return None, "Cannot perform modulus with zero"
        result = a % b
        self.last_result = result
        return result, f"{a} % {b} = {result}"

    def exponentiate(self, a, b):
        try:
            result = a ** b
            if abs(result) > 10**100:
                return None, f"{a} ** {b} = too large"
            self.last_result = result
            return result, f"{a} ** {b} = {result}"
        except OverflowError:
            return None, f"{a} ** {b} = overflow error"
        except ValueError as e:
            return None, f"{a} ** {b} = error: {e}"
        
    def even_odd_check(self, a, b):
        even_odd_a = "Even" if a % 2 == 0 else "Odd"
        even_odd_b = "Even" if b % 2 == 0 else "Odd"
        return None, f"{a} is {even_odd_a}, {b} is {even_odd_b}"

import json
import os
class HistoryManager:
    def __init__(self, filename="shakur_history.json"):
        self.filename = filename
    def load_history(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                return json.load(file)
        return []
    def save_history(self, history):
        with open(self.filename, "w") as file:
            json.dump(history, file, indent=4)
    def clear_history(self):
        with open(self.filename, "w") as file:
            json.dump([]. file)      
        
def get_number_input(prompt, last_result):
    while True:
        user_input = input(prompt)

        if user_input.lower() == "q":
            return "back_to_menu"
        if user_input.lower() == "ans":
            if last_result is None:
                print("No previous result, please input a number.")
                continue
            else:
                print(f"Using last_result = {last_result}")
                return last_result
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input, please enter a number, 'ans', or 'q' to go back.")
            continue

def show_menu():
    print("\nChoose an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Exponentiation")
    print("7. Even/Odd Check")
    print("8. Quit")
    print("9. View History")
    print("10. Clear History")   

def main():
    calc = Calculator()
    history_manager = HistoryManager()
    history = history_manager.load_history()
    print("Welcome to Shakur's Upgraded Calculator!")

    while True:
        show_menu()
        choice = input("Enter your choice (1-10): ")

        if choice == "8":
            history_manager.save_history(history)
            print("Exiting the calculator. Goodbye!")
            break
        elif choice == "9":
            if history:
                print("\nCalculation History:")
                for record in history:
                    print(record)
            else:
                print("No history available.")
            continue
        elif choice == "10":
            confirm = input("Are you sure you want to clear history? (y/n): ")
            if confirm.lower() in ['y', 'yes']:
                history_manager.clear_history()
            history = []
            print("History cleared.")
            continue

        a = get_number_input("Enter the first number (or 'ans' for last result, 'q' to go back): ", calc.last_result)
        if a == "back_to_menu":
            continue

        b = get_number_input("Enter the second number (or 'ans' for last result, 'q' to go back): ", calc.last_result)
        if b == "back_to_menu":
            continue

        operations = {
            "1": calc.add,
            "2": calc.subtract,
            "3": calc.multiply,
            "4": calc.divide,
            "5": calc.modulus,
            "6": calc.exponentiate,
            "7": calc.even_odd_check
        }
        operation_function = operations.get(choice)
        result, message = operation_function(a, b)

        print("Result:", message)
        history.append(message)

if __name__ == "__main__":
    main()