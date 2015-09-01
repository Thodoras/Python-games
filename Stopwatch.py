import simplegui


# define global variables
decisecond = 0
indicator = False
tries = 0
success = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(deciseconds):
    dseconds = deciseconds % 10
    mins = ((deciseconds - dseconds) / 10) / 60 
    secs = ((deciseconds - dseconds) / 10) % 60
    if (mins < 10):
        mins = '0' + str(mins)
    if (secs < 10):
        secs = '0' + str(secs)
    return str(mins) +":"+ str(secs)+"."+str(dseconds)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    timer.start()
    global indicator
    indicator = True

def stop_button():
    timer.stop()
    global indicator
    global success
    global tries
    if (indicator):
        indicator = False
        tries += 1
        if (decisecond % 10 == 0):
            success += 1

def reset_button():
    timer.stop()
    global indicator
    global success
    global tries
    global decisecond
    indicator = False
    success = 0
    tries = 0
    decisecond = 0
        

# define event handler for timer with 0.1 sec interval
def deciseconds():
    global decisecond
    decisecond += 1

# define draw handler
def draw_text(canvas):
    canvas.draw_text(format(decisecond),[90, 160], 36, 'Red')
    canvas.draw_text(str(success)+"/"+str(tries), [230,30], 30, 'Green')
       
   

# create frame
frame = simplegui.create_frame('Timer', 300, 300)

# register event handlers
timer = simplegui.create_timer(100, deciseconds)
button1 = frame.add_button('Start', start_button, 50)
button2 = frame.add_button('Stop', stop_button, 50)
button3 = frame.add_button('Reset', reset_button, 50)
frame.set_draw_handler(draw_text)

# start frame
frame.start()