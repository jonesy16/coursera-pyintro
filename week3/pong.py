# CodeSkulptor runs Python programs in your browser.
# Click the upper left button to run this simple demo.

# CodeSkulptor runs in Chrome 18+, Firefox 11+, and Safari 6+.
# Some features may work in other browsers, but do not expect
# full functionality.  It does NOT run in Internet Explorer.

import simplegui
import math
import random

# define global variables

player_score     = 0             # game score
computer_score   = 0
score_font_size  = 20  # score font size
score_font_color = 'Red'
game_state       = 0   # (0=stop, 1=active, 2=pause)
on_top_edge      = False
on_bot_edge      = False
player_pdl_vel   = 0

# Define canvas size and color

canvas_width  = 400
canvas_height = 300
center_x      = canvas_width / 2
center_y      = canvas_height / 2
canvas_color  = 'Black'

# Define paddle variables
ball_rad     = 6  # size of ball
ball_max_vel = 3  # maximum ball velocity
pdl_vel      = 3  # paddle movement speed
pdl_width    = 10  # width of paddle
pdl_height   = 50 # height of paddle
board_margin = 5  # distance of paddle from screen edge

pdl_left_edge_l   = board_margin
pdl_left_edge_r   = pdl_left_edge_l + pdl_width
pdl_left_edge_bot = center_y + pdl_height / 2
pdl_left_edge_top = pdl_left_edge_bot - pdl_height

pdl_right_edge_r = canvas_width - 1 - board_margin
pdl_right_edge_l = pdl_right_edge_r - pdl_width
pdl_right_edge_bot = center_y + pdl_height / 2
pdl_right_edge_top = pdl_left_edge_bot - pdl_height

# Define scorekeeper

def score(team):
    """
    Keeps score and starts the next round
    """
    global player_score, computer_score
    if team == 'player':
        player_score += 1
    else:
        computer_score += 1
    reset_ball()
    # call a timer to start the next round so the player can prepare
    timer.start()
    return

def reset_ball():
    """
    Resets the ball to the middle of the canvas with 0 velocity
    """
    global ball_pos, ball_vel
    ball_pos = [canvas_width / 2, canvas_height / 2]
    ball_vel = [0, 0]
    return

def move_player_paddle():
    """
    Moves the players paddle based on keyboard input
    """
    global pdl_vel, on_top_edge, on_bot_edge
    global pdl_left_edge_top, pdl_left_edge_bot
    pdl_left_edge_bot += player_pdl_vel
    pdl_left_edge_top += player_pdl_vel
    if pdl_left_edge_top <= 0:
        on_top_edge = True
        pdl_left_edge_top = 0
        pdl_left_edge_bot = pdl_height
    elif pdl_left_edge_bot >= (canvas_height - 1):
        on_bot_edge = True
        pdl_left_edge_bot = canvas_height - 1
        pdl_left_edge_top = pdl_left_edge_bot - pdl_height
    return

def move_computer_paddle():
    """
    A simple implementation of the computer's AI.
    Basically the computer gets to move if the ball is coming towards it.
    If ball is above paddle, move paddle up, and vice versa.
    """
    global pdl_right_edge_top, pdl_right_edge_bot
    pdl_right_middle = (pdl_right_edge_top + pdl_right_edge_bot) / 2
    if ball_vel[0] > 0:
        if ball_pos[1] < pdl_right_middle:
            pdl_right_vel = -pdl_vel
        elif ball_pos[1] > pdl_right_middle:
            pdl_right_vel = pdl_vel
        else:
            pdl_right_vel = 0
    else:
        pdl_right_vel = 0
    if pdl_right_edge_top <= 0:
        if pdl_right_vel < 0:
            pdl_right_vel = 0
    elif pdl_right_edge_bot >= (canvas_height - 1):
        if pdl_right_vel > 0:
            pdl_right_vel = 0
    pdl_right_edge_bot += pdl_right_vel
    pdl_right_edge_top += pdl_right_vel

