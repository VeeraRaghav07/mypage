
import random
import re
from collections import Counter


def number_guessing_game():
    """Play a number guessing game with a score."""
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    score = 100

    print("\n=== Number Guessing Game ===")
    print("Guess the number between 1 and 100.")
    print(f"You have {max_attempts} attempts.")
    print("You start with 100 points.")

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a valid whole number.")
            continue

        if not 1 <= guess <= 100:
            print("Enter a number between 1 and 100.")
            continue

        attempts += 1

        if guess == secret_number:
            print(f"Correct! The number was {secret_number}.")
            print(f"Attempts used: {attempts}")
            print(f"Your final score: {score}")
            return

        score -= 10

        if guess < secret_number:
            print("Too low!")
        else:
            print("Too high!")

        print(f"Attempts remaining: {max_attempts - attempts}")

    print(f"\nGame over! The number was {secret_number}.")
    print("Your final score: 0")


def analyze_word_frequency():
    """Read a text file and display the most common words."""
    print("\n=== Word Frequency Analyzer ===")
    filename = input("Enter the text file path: ").strip()
    filename = filename.strip('"').strip("'")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print("Error: File not found.")
        return
    except (PermissionError, IsADirectoryError, UnicodeError, OSError) as error:
        print(f"Could not read the file: {error}")
        return

    words = re.findall(r"\b[\w']+\b", text.lower())
    word_counts = Counter(words)

    if not word_counts:
        print("The file is empty or contains no words.")
        return

    try:
        limit = int(input("How many top words should be shown? "))
        if limit < 1:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Please enter a valid whole number.")
        return

    print(f"\nTotal words: {len(words)}")
    print(f"Unique words: {len(word_counts)}")
    print("\nMost common words:")

    sorted_words = sorted(
        word_counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    for word, count in sorted_words[:limit]:
        print(f"{word}: {count}")


def main():
    """Display the main menu."""
    while True:
        print("\n===== Python Mini Tools =====")
        print("1. Number Guessing Game")
        print("2. Word Frequency Analyzer")
        print("3. Quit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            number_guessing_game()
        elif choice == "2":
            analyze_word_frequency()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
