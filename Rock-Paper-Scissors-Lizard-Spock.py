import random
# A program that takes as an argument the choice of player, 
# chooses randomly the choice of the computer and
# outputs the outcome of the game (similar to rock - paper - scissors).
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

def name_to_number(name):
    # convert name to number using if/elif/else
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    elif name == 'scissors':
        return 4    

def number_to_name(number):
    # convert number to a name using if/elif/else
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    elif number == 4:
        return 'scissors'   

# Main function. 

def rpsls(player_choice): 
    #This is the main function.
    print " "
    print 'player chooses '+player_choice
    x = name_to_number(player_choice)
    y = random.randrange(0,5)
    print 'Computer choses '+ number_to_name(y)
    # compute difference of comp_number and player_number modulo five
    z = (x - y)%5 
    if z == 0:
        print 'Tie'
    elif z>2:
        print 'Computer wins'
    else:
        print 'Player wins'
    
# code testers
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")