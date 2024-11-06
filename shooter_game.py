from pygame import *
from random import randint
from time import time as timer

#background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)
#we need the following images:
img_back = "galaxy.jpg" #game background
img_hero = "rocket.png" #hero
img_enemy = 'ufo.png'
img_bullet = "bullet.png"
score = 0
goal = 11
lost = 0
max_lost = 5

#parent class for other sprites
class GameSprite(sprite.Sprite):
 #class constructor
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Call for the class (Sprite) constructor:
       sprite.Sprite.__init__(self)


       #every sprite must store the image property
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #every sprite must have the rect property – the rectangle it is fitted in
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #method drawing the character on the window
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
       
class Player(GameSprite):
   #method to control the sprite with arrow keys
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #method to "shoot" (use the player position to create a bullet there)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost = lost +1

class Enemy1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, 620)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


score = 0
lost = 0
#create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, 620), -40, 80, 50, randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Enemy1('asteroid.png', randint(80, 620), -40, 80, 50, randint(1,5))
    asteroids.add(asteroid)

#the "game is over" variable: as soon as True is there, sprites stop working in the main loop
finish = False
#Main game loop:
run = True #the flag is reset by the window close button
bullets = sprite.Group()
num_fire = 0
rel_time = False
while run:
   #"Close" button press event
   for e in event.get():
       if e.type == QUIT:
           run = False
       elif e.type == KEYDOWN:
        if e.key == K_SPACE:
            if num_fire <5 and rel_time == False:
                num_fire = num_fire +1
                fire_sound.play()
                ship.fire()

            if num_fire >=5 and rel_time == False:
                last_time = timer()
                rel_time = True


   if not finish:
       #update the background
       window.blit(background,(0,0))
       teks = font2.render('score: '+ str(score), 1, (255, 255, 255))
       window.blit(teks, (10, 20))
       teks2 = font2.render('missed: '+ str(lost), 1, (255, 255, 255))
       window.blit(teks2, (10, 50))
       #launch sprite movements
       ship.update()
       monsters.update()
       asteroids.update()
       bullets.update()
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
        score = score + 1
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
        monsters.add(monster)
       if sprite.spritecollide(ship, monsters, False) or lost >= max_lost or sprite.spritecollide(ship, asteroids, False):
        finish = True
        window.blit(lose, (200, 200))
       if score >= goal :
        finish = True
        window.blit(win, (200, 200))


       #update them in a new location in each loop iteration
       ship.reset()
       monsters.draw(window)
       asteroids.draw(window)
       bullets.draw(window)
       if rel_time == True:
        now_time = timer()
        if now_time - last_time <3:
            reload = font2.render('wait, reload', 1, (150, 0, 0))
            window.blit(reload, (260, 460))
        else:
            num_fire = 0
            rel_time = False
       display.update()
   #the loop is executed each 0.05 sec
   time.delay(50)