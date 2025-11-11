import json
import os

HISTORY_FILE = "shakur_history.json"
last_result = None


def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


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



def perform_operation(choice, a, b):
    if choice == "1":
        return a + b, f"{a} + {b} = {a + b}"
    elif choice == "2":
        return a - b, f"{a} - {b} = {a - b}"
    elif choice == "3":
        return a * b, f"{a} * {b} = {a * b}"
    elif choice == "4":
        if b != 0:
            result = round(a / b, 2)
            return result, f"{a} / {b} = {result}"
        else:
            return None, "Cannot divide by zero."
    elif choice == "5":
        if b != 0:
            return a % b, f"{a} % {b} = {a % b}"
        else:
            return None, "Cannot perform modulus with zero."
    elif choice == "6":
        try:
            result = a ** b
            if abs(result) > 10**100:
                return None, f"{a} ** {b} = too large"
            else:
                return result, f"{a} ** {b} = {result}"
        except OverflowError:
            return None, f"{a} ** {b} = overflow error"
        except ValueError as e:
            return None, f"{a} ** {b} = error: {e}"
    elif choice == "7":
        even_odd_a = "Even" if a % 2 == 0 else "Odd"
        even_odd_b = "Even" if b % 2 == 0 else "Odd"
        return None, f"{a} is {even_odd_a}, {b} is {even_odd_b}"



def show_menu():
    print("\nChoose an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Exponentiation")
    print("7. Check Even/Odd")
    print("8. Quit")
    print("9. View History")
    print("10. Clear History")


def main():
    global last_result
    history = load_history()
    print("Welcome to Shakur's Calculator (Modular Edition)")

    while True:
        show_menu()
        choice = input("Enter your choice (1–10): ")

        if choice == "8":
            save_history(history)
            print("History saved. Goodbye and have a good day!")
            break

        if choice == "9":
            if not history:
                print("No calculations yet.")
            else:
                print("\nCalculation History:")
                for i, record in enumerate(history, 1):
                    print(f"{i}. {record}")
            continue

        if choice == "10":
            if not history:
                print("No existing calculations to erase.")
            else:
                confirm = input("Are you sure you want to clear all history? (y/n): ")
                if confirm.lower() in ["y", "yes"]:
                    history = []
                    print("History cleared!")
                else:
                    print("Operation cancelled.")
            continue

        if choice not in [str(i) for i in range(1, 11)]:
            print("Invalid option! Please select a valid option.")
            continue

        a = get_number_input("Enter first number (or 'q'/'ans'): ", last_result)
        if a == "back_to_menu":
            continue
        b = get_number_input("Enter second number (or 'q'/'ans'): ", last_result)
        if b == "back_to_menu":
            continue

        result, message = perform_operation(choice, a, b)
        print("Result:", message)
        history.append(message)
        if result is not None:
            last_result = result


if __name__ == "__main__":
    main()
