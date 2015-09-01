# implementation of card game - Memory

import simplegui
import random


lst = []
exposed = range(16)
cards_open = 0
turns = 0
pair_cards = [0,0]

# helper function to initialize globals
def new_game():
    global lst, exposed, cards_open, turns
    lst1 = range(8)
    lst2 = range(8)
    lst = lst1 + lst2
    random.shuffle(lst)
    for i in range(16):
        exposed[i]= False
    cards_open = 0
    turns = 0
    label.set_text("Turns = "+ str(turns))

     
# define event handlers
def mouseclick(pos):
    global exposed, cards_open, turns, pair_cards
    index = pos[0] // 50
    if not exposed[index]:
        if cards_open < 2:
            exposed[index] = True
            pair_cards[cards_open] = index
            cards_open += 1
        else:
            exposed[index] = True
            cards_open = 1
            if lst[pair_cards[0]] != lst[pair_cards[1]]:
                exposed[pair_cards[0]] = False
                exposed[pair_cards[1]] = False
            pair_cards[0] = index
            turns += 1
            label.set_text("Turns = "+ str(turns))
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(lst[i]), [20+i*50,60], 30, 'Red')
        else:
            canvas.draw_polygon([[0+i*50,0], [50+i*50, 0], [50+i*50, 100], [0+i*50, 100]], 1, 'Yellow', 'Green')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = "+ str(turns))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()