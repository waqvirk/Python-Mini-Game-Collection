# Work off the platform in groups using the following code as a base

import random

# NUMBER GUESSING GAME
def number_guessing_game():
    pass




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

print("Game Over")
    


# TIC-TAC-TOE
# Function to print the board
def print_board(board):
    pass



# Function to check the winner
def check_winner(board):
    pass



# Function to run fo the actual tic-tac-toe game where your other functions will be used
def tic_tac_toe():
    pass

   

# MENU SYSTEM
# def main_menu(if_set_game_on):
#     if if_set_game_on != 1:
#         print("")
#         print("ME: Going outside, touching grass :-)")
#         print("")
#         return
    
#     print("")
#     print("Welcome to Python-Mini-Game Collection !!!")
#     print("")
#     print("1. Number guessing game")
#     print("")
#     print("2. Rock- paper- scissors")
#     print("")
#     print("3. Tic- Tac- Toe")
#     print("")
#     print("4. Exit program")
#     print("")
#     menu_selection = input("Please choose a game by entering the number and pressing 'enter' - have fun!")

#     if menu_selection.isdigit() != True:        #If entered value is not a number, print warning + return to main menu
#         print("###################################")
#         print("You need to enter a number, please.")
#         print("###################################")
#         main_menu()
    
    #game selection will call appropriate function to start the game:
    # if menu_selection == "1":
    #     number_guessing_game()
    # elif menu_selection == "2":
    #     rock_paper_scissors()
    # elif menu_selection == "3":
    #     tic_tac_toe()
    # elif menu_selection == "4":
    #     if_set_game_on = 0
    #     print("")
    #     print("AI says: Thank you for playing with us.")
    # else:
    #     print("Unexpected problem occured, returning to main menu.")
    
    # main_menu(if_set_game_on)

    
    
# RUN THE MENU

# if_set_game_on = 1
# main_menu(if_set_game_on)





