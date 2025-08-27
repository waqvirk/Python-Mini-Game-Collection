import random

def guessing_game():
    number = random.randint(1, 10)  # Random 1 to 10
    guess = None
    attempts = 0

    print("Welcome to the Guessing Game!")
    print("You have to guess a number between 1 to 10. Wanna try?!")

    # Solange geraten wird, wiederhole die Eingabe
    while guess != number:
        try:
            guess = int(input("Guess the number: "))
            attempts += 1

            if guess < number:
                print("Too low! Try again with a bigger number!")
            elif guess > number:
                print("Too high! Try again with a lower number!")
            else:
                print("="*55)
                print(f"✅ Correct! You won in {attempts} tries.\n")
                print(r"""
 __     ______  _    _   __          _______ _   _ 
 \ \   / / __ \| |  | |  \ \        / /_   _| \ | |
  \ \_/ / |  | | |  | |   \ \  /\  / /  | | |  \| |
   \   /| |  | | |  | |    \ \/  \/ /   | | | . ` |
    | | | |__| | |__| |     \  /\  /   _| |_| |\  |
    |_|  \____/ \____/       \/  \/   |_____|_| \_|
""")
                print("="*55)
        except ValueError:
            print("Error: Inavild number, try again a full number between 1 - 10")

if __name__ == "__main__":
    guessing_game()