def move_ball():
    """
    Moves the ball's location based on its current velocity
    """
    # determine ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # check for intersection with paddle
    isect = ball_intersect_paddle()
    # check for intersection with screen edge (top/bot first)
    if not isect:
        ball_intersect_screen()
    # check for scoring position
        if (ball_pos[0] > (canvas_width - 1)):
            score('player')
        elif ball_pos[0] <= 0:
            score('computer')
    return

def ball_intersect_paddle():
    """
    Checks for ball intersection with paddle and computes new velocity
    based on where it hits the paddle.
    """
    isect = 0
    if ((ball_pos[0] - ball_rad) <= pdl_left_edge_r) and \
       ((ball_pos[1] + ball_rad) >= pdl_left_edge_top) and \
       ((ball_pos[1] - ball_rad) <= pdl_left_edge_bot):
        isect = 1
        isect_dist_from_top = ball_pos[1] - pdl_left_edge_top - ball_rad
        isect_dist_from_bottom = pdl_left_edge_bot - ball_pos[1] - ball_rad
    elif ((ball_pos[0] + ball_rad) >= pdl_right_edge_l) and \
         ((ball_pos[1] + ball_rad) >= pdl_right_edge_top) and \
         ((ball_pos[1] - ball_rad) <= pdl_right_edge_bot):
        isect = 1
        isect_dist_from_top = ball_pos[1] - pdl_right_edge_top - ball_rad
        isect_dist_from_bottom = pdl_right_edge_bot - ball_pos[1] - ball_rad
    if isect == 1:
        if abs(isect_dist_from_bottom - isect_dist_from_top) < (pdl_height / 3):
            ball_vel[0] = -ball_vel[0]
            ball_vel[1] = ball_vel[1]
        elif isect_dist_from_top <= 0:
            vel_mult = min((ball_rad - isect_dist_from_top)/ball_rad,ball_max_vel)
            ball_vel[1] = -abs(max(ball_vel[1]*vel_mult,ball_max_vel))
            if ball_vel[0] > 0:
                ball_vel[0] = -max(ball_vel[0]*vel_mult,ball_max_vel)
            else:
                ball_vel[0] = max(ball_vel[0]*vel_mult,ball_max_vel)
        elif isect_dist_from_bottom <= 0:
            vel_mult = min((ball_rad - isect_dist_from_bottom)/ball_rad,ball_max_vel)
            ball_vel[1] = max(abs(ball_vel[1])*vel_mult,ball_max_vel)
            if ball_vel[0] > 0:
                ball_vel[0] = -max(ball_vel[0]*vel_mult,ball_max_vel)
            else:
                ball_vel[0] = max(ball_vel[0]*vel_mult,ball_max_vel)
        elif isect_dist_from_top < isect_dist_from_bottom:
            ball_vel[1] = -abs(ball_vel[1])
            ball_vel[0] = -ball_vel[0]
        elif isect_dist_from_bottom < isect_dist_from_top:
            ball_vel[1] = abs(ball_vel[1])
            ball_vel[0] = -ball_vel[0]
        return True
    else:
        return False

def ball_intersect_screen():
    """
    Checks if the ball intersects the screen edge and reflects it
    """
    if ((ball_pos[1] - ball_rad) <= 0):
        ball_vel[1] = -ball_vel[1]
        ball_pos[1] = ball_rad
    elif (ball_pos[1] + ball_rad) > (canvas_height - 1):
        ball_vel[1] = -ball_vel[1]
        ball_pos[1] = canvas_height - 1 - ball_rad
    return

# define key handler

def keydown_handler(key):
    """
    Handle keyboard input when keys are pressed
    """
    global player_pdl_vel, on_top_edge, on_bot_edge
    if key == simplegui.KEY_MAP["down"]:
        if not on_bot_edge:
            on_top_edge = False
            player_pdl_vel = pdl_vel
    elif key == simplegui.KEY_MAP["up"]:
        if not on_top_edge:
            on_bot_edge = False
            player_pdl_vel = -pdl_vel
    elif key == simplegui.KEY_MAP["space"]:
        game_pause()
    return

