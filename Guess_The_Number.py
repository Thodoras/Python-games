import simplegui
import random

num = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global tries, secret_number
    secret_number = random.randrange(0,num+1)
    if num == 100:
        tries = 7
    else:
        tries = 10
    print "Range is " + str(num)
    print "You have " + str(tries)+ " tries left"
    print "Enter a number"
    print " "    
    

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num
    num = 100
    new_game()   

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num
    num = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here
    global tries
    print "Guess was " + guess
    if int(guess) > secret_number:
        print "lower"
        tries -= 1
        if tries > 0:
            print "You have "+str(tries)+ " left"
            print " "
        else:
            print "You lose the secret number was" + str(secret_number)
            print " "
            new_game()
    elif int(guess) < secret_number:
        print "higher"
        tries -= 1
        if tries > 0:
            print "You have "+str(tries)+ " left"
            print " "
        else:
            print "You lose the secret number was " + str(secret_number)
            print " "
            new_game()
    else:
        print "You are correct"
        print " "
    
# create frame
f = simplegui.create_frame("Guess the number.", 300, 300)

# register event handlers for control elements and start frame
f.add_input("Enter number",input_guess,100)
f.add_button("Range [0,100]", range100, 100)
f.add_button("Range [0,1000]", range1000, 100)

# call new_game 
new_game()
