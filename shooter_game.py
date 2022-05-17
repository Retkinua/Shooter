from pygame import *
from random import randint
from time import time as timer #импортируем функцию для засекания времени, чтобы интерпретатор не искал эту функцию в pygame модуле time, даём ей другое название сами

mixer.init()
mixer.music.load('Robobozo.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg') 

win_width = 1080
win_height = 720
window = display.set_mode((win_width, win_height))
display.set_caption("Space RobotoShooter")
background = transform.scale(image.load("galaxy-gd44c95260_1280.jpg"), (win_width, win_height))
 
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 720:
            self.rect.y = 0
            self.rect.x = randint(80, 1000)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 720:
            self.rect.y = 0
            self.rect.x = randint(80, 1000)

asteroids = sprite.Group()
for i in range(1, 3):
   asteroid = Asteroid('asteroid.png', randint(30, 1000), -40, 80, 50, randint(1, 7))
   asteroids.add(asteroid)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80,1000), -40, 80, 50, randint(1,5))
    monsters.add(monster)

font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 72)
lost = 0
score = 0
bullets = sprite.Group()

ship = Player("rocket.png", 5, win_height - 100, 80, 100, 18)
finish = False
run = True 

rel_time = False #флаг, отвечающий за перезарядку
 
num_fire = 0  #переменная для подсчёта выстрелов  
life = 3

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire  >= 5 and rel_time == False : #если игрок сделал 5 выстрелов
                    last_time = timer() #засекаем время, когда это произошло
                    rel_time = True #ставим флаг перезарядки

    if not finish:
        window.blit(background,(0,0))
        text = font1.render('Счет: ' + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer() #считываем время        
            if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезарядке
                reload = font1.render('идет перезарядка...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0   #обнуляем счётчик пуль
                rel_time = False #сбрасываем флаг перезарядки

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life -1

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if score >= 10:
            finish = True
            win = font1.render('YOU WIN!', True, (255, 255, 255))
            window.blit(win, (200, 200))
        if life == 0 or lost >= 8:
            finish = True 
            lose = font1.render('YOU LOSE!', True, (180, 0, 0))
            window.blit(lose, (200, 200))
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
    
        text_life = font2.render(str(life), 1, life_color)
        window.blit(text_life, (1030, 10))
        display.update()
    time.delay(20)
