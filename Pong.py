# Implementation of game - Pong.

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [300,200]
    if direction:
        ball_vel = [random.random()*3 + 1,-random.random() - 1]
    else:
        ball_vel = [-random.random()*3 - 1,-random.random() - 1]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(random.choice([LEFT, RIGHT]))
    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT/2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT/2]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    #draw scores
    canvas.draw_text(str(score1), [185,100], 50, 'Green')
    canvas.draw_text(str(score2), [385,100], 50, 'Green')
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'Red', 'Red')
     
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] + paddle1_vel >= 40 and paddle1_pos[1] + paddle1_vel <= 360:
        paddle1_pos[1] += paddle1_vel
        
    if paddle2_pos[1] + paddle2_vel >= 40 and paddle2_pos[1] + paddle2_vel <= 360:
        paddle2_pos[1] += paddle2_vel
    
    # draw paddles
    canvas.draw_polygon([[paddle1_pos[0] - 4, paddle1_pos[1] - 40], [paddle1_pos[0] - 4, paddle1_pos[1] + 40], [paddle1_pos[0] + 4, paddle1_pos[1] + 40], [paddle1_pos[0] + 4, paddle1_pos[1] - 40]], 2, 'Purple', 'Purple')
    canvas.draw_polygon([[paddle2_pos[0] - 4, paddle2_pos[1] - 40], [paddle2_pos[0] - 4, paddle2_pos[1] + 40], [paddle2_pos[0] + 4, paddle2_pos[1] + 40], [paddle2_pos[0] + 4, paddle2_pos[1] - 40]], 2, 'Orange', 'Orange')
    
    # determine whether paddle and ball collide
    if ball_pos[0] - 20 <= 8:
        if ball_pos[1] - paddle1_pos[1] <= 40 and ball_pos[1] - paddle1_pos[1] >= -40:
            ball_vel[0] = -(ball_vel[0] + 0.1 * ball_vel[0])
        else:
            score2 += 1
            spawn_ball(RIGHT)
    if ball_pos[0] + 20 >= 592:
        if ball_pos[1] - paddle2_pos[1] <= 40 and ball_pos[1] - paddle2_pos[1] >= -40:
            ball_vel[0] = -(ball_vel[0] + 0.1 * ball_vel[0])
        else:
            spawn_ball(LEFT)
            score1 += 1
    if ball_pos[1] - 20 <= 0 or ball_pos[1] + 20 >= 400:
        ball_vel[1] *= -1
    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 4
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 4
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 4
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 4
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += 4
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= 4
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel += 4
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= 4


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)


# start frame
new_game()
frame.start()