
def get_number(prompt):
    """Read a valid number from the user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a number.")


def arithmetic():
    """Perform basic arithmetic."""
    print("\n--- Basic Arithmetic ---")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")

    while True:
        choice = input("Choose an operation (1-4): ")

        if choice in ("1", "2", "3", "4"):
            break
        print("Invalid choice! Enter a number from 1 to 4.")

    num1 = get_number("Enter the first number: ")
    num2 = get_number("Enter the second number: ")

    if choice == "1":
        result = num1 + num2
    elif choice == "2":
        result = num1 - num2
    elif choice == "3":
        result = num1 * num2
    elif choice == "4":
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
            return
        result = num1 / num2

    print("Result:", result)


def unit_conversion():
    """Convert units."""
    print("\n--- Unit Conversion ---")
    print("1. Kilometers to Miles")
    print("2. Celsius to Fahrenheit")

    while True:
        choice = input("Choose a conversion (1-2): ")

        if choice in ("1", "2"):
            break
        print("Invalid choice! Enter 1 or 2.")

    value = get_number("Enter the value to convert: ")

    if choice == "1":
        result = value * 0.621371
        print(f"{value} km = {result:.2f} miles")
    elif choice == "2":
        result = (value * 9 / 5) + 32
        print(f"{value}°C = {result:.2f}°F")


def main():
    """Display the main menu."""
    while True:
        print("\n===== Calculator and Unit Converter =====")
        print("1. Basic Arithmetic")
        print("2. Unit Conversion")
        print("3. Quit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            arithmetic()
        elif choice == "2":
            unit_conversion()
        elif choice == "3":
            print("Thank you for using the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
