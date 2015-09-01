# Implementation of game "Spaceship"
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

#general globals
rock_group = set()
missile_group = set()
explosion_group = set()

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False, factor = 1):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
        self.factor = factor

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
    def get_size_in_canvas(self):
        return [self.size[0]*self.factor, self.size[1]*self.factor]
        

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
small_asteroid_info = ImageInfo([45,45], [90,90], 40, None, False, 0.5)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def collision_ship():
    global started, lives, missile_group, rock_group, ship1
    for rock in rock_group:
        if rock.collide(ship1):
            explode_rock(rock)
            rock_group.discard(rock)
            if lives > 0:
                lives -= 1
            if lives == 0:
                started = False
                missile_group = set()
                rock_group = set()
                soundtrack.rewind()
                ship1 = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
            
def eliminate_old_missiles():
    for missile in missile_group:
        if missile.old():
            missile_group.remove(missile)
            
def destroy_rocks():
    global score
    for missile in missile_group:
        for rock in rock_group:
            if dist(rock.pos, missile.pos) < rock.radius + missile.radius:
                split_rock(rock)
                explode_rock(rock)
                missile_group.discard(missile)
                rock_group.discard(rock)
                score += 1

def explode_rock(rock):
    explosion = Sprite(rock.pos, [0,0], 0, 0, explosion_image, explosion_info)
    explosion_sound.rewind()
    explosion_sound.play()
    explosion_group.add(explosion)
 
def eliminate_old_explosions():
    for explosion in explosion_group:
        if explosion.old():
            explosion_group.discard(explosion)
            
def split_rock(rock):
    if rock.radius == 40:
        rock_group.add(Sprite(rock.pos, rotate_45_degrees_cw(rock.vel), rock.angle, rock.angle_vel, asteroid_image, small_asteroid_info))
        rock_group.add(Sprite(rock.pos, rotate_45_degrees_qcw(rock.vel), rock.angle, rock.angle_vel, asteroid_image, small_asteroid_info))
        
def rotate_45_degrees_qcw(vector):
    v = []
    v.append(vector[0]*math.cos(math.pi/4) + vector[1]*math.sin(math.pi/4))
    v.append(- vector[0]*math.sin(math.pi/4) + vector[1]*math.cos(math.pi/4))
    return v

def rotate_45_degrees_cw(vector):
    v = []
    v.append(vector[0]*math.cos(-math.pi/4) + vector[1]*math.sin(-math.pi/4))
    v.append(- vector[0]*math.sin(-math.pi/3) + vector[1]*math.cos(-math.pi/3))
    return v

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            ship_info.get_center()[0] = 135
        else:
            ship_info.get_center()[0] = 45
        canvas.draw_image(ship_image, ship_info.get_center(), ship_info.get_size(), self.pos, ship_info.get_size(), self.angle)
        
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
        self.vel[0] *= 0.993
        self.vel[1] *= 0.993
        
        self.angle += self.angle_vel
        
        if self.thrust:
            self.vel[0] += 0.07*angle_to_vector(self.angle)[0]
            self.vel[1] += 0.07*angle_to_vector(self.angle)[1]
            
    def shoot(self):
        missile_group.add(Sprite([self.pos[0] + self.radius*angle_to_vector(self.angle)[0], self.pos[1] + self.radius*angle_to_vector(self.angle)[1]], 
                                 [self.vel[0] + 5*angle_to_vector(self.angle)[0],self.vel[1] + 5*angle_to_vector(self.angle)[1]], 0, 0, missile_image, missile_info, missile_sound))
        
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()*info.factor
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.image_size_in_canvas = info.get_size_in_canvas()
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.age*128, self.image_center[1]], self.image_size, self.pos, self.image_size_in_canvas, self.angle) 
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size_in_canvas, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        
        self.angle += self.angle_vel
        
        self.age += 1
        
    def collide(self, other):
        if dist(self.pos, other.pos) < self.radius + other.radius:
            return True
        else:
            return False
     
    def old(self):
        if self.age > self.lifespan:
            return True
        else:
            return False
        
        
#Key handlers
def keyboard_input_down(key):
    if key == simplegui.KEY_MAP["right"]:
        ship1.angle_vel = math.pi/40
    if key ==  simplegui.KEY_MAP["left"]:
        ship1.angle_vel = -math.pi/40
    if key ==  simplegui.KEY_MAP["up"]:
        ship1.thrust = True
        ship_thrust_sound.play()
    if key == simplegui.KEY_MAP["space"]:
        ship1.shoot()
        
def keyboard_input_up(key):
    if key == simplegui.KEY_MAP["right"]:
        ship1.angle_vel = 0
    if key ==  simplegui.KEY_MAP["left"]:
        ship1.angle_vel = 0
    if key ==  simplegui.KEY_MAP["up"]:
        ship1.thrust = False
        ship_thrust_sound.rewind()
    
#Mouse handler
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        soundtrack.play()
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites 
    ship1.draw(canvas)
    for missile in missile_group:
        missile.draw(canvas)
    for rock in rock_group:
        rock.draw(canvas)
    for explosion in explosion_group:
        explosion.draw(canvas)
    
    # update ship and sprites
    ship1.update()
    eliminate_old_missiles()
    eliminate_old_explosions()
    for rock in rock_group:
        rock.update()
    for missile in missile_group:
        missile.update()
    for explosion in explosion_group:
        explosion.update()
    
    #draw score and lives
    canvas.draw_text('Lives', [40,40], 25, 'White', 'sans-serif')
    canvas.draw_text(str(lives), [40,65], 25, 'White', 'sans-serif')
    
    canvas.draw_text('Score', [700,40], 25, 'White', 'sans-serif')
    canvas.draw_text(str(score), [700,65], 25, 'White', 'sans-serif')
    
    #draw collision
    collision_ship()
    destroy_rocks()
    
    #draw splash screen every time a new game starts
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
# timer handler that spawns a rock    
def rock_spawner():
    if len(rock_group) <= 12 and started:
        while(True):
            sprite = Sprite([random.random()*WIDTH, random.random()*HEIGHT], [random.random()*4 - 2, random.random()*2 - 1], random.random()*math.pi*2, random.random()*math.pi/60.0 - math.pi/120, asteroid_image, asteroid_info)
            if dist(sprite.pos, ship1.pos) > 100:
                rock_group.add(sprite)
                break
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship
ship1 = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keyboard_input_down)
frame.set_keyup_handler(keyboard_input_up)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()