def keyup_handler(key):
    """
    Handle keyboard input when keys are released
    """
    global player_pdl_vel
    if key == simplegui.KEY_MAP["down"]:
        player_pdl_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        player_pdl_vel = 0
    return

# define event handlers

def game_reset():
    """
    Reset the game and score
    """
    global player_score, computer_score, game_state
    player_score = 0
    computer_score = 0
    reset_ball()
    game_state = 0
    return

def game_start():
    """
    Start the game, i.e., launch the ball.
    Determines a random starting velocity for the ball.
    """
    global ball_vel, game_state
    if (ball_vel[0] or ball_vel[1]):
        return
    ball_x_vel = min(random.randint(1,max(player_score,computer_score,1)),ball_max_vel)
    ball_y_vel = min(random.randint(1,max(player_score,computer_score,1)),ball_max_vel)
    if random.randint(1,2) == 1:
        ball_x_vel = -ball_x_vel
    if random.randint(1,2) == 1:
        ball_y_vel = -ball_y_vel
    ball_vel = [ball_x_vel, ball_y_vel]
    game_state = 1
    timer.stop()
    return

def game_pause():
    """
    Pauses the game
    """
    global game_state
    if game_state == 2:
        game_state = 1
    else:
        game_state = 2

# define draw handler

def draw_paddle(canvas):
    """
    """
    if game_state == 0:
        canvas.draw_text(msg_start, (center_x - msg_start_width / 2,
                                     center_y + msg_font_size / 2),
                                     msg_font_size, 'White' )
    elif game_state == 2:
        canvas.draw_text(msg_pause, (center_x - msg_pause_width / 2,
                                     center_y + msg_font_size / 2),
                                     msg_font_size, 'White' )
    else:
        # determine ball_position
        move_ball()
        # determine paddle position
        move_player_paddle()
        move_computer_paddle()
        # draw ball and paddles
        canvas.draw_circle(ball_pos, ball_rad, 1, 'White', 'White')
        canvas.draw_polygon([(pdl_left_edge_l,pdl_left_edge_bot),
                             (pdl_left_edge_r,pdl_left_edge_bot),
                             (pdl_left_edge_r,pdl_left_edge_top),
                             (pdl_left_edge_l,pdl_left_edge_top)], 1, 'White', 'White')
        canvas.draw_polygon([(pdl_right_edge_l,pdl_right_edge_bot),
                             (pdl_right_edge_r,pdl_right_edge_bot),
                             (pdl_right_edge_r,pdl_right_edge_top),
                             (pdl_right_edge_l,pdl_right_edge_top)], 1, 'White', 'White')
        # draw score
        canvas.draw_text(str(player_score), (center_x - 20, 25),
                         score_font_size, score_font_color)
        canvas.draw_text(str(computer_score), (center_x + 20, 25),
                         score_font_size, score_font_color)
        # draw ball velocity
        canvas.draw_text(str(ball_vel), (10,10), 10, 'green')
        # draw standby message
        if timer.is_running():
            
            canvas.draw_text(msg_ready, (center_x - msg_ready_width / 2,
                                         center_y + msg_font_size),
                                         msg_font_size, 'White')

# create frame

frame=simplegui.create_frame('Paddle', canvas_width, canvas_height)
frame.set_canvas_background(canvas_color)
frame.set_draw_handler(draw_paddle)

# register event handlers

frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
timer = simplegui.create_timer(1000, game_start)

# Create buttons

frame.add_button('New Game', game_reset, 200)
frame.add_button('Start Game', game_start, 200)
frame.add_button('Pause (spacebar)', game_pause, 200)

# Create Game Messages

msg_font_size = 24
msg_start = "Press 'Start Game' to start!"
msg_pause = "Press spacebar to resume"
msg_ready = "Get ready"
msg_start_width = text_width = frame.get_canvas_textwidth(msg_start, msg_font_size)
msg_pause_width = text_width = frame.get_canvas_textwidth(msg_pause, msg_font_size)
msg_ready_width = text_width = frame.get_canvas_textwidth(msg_ready, msg_font_size)

# start frame

reset_ball()
frame.start()
