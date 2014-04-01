# Intro to Python - Week 1 Mini-project
# E. Jones, copyright 2014
#
# Description: 
# A program to simluate the game Rock-Paper-Lizard-Scissors-Spock from
# The Big Bang Theory.
#
# Notes:
# This is a generic solution intended to be adaptable to any game of
# choice by changing the two global variables below. For consistency with
# the game templates, values 0-4 are used, but any values are acceptable as
# long as they are changed consistently between those two variables.

import random
############# Global Variables ################

# List of possible choices and their numeric values
# These do not need to be in order nor are you restricted to any range

choices = {"rock"    : 0,
           "Spock"   : 1,
           "paper"   : 2,
           "lizard"  : 3,
           "scissors": 4}

# List of values that a given choice defeats. E.g, winlose[0] returns [3,4], 
# so selecting option 0 would result in a win over options 3 and 4.

winarray = {0 : [3,4],
            1 : [4,0],
            2 : [0,1],
            3 : [1,2],
            4 : [2,3]}

######### End of Global Variables ############

# helper functions

def name_to_number(name):
    """
    Converts string name to equivalent integer value
    """
    if name in choices:
        return choices[name]
    else:
        return "Invalid choice"
    
def number_to_name(number):
    """
    Converts integer value into corresponding string
    """
    for name in choices.keys():
        if choices[name] == number:
            return name
    return "Invalid choice"

def computer_choose():
    """
    Computes an opponent's choice based on an upper max
    """
    computer_choice_num = None
    while (computer_choice_num not in winarray) :  
        computer_choice_num = random.randrange(min(winarray),max(winarray))
    return computer_choice_num

def win_lose(choice1, choice2):
    """
    Determines if choice1 beats choice2. Returns True for a win, False for a loss
    and None for a tie.
    """
    if choice2 == choice1:
        return None
    elif choice2 in winarray[choice1]:
        return True
    else:
        return False
    
def rpsls(player_choice_name):
    """
    A function to detmine the outcome of the game. It initiates the computer's choice,
    converts between integer choices and the corresponding names, checks for cheating,
    and outputs the results of the game. If an invalid choice is detected, a message
    is printed and the function returns.
    """
    
    # The computer makes its move, choosing randomly from the available options
    # and the choice is stored in the string variable "computer_choice_name"
    computer_choice_num = computer_choose()
    computer_choice_name = number_to_name(computer_choice_num)
    
    # We test to make sure the computer picked a valid option even though
    # we know that we coded it to
    if computer_choice_name == "Invalid choice":
        print "Computer broke the rules, aborting game!\n"
        return
    
    # The player's choice is checked for validity as well
    player_choice_num=name_to_number(player_choice_name)
    if player_choice_num == "Invalid choice":
        print "Player chooses", player_choice_name
        print "Player broke the rules, aborting game!\n"
        return
    
    # Now we determine the winner, printing the "throws" of both players and the outcome
    win_status = win_lose(player_choice_num,computer_choice_num)
    print "Player chooses", player_choice_name
    print "Computer chooses", computer_choice_name
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
