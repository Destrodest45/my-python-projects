import ast
import operator as op
import json
import os
import math
last_result = None

HISTORY_FILE = "shakur_history.json"

_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.FloorDiv: op.floordiv,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

def safe_eval(expr: str, last_result=None):

    if expr is None:
        raise ValueError("No expression provided")

    expr = expr.strip()
    if expr.lower() == "ans":
        if last_result is None:
            raise ValueError("No last result available (ans)")
        return last_result

    try:
            node = ast.parse(expr, mode="eval")
    except SyntaxError as e:
            raise ValueError(f"Syntax error: {e}")
    return _eval(node, last_result=last_result)
def _eval(node, last_result=None):

    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                op_type = type(node.op)
                if op_type in _ALLOWED_OPS:
                    return _ALLOWED_OPS[op_type](left, right)
                raise ValueError(f"Operator {op_type} not allowed")
    
    if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in _ALLOWED_OPS:
                return _ALLOWED_OPS[op_type](operand)
            raise ValueError(f"Unary operator {op_type} not allowed")

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")


    if isinstance(node, ast.Name):
            if node.id == "ans":
                if last_result is None:
                    raise ValueError("No last result available (ans)")
                return last_result
            raise ValueError(f"Use of name '{node.id}' is not allowed")
    
    raise ValueError(f"Unsupported expression element: {type(node)}")

class Calculator:
    def __init__(self):
        self.last_result = None

    def _store_and_format(self, result, message, update_last=True):
        if update_last and result is not None:
            self.last_result = result
        return result, message

    def add(self, a, b):
        return self._store_and_format(a + b, f"{a} + {b} = {a + b}")

    def subtract(self, a, b):
        return self._store_and_format(a - b, f"{a} - {b} = {a - b}")
    
    def multiply(self, a, b):
        return self._store_and_format(a * b, f"{a} * {b} = {a * b}")
    
    def divide(self, a, b):
        if b == 0:
            return None, "Cannot divide by zero."
        res = round(a / b, 2)
        return self._store_and_format(res, f"{a} / {b} = {res}")
    
    def modulus(self, a, b):
        if b == 0:
            return None, "Cannot perform modulus with zero."
        return self._store_and_format(a % b, f"{a} % {b} = {a % b}")

    def exponent(self, a, b):
        try:
            result = a ** b
            
            if abs(result) > 10**100:
                return None, f"{a} ** {b} = too large"
            return self._store_and_format(result, f"{a} ** {b} = {result}")
        except OverflowError:
            return None, f"{a} ** {b} = overflow error"
        except ValueError as e:
            return None, f"{a} ** {b} = error: {e}"    

    def check_even_odd(self, a, b):
        try:
            ea = "Even" if int(a) % 2 == 0 else "Odd"
            eb = "Even" if int(b) % 2 == 0 else "Odd"
            return None, f"{a} is {ea}, {b} is {eb}"
        except Exception as e:
            return None, f"Error checking even/odd: {e}"
        
    def percentage_of(self, a, b):
        try:
            result = (a / 100.0) * b
            return self._store_and_format(result, f"{a}% of {b} = {result}")
        except Exception as e:
            return None, f"Error computing percentage: {e}"
        
    def factorial(self, a):
        try:
            n = int(a)
            if n < 0:
                return None, "Factorial not defined for negative numbers"
            if n > 5000:
                return None, f"Factorial too large: {n}! (max: 5000)"
            result = math.factorial(n)
            return self._store_and_format(result, f"{n}! = {result}")
        except Exception as e:
            return None, f"Error computing factorial: {e}"    

    def base_convert(self, a, base):
        try:
            n = int(a)
            if base == 2:
                out = bin(n)
            elif base == 8:
                out = oct(n)
            elif base == 16:
                out = hex(n)
            else:
                return None, "Unsupported base"
            # keep numeric last_result unchanged for base conversions
            return None, f"{n} in base {base} = {out}"
        except Exception as e:
            return None, f"Error converting base: {e}"

class HistoryManager:
    def __init__(self, filename="shakur_history.json"):
        self.filename = filename
    
    def load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    return json.load(f)
            except Exception:
                return []
        return []
    
    def save_history(self, history):
        try:
            with open(self.filename, "w") as f:
                json.dump(history, f, indent=4)
        except Exception as e:
            print(f"Warning: failed to save history: {e}")

    def clear_history(self):
            try:
                with open(self.filename, "w") as f:
                    json.dump([], f)
            except Exception as e:
                print(f"Warning: failed to clear history: {e}")

