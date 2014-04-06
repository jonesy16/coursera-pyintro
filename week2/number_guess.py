# Intro to Python - Week 2 Mini-project
# E. Jones, copyright 2014
#
# Description: 
# A program that plays Guess the Number
# Two ranges are allowed: [0,100) and [0,1000) which are selected via
# button inputs. The player has 7 guesses with the smaller range
# and 10 guesses with the larger range. Score is printed on the canvas.
#
# Notes:
# Due the the exclusive nature of the ranges ")", the actual guess
# range is 1 less (e.g., [0,100) includes all numbers from 0 through 99.
# The font sizes are automatically adjusted based on the size of the 
# canvas.

import simplegui
import random

# initialize global variables used in your code
guess_min   = 0
answer      = 0
guess_count = 0
wins        = 0
losses      = 0
max_font_size = 0

# Define canvas size and color
canvas_width  = 200
canvas_height = 200
canvas_color  = 'hsla(120,60%,70%,0.3)'

# helper function to start and restart the game
def new_game():
    """
    Starts a new game, resets guess counter
    """
    global guess_count, answer
    print '\nStarting new game!'
    print 'Guess a number between', guess_min, 'and', guess_max-1
    print 'You have', max_guesses, 'guesses to get it right'
    guess_count=0
    answer=random.randrange(guess_min,guess_max)

# define canvas drawing function
def draw_game_title(canvas):
    """
    Draws game title and sizes font appropriately
    """
    global max_font_size, font_size
    game_title = ("Guess","the","Number!")
    # set frame margin
    margin = 20
    # determine ideal text size
    if (max_font_size == 0):
        max_font_size = 200
        font_size = max_font_size
        text_width = frame.get_canvas_textwidth('Number!',font_size)
        while text_width > (canvas_width - 2 * margin):
            font_size -= 2
            text_width = frame.get_canvas_textwidth('Number!',font_size)
    # print game title, centered
    line_height = (canvas_height - 2 * margin) / 4 + font_size / 8
    text_y = margin
    for line in game_title:
        text_width = frame.get_canvas_textwidth(line, font_size)
        text_x = canvas_width / 2 - text_width / 2
        text_y = text_y + line_height
        canvas.draw_text(line, (text_x,text_y), font_size, 'Black')
    # print score
    text_y = canvas_height - margin
    score_font_size = font_size / 3
    # print wins
    text_width = frame.get_canvas_textwidth('Wins: '+str(wins), score_font_size)
    text_x = canvas_width / 4 - text_width / 2
    canvas.draw_text('Wins: '+str(wins), (text_x,text_y), score_font_size, 'Black')
    # print losses
    text_width=frame.get_canvas_textwidth('Losses: '+str(losses), score_font_size)
    text_x = canvas_width * 3 / 4 - text_width / 2
    canvas.draw_text('Losses: '+str(losses), (text_x,text_y), score_font_size, 'Black')

# define event handlers for control panel
def range100():
    """
    button that changes range to range [0,100) and restarts
    """
    global guess_max, max_guesses
    guess_max, max_guesses = 100, 7
    new_game()

def range1000():
    """
    button that changes range to range [0,1000) and restarts
    """
    global guess_max, max_guesses
    guess_max, max_guesses = 1000, 10
    new_game()

def input_guess(guess):
    """
    Game logic and input processing. Reads 'guess' and determines
    whether the guess is 1) valid and 2) correct. Keeps score.
    """
    global guess_count, wins, losses
    # Reset input field
    inp_field.set_text('')
    # Check for guess validity
    try:
        int(guess)
        guess = int(guess)
    except:
        print '\nInvalid guess, try again'
        return
    if (guess >= guess_max) or (guess < guess_min):
        print '\nInvalid guess'
        return
    # If guess is valid, increase guess count
    else:
        guess_count += 1
    # Print results
    print '\nYou guessed', guess
    if guess == answer:
        print "That's it, you win!"
        wins += 1
        new_game()
    else:
        if guess > answer:
            print 'Your guess is too high'
        else:
            print 'Your guess is too low'
        if (max_guesses - guess_count == 1 ):
            print 'You have 1 guess left'
        elif guess_count == max_guesses:
            print 'Out of guesses, Game Over'
            losses += 1
            new_game()
        else:
            print 'You have', max_guesses - guess_count,'guesses left'
    return

# create frame

frame=simplegui.create_frame('Game', canvas_width, canvas_height)
frame.set_canvas_background(canvas_color)
frame.set_draw_handler(draw_game_title)

# add buttons

frame.add_button('Set range to [0,100)',   range100, 150)
frame.add_button('Set range to [0,1000)', range1000, 150)

# register event handlers for control elements

inp_field=frame.add_input('Guess: ', input_guess, 100)

# call new_game and start frame

range100()
frame.start()
