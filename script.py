# Work off the platform in groups using the following code as a base

# NUMBER GUESSING GAME
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



# PAPER, ROCK, SCISSORS
print("Welcome to Rock Paper Scissors")
def get_player_choice():
    choice = input("Enter rock, paper, or scissors: ").lower()
    while choice not in ["rock", "paper", "scissors", "x"]:
        choice = input("Invalid choice! Please type rock, paper or scissors (x to quit): ").lower()
    return choice

def get_computer_choice():
    return random.choice(["rock", "paper", "scissors"])


def rock_paper_scissors(player, computer):
    if player == computer:
        return "draw"
    elif (player == "rock" and computer == "scissors") or \
         (player == "scissors" and computer == "paper") or \
         (player == "paper" and computer == "rock"):
        return "player"
    else:
        return "computer"
    
# Initialize scores
player_score = 0
computer_score = 0

# Game loop
while True:
    player_move = get_player_choice()
    if player_move == "x":
        print("Exiting the game...")
        break

    computer_move = get_computer_choice()
    print(f"\nYou chose: {player_move}")
    print(f"Computer chose: {computer_move}")

    winner = rock_paper_scissors(player_move, computer_move)

    if winner == "player":
        print("You win this round!")
        player_score += 1
    elif winner == "computer":
        print("Computer wins this round!")
        computer_score += 1
    else:
        print("it's a draw")

    print(f"Score --> You: {player_score} | Computer: {computer_score}")
    print("\n---\n")

print("Game over!")

# TIC-TAC-TOE
# Function to print the board
def print_board(board):
        if board == 0:   #pre-fill fields for first initial board draw, for player to understand
            global field_list
            field_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]    #field_list[1-9] == 1-9
        #use index 0 for playing and if win condition set, change to 1!
        global current_player    
        if board >= 1:
            symbol = "O" if current_player == "player2" else "X"        #apply value to field_list index, consider player1 or 2 is active (X/O!)
            #change field list index to symbol according to 'board'-value, check if already exist, use counter 'i' globally
            global i    #no.  of current turn
            if field_list[board] == " ":    #check if board is empty
                field_list[board] = symbol   #mark symbol (pre-selected X/O) to given board no.

            #draw board setup:
        v1 = f'| {field_list[1]}  | {field_list[2]}  | {field_list[3]}  |'
        v2 = f'| {field_list[4]}  | {field_list[5]}  | {field_list[6]}  |'
        v3 = f'| {field_list[7]}  | {field_list[8]}  | {field_list[9]}  |'
        h = f' ____ ____ ____ '

        for i in range(1,8):
            if i == 2:
                print(v1)
            elif i == 4:
                print(v2)
            elif i == 6:
                print(v3)
            else:
                print(h)
     

# Function to check the winner
def check_winner(current_player, field_list):
    pass


# Function to run fo the actual tic-tac-toe game where your other functions will be used
def tic_tac_toe(stay_in_game):
    if stay_in_game != 1:
        return
    print("")
    print("3. Tic- Tac- Toe")
    print("To play you can type '6' for example for 2nd row and 3rd column when it's your turn.")
    print("Player no.1 begins and takes turns with player no.2. Player no.1 please begin.")    
    print("")
    while stay_in_game == 1:
        print_board(board=0) #initial board draw filled numbers 1-9 to display
        print("")
        global field_list
        field_list = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]     #reset working list before playing 9 turns
        global i
        for i in range(1,10,1):          #grid 3x3 equals 9 possible moves; does not include wrong moves!
            #end range should be increase for proper gameplay,   check 9 fields + 3 rows for end/winning conditions
            global current_player
            current_player = "player2" if i %2 == 0 else "player1"
            print(f"It's the turn of: {current_player} - choose a field (1-9).")
            try:

                if current_player == "player1":
                 player1_input = int(input("Player 1, you use 'X' - make your choice: "))
                    #check if variable INT or errors out on letters here later
                 print_board(board=player1_input)
                elif current_player == "player2":
                    player2_input = int(input("Player 2, you use 'O' - make your choice: "))
                    #print(type(player2_input))
                    print_board(board=player2_input)
                else:
                    print("Error detected, check program code.")
            
                check_winner(current_player, field_list)
            except:
                ValueError

            #check_win_condition as 9 rounds of gameplay will lead here, set variable stay_in_game to 0 to exit or leave to replay


# MENU SYSTEM
def main_menu(if_set_game_on):
    if if_set_game_on != 1:
        print("")
        print("ME: Going outside, touching grass :-)")
        print("")
        return
    
    print("")
    print("Welcome to Python-Mini-Game Collection !!!")
    print("")
    print("1. Number guessing game")
    print("")
    print("2. Rock- paper- scissors")
    print("")
    print("3. Tic- Tac- Toe")
    print("")
    print("4. Exit program")
    print("")
    menu_selection = input("Please choose a game by entering the number and pressing 'enter' - have fun!")

    if menu_selection.isdigit() != True:        #If entered value is not a number, print warning + return to main menu
        print("###################################")
        print("You need to enter a number, please.")
        print("###################################")
        main_menu()
    
    #game selection will call appropriate function to start the game:
    if menu_selection == "1":
        number_guessing_game()
    elif menu_selection == "2":
        rock_paper_scissors()
    elif menu_selection == "3":
        tic_tac_toe(stay_in_game=1)
    elif menu_selection == "4":
        if_set_game_on = 0
        print("")
        print("AI says: Thank you for playing with us.")
    else:
        print("Unexpected problem occured, returning to main menu.")
    
    main_menu(if_set_game_on)

    
# RUN THE MENU
if_set_game_on = 1          #used to run main menu, if 0 will pass through and exit
main_menu(if_set_game_on)
