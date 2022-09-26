from pygame import *
import random

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()
        self.surf = transform.scale(image.load(player_image),(40, 60))
        self.x = player_x
        self.y = player_y
        self.rect = self.surf.get_rect()
        self.rect.x = self.x 
        self.rect.y = self.y
    
    def reset(self):
        window.blit(self.image, (self.x, self.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, move_right, move_left, move_up, move_down):
        GameSprite.__init__(self, player_image, player_x, player_y)
        self.move_right = move_right
        self.move_left = move_left
        self.move_up = move_up
        self.move_down = move_down

    def update(self):
        keys = key.get_pressed()
        if keys[self.move_left] and self.x > 5:
            self.x -= 5
        if keys[self.move_right] and self.x < 950:
            self.x += 5
        if keys[self.move_up] and self.y > 5:
            self.y -= 5
        if keys[self.move_down] and self.y < 630:
            self.y += 5
        self.rect.x = self.x 
        self.rect.y = self.y

class Enemy(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = Surface((15, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

window = display.set_mode((1000, 700))

display.set_caption("Cat VS Dog")

background = transform.scale(image.load("images/bg.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

clock = time.Clock()

mixer.init()
mixer.music.load('sounds/music.mp3')
mixer.music.play(-1)

ADDENEMY = USEREVENT + 1
time.set_timer(ADDENEMY, 250)

cat = Player('images/cat.png', 5, 5, K_RIGHT, K_LEFT, K_UP, K_DOWN)
dog = Player('images/dog.png', 5, 630, K_d, K_a, K_w, K_s)

enemies = sprite.Group()
all_sprites = sprite.Group()
all_sprites.add(cat)
all_sprites.add(dog)
players = sprite.Group()
players.add(cat)
players.add(dog)

FPS = 60

game = True

while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        elif e.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    cat.update()
    dog.update()
    enemies.update()

    window.blit(background,(0, 0))

    for entity in all_sprites:
        window.blit(entity.surf, entity.rect)

    if sprite.spritecollideany(cat, enemies):
        cat.kill()

    elif sprite.spritecollideany(dog, enemies):
        dog.kill()
    
    if not players:
        game = False

    display.update()
    clock.tick(FPS)