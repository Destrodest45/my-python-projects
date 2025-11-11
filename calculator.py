print("Shakur's Calculator")

history = []
last_result = None

def get_number_input(prompt):
    while True:
        user_input = input(prompt)

        if user_input.lower() == 'q':
            return 'back_to_menu'
        if user_input.lower() == 'ans':
            if last_result is None:
                print("No previous result, please input a number.")
                continue
            else:
                print(f"Using last_result = {last_result}")
                return last_result
        try:
            return float(user_input)
        except ValueError:
            print("Invalid input, please enter a number,'ans', or 'q'to go back")
            continue


while True:
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
    print("10. Clear history")

    choice = input("Enter your choice (1-10): ")

    if choice == '8':
        print("Exiting Shakur's calculator. Goodbye and have a good day!")
        break
    if choice not in ['1','2','3','4','5','6','7','8','9','10']:
        print("Invalid option! please select a valid option.")
        continue
    if choice == '9':
        if len(history) == 0:
            print("No calculations yet.")
        else:
            print("\n Calculation History:")
            for i, record in enumerate(history, 1):
                print(f"{i}. {record}")
        continue

    if choice == '10':
        if len(history) == 0:
            print("No Existing Calculations to be erased")
        else:
            confirm = input("Are you sure you want to clear all history? (y/n): ")
            if confirm.lower() in ['y','yes']:
                history = []
                print("History Cleared!")
            else:
                print("Operation Cancelled")
        continue

    a_input = get_number_input("Enter first number (or 'q' to go back , 'ans'for last result): ")
    if a_input == 'back_to_menu':
        continue

    b_input = get_number_input("Enter second number(or 'q' to go back,'ans'for last result): ")
    if b_input == 'back_to_menu':
        continue


    try:
        a = a_input
        b = b_input

        if choice == '1':
            result = a + b
            print("Result:", result)
            history.append(f"{a} + {b} = {result}")
            last_result = result
        elif choice == '2':
            result = a - b
            print("Result:", result)
            history.append(f"{a} - {b} = {result}")
            last_result = result
        elif choice == '3':
            result = a * b
            print("Result:", result)
            history.append(f"{a} * {b} = {result}")
            last_result = result
        elif choice == '4':
            if b != 0:
                result = round(a / b, 2)
                print("Result:", result)
                history.append(f"{a} / {b} = {result}")
                last_result = result
            else:
                print("Cannot divide by zero. ")
        elif choice == '5':
            if b != 0:
                result = a % b
                print("Result:", result)
                history.append(f"{a} % {b} = {result}")
                last_result = result
            else:
                print("Cannot perform modulus with zero. ")
        elif choice == '6':

            try:
                result = a ** b
                if abs(result) > 10 ** 100:
                    print(f"Exponentiation: {a}**{b} = too large to display")
                    history.append(f"{a} ** {b} = too large")
                else:
                    result = a ** b
                    print("Result:", result)
                    history.append(f"{a} ** {b} = {result}")
                    last_result = result
            except OverflowError:
                print(f"Result: {a}**{b} = result too large (overflow)")
                history.append(f"{a} ** {b} = overflow error")
            except ValueError as e:
                print(f"Exponentiation error: {e}")
                history.append(f"{a} ** {b} = error: {e}")
        elif choice == '7':
            print(f"{a} is Even" if a % 2 == 0 else f"{a} is odd")
            print(f"{b} is Even" if b % 2 == 0 else f"{b} is Odd")
            history.append(f"Even/Odd: {a}(a_even_odd), {b}(b_even_odd)")
    except ValueError:
        print("Invalid input! please enter numbers only.")
