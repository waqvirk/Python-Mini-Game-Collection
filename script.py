# --- Optional color support ---

try:
    from colorama import Fore, Back, Style, init as colorama_init
    colorama_init(autoreset=True)
    COLOR_ENABLED = True
except Exception:
    # colorama not installed → define no-op stand-ins
    COLOR_ENABLED = False
    class _NoColor:
        def __getattr__(self, _):  # Fore.LIGHTMAGENTA_EX → ""
            return ""
    Fore = Back = Style = _NoColor()
    def colorama_init(*args, **kwargs):  # keep API shape if you call it elsewhere
        pass


# Number Game1

import random
import time
import shutil

# Number game colors
P      = Fore.LIGHTMAGENTA_EX + Style.BRIGHT
P_DIM  = Fore.LIGHTMAGENTA_EX
OK     = Fore.LIGHTGREEN_EX + Style.BRIGHT
WARN   = Fore.LIGHTYELLOW_EX + Style.BRIGHT
ERR    = Fore.LIGHTRED_EX + Style.BRIGHT
INFO   = Fore.LIGHTCYAN_EX
TEXT   = Fore.LIGHTWHITE_EX

# ====== Helpers ======
def typewriter(text, delay=0.02):
    """Print text with a typewriter effect (no newline)."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    # caller controls newline

def draw_banner():
    title = "NUMBER GUESSING ARENA"
    w = max(len(title) + 12, 42)
    top = "╔" + "═" * (w - 2) + "╗"
    sep = "╠" + "═" * (w - 2) + "╣"
    bot = "╚" + "═" * (w - 2) + "╝"
    line = "║" + " " * (w - 2) + "║"

    print(P + top)
    print(P + line)
    center = f"███   {title}   ███"
    print(P + "║" + center.center(w - 2) + "║")
    print(P + line)
    print(P + sep)
    msg1 = "Guess a number between 1–100."
    msg2 = "Type 'x' to quit anytime."
    print(P + "║" + msg1.ljust(w - 2) + "║")
    print(P + "║" + msg2.ljust(w - 2) + "║")
    print(P + bot)

def loading_sequence(steps=10):
    """Intro loading: typewriter header + 10-step progress bar (magenta)."""
    typewriter(P + "Initializing range ", 0.018)
    typewriter(P + "1–100", 0.03)
    print()
    typewriter(P + "Loading game assets", 0.018)
    print()
    bar_w = 30
    for i in range(steps):
        filled = int(bar_w * (i + 1) / steps)
        bar = P + "[" + "#" * filled + "-" * (bar_w - filled) + "]"
        pct = int((i + 1) / steps * 100)
        print(f"{bar} {pct}%", end="\r", flush=True)
        time.sleep(0.08)
    print()
    print()

def clamp_guess(g, lo, hi):
    if g < lo:
        return lo
    if g > hi:
        return hi
    return g

def draw_ruler(lo, hi, last=None, global_lo=1, global_hi=100, width=40):
    """
    Draw a ruler showing current valid range within the global 1..100.
    Marks last guess with '^' (if given).
    """
    width = max(20, width)
    span = global_hi - global_lo

    def pos(val):
        if span == 0:
            return 0
        return int((val - global_lo) / span * (width - 1))

    lo_i = pos(lo)
    hi_i = pos(hi)
    line = ["·"] * width  # faint baseline
    for i in range(lo_i, hi_i + 1):
        line[i] = "—"
    line[lo_i] = "|"
    line[hi_i] = "|"

    pointer_line = [" "] * width
    label = ""
    if last is not None and global_lo <= last <= global_hi:
        li = pos(last)
        pointer_line[li] = "^"
        label = f"  last: {last}"

    print(P + f"Range: [{global_lo}" + "".join(line) + f"{global_hi}]")
    print(P + "       " + "".join(pointer_line) + (TEXT + label if label else ""))

def print_history(history):
    """
    history: list of dicts with keys: try, guess, result
    """
    if not history:
        return
    try_w = max(3, len("Try"))
    guess_w = max(5, len("Guess"))
    result_w = max(6, max(len(h["result"]) for h in history))

    print(P + "┌" + "─"*(try_w+2) + "┬" + "─"*(guess_w+2) + "┬" + "─"*(result_w+2) + "┐")
    print(P + "│ " + "Try".ljust(try_w) + " │ " + "Guess".ljust(guess_w) + " │ " + "Result".ljust(result_w) + " │")
    print(P + "├" + "─"*(try_w+2) + "┼" + "─"*(guess_w+2) + "┼" + "─"*(result_w+2) + "┤")
    for h in history:
        res = h["result"]
        if   res == "correct": color = OK
        elif res == "high":    color = WARN
        elif res == "low":     color = INFO
        else:                  color = TEXT
        print(
            P + "│ " + str(h["try"]).ljust(try_w) +
            " │ " + str(h["guess"]).ljust(guess_w) +
            " │ " + color + res.ljust(result_w) + P + " │"
        )
    print(P + "└" + "─"*(try_w+2) + "┴" + "─"*(guess_w+2) + "┴" + "─"*(result_w+2) + "┘")

def terminal_width():
    try:
        return shutil.get_terminal_size(fallback=(80, 20)).columns
    except Exception:
        return 80
    
# ====== Game ======

def number_guessing_game():
    GLOBAL_LO, GLOBAL_HI = 1, 100

    while True:  # replay loop
        number = random.randint(GLOBAL_LO, GLOBAL_HI)
        lo, hi = GLOBAL_LO, GLOBAL_HI
        guess = None
        attempts = 0
        history = []

        print()
        draw_banner()
        loading_sequence(steps=10)

        print(P + "Make your guess! (enter a number 1–100, or 'x' to quit)\n")

        # guessing loop
        while guess != number:
            # show ruler before each guess
            draw_ruler(lo, hi, last=guess, global_lo=GLOBAL_LO, global_hi=GLOBAL_HI, width=min(60, terminal_width()-20))
            if history:
                print_history(history)
            user_in = input("\nGuess: ").strip()
            if user_in.lower() == "x":
                print("\nExiting the game...")
                return

            try:
                guess = int(user_in)
            except ValueError:
                print(ERR + "❌ Invalid input! Please enter a number 1–100 (or x to quit).")
                continue

            if not (GLOBAL_LO <= guess <= GLOBAL_HI):
                print(WARN + "⚠️  Out of bounds. Stay within 1–100.")
                continue

            attempts += 1

            if guess < number:
                result = "low"
                history.append({"try": attempts, "guess": guess, "result": result})
                lo = max(lo, guess + 1)
                print(INFO + "Too low! Try again with a bigger number!")
            elif guess > number:
                result = "high"
                history.append({"try": attempts, "guess": guess, "result": result})
                hi = min(hi, guess - 1)
                print(INFO + "Too high! Try again with a lower number!")
            else:
                result = "correct"
                history.append({"try": attempts, "guess": guess, "result": result})
                print("\n" + P + "=" * 60)
                print(f"✅ Correct! You won in {attempts} tries.\n")
                print(r"""
 __     ______  _    _   __          _______ _   _ 
 \ \   / / __ \| |  | |  \ \        / /_   _| \ | |
  \ \_/ / |  | | |  | |   \ \  /\  / /  | | |  \| |
   \   /| |  | | |  | |    \ \/  \/ /   | | | . ` |
    | | | |__| | |__| |     \  /\  /   _| |_| |\  |
    |_|  \____/ \____/       \/  \/   |_____|_| \_|
""")
                print(P + "=" * 60)
                print_history(history)
                break

        # replay?
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing! 👋")
            return


# PAPER, ROCK, SCISSORS
def get_player_choice():
    choice = input(Fore.LIGHTWHITE_EX + "Enter rock, paper, or scissors: ").lower()
    while choice not in ["rock", "paper", "scissors", "x"]:
        choice = input(Fore.LIGHTRED_EX + "❌ Invalid choice! Please type rock, paper or scissors (x to quit): ").lower()
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
def play_rps():
    print(Fore.LIGHTYELLOW_EX + "Welcome to Rock Paper Scissors ✊✋✌️")
    print(Fore.LIGHTRED_EX + "Type 'x' to quit anytime")
    player_score = 0
    computer_score = 0

# Game loop
    while True:
        player_move = get_player_choice()
        if player_move == "x":
            print(Fore.LIGHTBLUE_EX + "Exiting the game...")
            break

        computer_move = get_computer_choice()
        print(Fore.LIGHTBLUE_EX + f"\n👤 You chose: {player_move}")
        print(Fore.LIGHTCYAN_EX + f"🤖 Computer chose: {computer_move}")

        winner = rock_paper_scissors(player_move, computer_move)

        if winner == "player":
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "👤 You win this round!")
            player_score += 1
        elif winner == "computer":
            print(Fore.LIGHTRED_EX + Style.BRIGHT + "🤖 Computer wins this round!")
            computer_score += 1
        else:
            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "🤝 It's a draw")

        print(Fore.LIGHTWHITE_EX + Style.BRIGHT + f"🎮 Score --> 👤 : {player_score} | 🤖 : {computer_score}")
        print(Fore.LIGHTBLUE_EX + "\n---\n")

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
    
    symbol = "O" if current_player == "player2" else "X"
    
    winning_combinations = [
        [1, 2, 3],       
        [4, 5, 6],
        [7, 8, 9],
        [1, 4, 7],
        [2, 5, 8],
        [3, 6, 9],
        [1, 5, 9],
        [3, 5, 7],
    ]

    for a, b, c in winning_combinations:
        if field_list[a] == field_list[b] == field_list[c] == symbol:
            return current_player
    
    if all(cell != " " for cell in field_list[1:10]):
        return "Draw"
    
    return None


# Function to run fo the actual tic-tac-toe game where your other functions will be used
def tic_tac_toe(stay_in_game):
    if stay_in_game != 1:
        return
    print("")
    print(Fore.LIGHTGREEN_EX + "3. Tic- Tac- Toe")
    print(Fore.LIGHTGREEN_EX + "To play you can type '6' for example for 2nd row and 3rd column when it's your turn.")
    print(Fore.LIGHTGREEN_EX + "Player no.1 begins and takes turns with player no.2. Player no.1 please begin.")    
    print("")
    while True:
        print_board(board=0) #initial board draw filled numbers 1-9 to display
        print("")
        global field_list
        field_list = [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "]     #reset working list before playing 9 turns
        global i
        for i in range(1,10,1):          #grid 3x3 equals 9 possible moves; does not include wrong moves!
            #end range should be increase for proper gameplay,   check 9 fields + 3 rows for end/winning conditions
            global current_player
            current_player = "player2" if i %2 == 0 else "player1"
            print(Fore.LIGHTGREEN_EX + f"It's the turn of: {current_player} - choose a field (1-9).")
            try:

                if current_player == "player1":
                    player1_input = int(input(Fore.LIGHTRED_EX + "Player 1, you use 'X' - make your choice: "))
                    #check if variable INT or errors out on letters here later
                    print_board(board=player1_input)
                elif current_player == "player2":
                    player2_input = int(input(Fore.LIGHTCYAN_EX + "Player 2, you use 'O' - make your choice: "))
                    #print(type(player2_input))
                    print_board(board=player2_input)
                else:
                    print("Error detected, check program code.")
            
                result = check_winner(current_player, field_list)
                if result:
                    if result == "Draw":
                        print(Fore.LIGHTGREEN_EX + "it's a draw!")
                    else:
                        print (Fore.LIGHTGREEN_EX + f"{result} wins!")
                    break
            except:
                ValueError
        # --- Ask to play again or return to menu ---
        choice = input(Fore.LIGHTGREEN_EX + "Play again? (y = yes, m = main menu): ").strip().lower()
        if choice == "y":
            continue
        elif choice == "m":
            return
        else:
            print(Fore.LIGHTGREEN_EX + "Invalid choice, returning to main menu.")
            return

            #check_win_condition as 9 rounds of gameplay will lead here, set variable stay_in_game to 0 to exit or leave to replay


# MENU SYSTEM
def main_menu(if_set_game_on):
    if if_set_game_on != 1:
        print("")
        print(Fore.LIGHTGREEN_EX + "ME: Going outside, touching grass :-)")
        print("")
        return
    
    print("")
    print("")
    print("")
    print(Fore.LIGHTWHITE_EX + "Welcome to Python-Mini-Game Collection !!!")
    print("")
    print(Fore.LIGHTMAGENTA_EX + "1. Number guessing game")
    print("")
    print(Fore.LIGHTYELLOW_EX + "2. Rock- paper- scissors")
    print("")
    print(Fore.LIGHTGREEN_EX + "3. Tic- Tac- Toe")
    print("")
    print(Fore.LIGHTCYAN_EX + "4. Exit program")
    print("")
    menu_selection = input(Fore.LIGHTWHITE_EX + "Please choose a game by entering the number and pressing 'enter' - have fun! ")

    if menu_selection.isdigit() != True:        #If entered value is not a number, print warning + return to main menu
        print(Fore.LIGHTWHITE_EX + "###################################")
        print(Fore.LIGHTWHITE_EX + "You need to enter a number, please.")
        print(Fore.LIGHTWHITE_EX + "###################################")
        main_menu(if_set_game_on)
    
    #game selection will call appropriate function to start the game:
    if menu_selection == "1":
        number_guessing_game()
    elif menu_selection == "2":
        play_rps()
    elif menu_selection == "3":
        tic_tac_toe(stay_in_game=1)
    elif menu_selection == "4":
        if_set_game_on = 0
        print("")
        print(
    Fore.LIGHTYELLOW_EX + r"""
                          \   |   /
                            .-*-.
                         ‒ (  ☀  ) ‒
                            `-*-'
                          /   |   \ 
