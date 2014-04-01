# A program to simluate the game Rock-Paper-Lizard-Scissors-Spock from
# The Big Bang Theory.
# This is a generic solution intended to be adaptable to any game of
# choice by changing the three global variables below.

import random
############# Global Variables ################

# Number of possible choices in this game
num_choices = 5

# List of possible choices and their numeric values

choices = {"rock":0,
           "Spock":1,
           "paper":2,
           "lizard":3,
           "scissors":4}

# List of values that a given choice defeats. E.g, winlose[0] returns [3,4], 
# so selecting option 0 would result in a win over options 3 and 4.

winarray = [[3,4],
           [4,0],
           [0,1],
           [1,2],
           [2,3]]

######### End of Global Variables ############

# helper functions

def name_to_number(name):
    """Converts string name to equivalent integer value"""
    if name in choices:
        return choices[name]
    else:
        return "Invalid choice"
    
def number_to_name(number):
    """Converts integer value into corresponding string"""
    for name in choices.keys():
        if choices[name] == number:
            return name
    return "Invalid choice"

def computer_choose(choice_limit):
    """Computes an opponent's choice based on an upper max"""
    if choice_limit <= 0:
        print "Computer is left without a valid move to make"
    return random.randrange(0,choice_limit)

def win_lose(choice1, choice2):
    """Determines if choice1 beats choice2. Returns True for a win, False for a loss
    and None for a tie."""
    if choice2 == choice1:
        return None
    elif choice2 in winarray[choice1]:
        return True
    else:
        return False
    
def rpsls(player_choice_name):
    """A function to detmine the outcome of the game. It initiates the computer's choice,
    converts between integer choices and the corresponding names, checks for cheating,
    and outputs the results of the game. If an invalid choice is detected, a message
    is printed and the function returns."""
    computer_choice_num = computer_choose(num_choices)
    computer_choice_name = number_to_name(computer_choice_num)
    if computer_choice_name == "Invalid choice":
        print "Computer attempted to bypass the rules, aborting game!\n"
        return
    player_choice_num=name_to_number(player_choice_name)
    if player_choice_num == "Invalid choice":
        print "Player chooses", player_choice_name
        print "Player attempted to cheat or needs the rules reread to them, aborting game!\n"
        return
    print "Player chooses", player_choice_name
    print "Computer chooses", computer_choice_name
    win_status = win_lose(player_choice_num,computer_choice_num)
    if win_status == None:
        print "Player and computer tie!\n"
    elif win_status:
        print "Player wins!\n"
    else:
        print "Computer wins!\n"
    
# Run the code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# Error tests
# Check for invalid user choice
rpsls("Scottie")
