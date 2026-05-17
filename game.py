import pygame as pg
from random import randint
pg.init()
pg.font.init()
pg.mixer.init()

back_img = 'images/Background.jpg'
helicopter_left_img = 'images/Helicopter_left.png'
helicopter_right_img = 'images/Helicopter.png'
alien_img = 'images/Aliens.png'
skydiver_img = 'images/Skydiver.png'

win_width, win_height = 1000, 700
FPS = 60
score = 0
STOP_SCORE = 10

window = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('HeliRescue')
pg.display.set_icon(pg.image.load(helicopter_right_img))
clock = pg.time.Clock()

background = pg.transform.scale(pg.image.load(back_img), (win_width, win_height))

pg.mixer.music.load('sounds/Silly-Fun(chosic.com).mp3')
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.4)

sound_safe = pg.mixer.Sound('sounds/Voicy_Homer Simpson_ Woo-hoo.mp3')
sound_safe.set_volume(0.5)
sound_lost = pg.mixer.Sound('sounds/Retro-Space-Explosion-Or-Death-chosic.com_.mp3')
sound_lost.set_volume(0.5)

class GameSprite(pg.sprite.Sprite):
    def __init__(self, filename: tuple = (), x: int = 0, y: int = 0, width: int = 10, height: int = 10, speed: int = 10):
        super().__init__()
        self.filename = filename
        self.width = width
        self.height = height
        self.image = pg.transform.scale(pg.image.load(self.filename[0]), (self.width, self.height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
        self.speed = speed 
                
    def draw_sprite(self):
        window.blit(self.image, (self.rect.x, self.rect.y))    
        
class Helicopter(GameSprite):
    def __init__(self, filename, x, y, width, height, speed):
        super().__init__(filename, x, y, width, height, speed)
        self.image_right = pg.transform.scale(pg.image.load(filename[0]), (width, height))
        self.image_left = pg.transform.scale(pg.image.load(filename[1]), (width, height))
        self.image = self.image_right

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] and self.rect.x < win_width - 100:
            self.image = self.image_right
            self.rect.x += self.speed
        if keys[pg.K_LEFT] and self.rect.x > 10:
            self.image = self.image_left
            self.rect.x -= self.speed
        if keys[pg.K_UP] and self.rect.y > 10:
            self.rect.y -= self.speed
        if keys[pg.K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        
class SkyDiver(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            
class Alien(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.y = randint(80, win_height - 80)
            self.rect.x = win_width            

class Label(pg.sprite.Sprite):
    def set_text(self, x: int = 0, y: int = 0, text: str = '', font_size: int = 12, text_color: tuple = (0, 0, 0)):
        font_family = 'font/MADE Dillan RUS.ttf'
        self.text = pg.font.Font(font_family, font_size).render(text, True, text_color)
        self.rect = self.text.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw_text(self):
        window.blit(self.text, (self.rect.x, self.rect.y))

helicopter = Helicopter((helicopter_right_img, helicopter_left_img), 30, win_height // 2, 100, 80, 10)
skydiver = SkyDiver((skydiver_img,), randint(80, win_width - 80), 0, 40, 50, randint(2, 5))
alien = Alien((alien_img,),  win_width, randint(80, win_height - 80), 100, 80, randint(5, 10))  

score_text = Label() 
lose_text = Label()
lose_text.set_text(win_width // 3, win_height // 2, 'YOU LOSE!', 72, (242, 12, 12)) 
win_text = Label()
win_text.set_text(win_width // 3, win_height // 2, 'YOU WIN!', 72, (242, 158, 12))  

again_text = Label()
again_text.set_text(win_width // 6, win_height // 4, 'PLAY AGAIN? CLICK HERE!', 48, (124, 103, 245))

def reset_game():
    global score, finish, win, helicopter, skydiver, alien

    score = 0
    finish = False
    win = False

    helicopter.rect.x = 30
    helicopter.rect.y = win_height // 2
    helicopter.image = helicopter.image_right

    skydiver.rect.x = randint(80, win_width - 80)
    skydiver.rect.y = 0
    skydiver.speed = randint(2, 5)

    alien.rect.x = win_width
    alien.rect.y = randint(80, win_height - 80)
    alien.speed = randint(5, 10)

    score_text.set_text(5, 10, f'SCORE: {score}', 24, (124, 103, 245))
    
game = True
finish = False
win = False
while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
            
        if finish and event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
            if again_text.rect.collidepoint(event.pos):
                reset_game()
            
    if not finish:
        window.blit(background, (0, 0))        
        
        if pg.sprite.collide_rect(helicopter, skydiver):
            score += 1
            sound_safe.play()
            skydiver.rect.x = randint(80, win_width - 80)
            skydiver.rect.y = 0
            
        if pg.sprite.collide_rect(alien, skydiver):
            score -= 1
            sound_lost.play()
            skydiver.rect.x = randint(80, win_width - 80)
            skydiver.rect.y = 0
            
        if pg.sprite.collide_rect(helicopter, alien):            
            score = -STOP_SCORE
            sound_lost.play()
            
        if score <= -STOP_SCORE:
            win = False
            finish = True 
            
        if score >= STOP_SCORE:
            win = True
            finish = True
            
        helicopter.draw_sprite()
        helicopter.update()        
        skydiver.draw_sprite()
        skydiver.update()
        alien.draw_sprite()
        alien.update()
        score_text.set_text(5, 10, f'SCORE:  {score}', 24, (124, 103, 245))
        score_text.draw_text()
    
    if finish:
        window.blit(background, (0, 0)) 
        score_text.draw_text()
        again_text.draw_text()
        if win:
            win_text.draw_text() 
        else:
            lose_text.draw_text()
    
    pg.display.update()
    clock.tick(FPS)
    