def get_expression_input(prompt, last_result):
     while True:
        s = input(prompt).strip()
        if s.lower() == "q":
            return "back_to_menu"
        if s.lower() == "ans":
            if last_result is None:
                print("No previous result available.")
                continue
            print(f"Using last result: {last_result}")
            return last_result
        
        try:
            val = safe_eval(s, last_result=last_result)
            return val    
        except Exception as e:
            print(f"Invalid expression: {e}. Enter a number, expression, 'ans', or 'q'.")
        
def show_menu(autosave_enabled):
    print("\n--- Main Menu ---")
    print("1. Addition (a + b)")
    print("2. Subtraction (a - b)")
    print("3. Multiplication (a * b)")
    print("4. Division (a / b)")
    print("5. Modulus (a % b)")
    print("6. Exponentiation (a ** b)")
    print("7. Check Even/Odd (a, b)")
    print("8. Quit")
    print("9. View History")
    print("10. Clear History")
    print("11. Parse full expression (single input)")
    print("12. Percentage (a% of b)")
    print("13. Factorial (n!)")
    print("14. Number base converter")
    print(f"15. Toggle autosave (currently {'ON' if autosave_enabled else 'OFF'})")
    print("------------------")



def main():
    calc = Calculator()
    history = HistoryManager().load_history()
    history_manager = HistoryManager()
    autosave = True  # default ON as you wanted

    print("Welcome to Shakur's Upgraded Calculator!")

    while True:
        show_menu(autosave)
        choice = input("Enter your choice (1-15): ").strip()

        if choice == "8":  # Quit
            history_manager.save_history(history)
            print("History saved. Goodbye!")
            break

        if choice == "9":  # View history
            if not history:
                print("No history yet.")
            else:
                print("\nCalculation History:")
                for i, rec in enumerate(history, 1):
                    print(f"{i}. {rec}")
            continue

        if choice == "10":  # Clear history
            c = input("Clear history? (y/n): ").strip().lower()
            if c == "y":
                history = []
                history_manager.clear_history()
                print("History cleared.")
            else:
                print("Cancelled.")
            continue

        if choice == "15":  # Toggle autosave
            autosave = not autosave
            print(f"Autosave {'enabled' if autosave else 'disabled'}.")
            continue

        if choice not in [str(i) for i in range(1, 16)]:
            print("Invalid choice.")
            continue

        # Single-input expression option
        if choice == "11":
            val = get_expression_input("Enter expression (or 'ans'/'q'): ", calc.last_result)
            if val == "back_to_menu":
                continue
            message = f"Expression = {val}"
            print("Result:", message)
            history.append(message)
            calc.last_result = val 
            if autosave:
                history_manager.save_history(history)
            continue

        # Factorial (single operand)
        if choice == "13":
            n = get_expression_input("Enter integer n (or 'ans'/'q'): ", calc.last_result)
            if n == "back_to_menu":
                continue
            result, message = calc.factorial(n)
            print("Result:", message)
            history.append(message)
            if autosave:
                history_manager.save_history(history)
            continue

        # Percentage (a% of b)
        if choice == "12":
            a = get_expression_input("Enter percentage a (or 'ans'/'q'): ", calc.last_result)
            if a == "back_to_menu":
                continue
            b = get_expression_input("Enter value b (or 'ans'/'q'): ", calc.last_result)
            if b == "back_to_menu":
                continue
            result, message = calc.percentage_of(a, b)
            print("Result:", message)
            history.append(message)
            if autosave:
                history_manager.save_history(history)
            continue

        # Base converter
        if choice == "14":
            n = get_expression_input("Enter integer (or 'ans'/'q'): ", calc.last_result)
            if n == "back_to_menu":
                continue
            base_choice = input("Target base (2=binary, 8=octal, 16=hex): ").strip()
            try:
                base = int(base_choice)
            except ValueError:
                print("Invalid base selection.")
                continue
            result, message = calc.base_convert(n, base)
            print("Result:", message)
            history.append(message)
            if autosave:
                history_manager.save_history(history)
            continue

        a = get_expression_input("Enter first operand (or 'ans'/'q'): ", calc.last_result)
        if a == "back_to_menu":
            continue
        b = get_expression_input("Enter second operand (or 'ans'/'q'): ", calc.last_result)
        if b == "back_to_menu":
            continue    
    
        ops = {
            "1": calc.add,
            "2": calc.subtract,
            "3": calc.multiply,
            "4": calc.divide,
            "5": calc.modulus,
            "6": calc.exponent,
            "7": calc.check_even_odd,
        }
        func = ops.get(choice)
        result, message = func(a, b)
        print("Result:", message)
        history.append(message)
        if autosave:
            history_manager.save_history(history)

if __name__ == "__main__":
    main()