""" +
    Fore.GREEN + r"""
            /\          /\                    /\          /\
           /  \        /  \                  /  \        /  \
          /^^^^\      /^^^^\                /^^^^\      /^^^^\
     ____/^^^^^^\____/^^^^^^\______________/^^^^^^\____/^^^^^^\____
    /                                                              \ 
""" +
    Fore.MAGENTA + 
r"""   |   ✿  ✿        ~ ~ ~  ~  ~   ~ ~ ~   ~  ~  ~ ~ ~        ✿  ✿   |
   |   ✿       ~  ~   ~ ~   ~ ~ ~ ~ ~ ~ ~ ~ ~   ~   ~            ✿  | 
""" +
    Fore.LIGHTYELLOW_EX +
r"""   |                                                              |
   |  ╔══════════════════════════════════════════════════════════╗ |
   |  ║  AI says: Thank you for playing with us.                 ║ |
   |  ╚══════════════════════════════════════════════════════════╝ |
   |                                                              |
""" +
    Fore.MAGENTA +
r"""   |   ✿       ~  ~   ~ ~   ~ ~ ~ ~ ~ ~ ~ ~ ~   ~   ~        ✿     |
   |   ✿  ✿        ~ ~ ~  ~  ~   ~ ~ ~   ~  ~  ~ ~ ~     ✿  ✿      |
""" +
    Fore.GREEN +
r"""    \______________________________________________________________/
           \^^^^/      \^^^^/                \^^^^/      \^^^^/
            \__/        \__/                  \__/        \__/
"""
)

        return   # <-- Mini-Fix: jetzt beendet sich das Programm wirklich
    else:
        print(Fore.LIGHTWHITE_EX + "Unexpected problem occured, returning to main menu.")
    
    main_menu(if_set_game_on)

    
# RUN THE MENU
if_set_game_on = 1          #used to run main menu, if 0 will pass through and exit
main_menu(if_set_game_on)
