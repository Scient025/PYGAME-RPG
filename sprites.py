import pygame as pg
from config import*
import math 
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pg.image.load(file).convert()
        self.sheet.set_colorkey(BLACK)  # Set black as transparent color
       

    def get_sprite(self, x, y, width, height):
        sprite = pg.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        return sprite


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__(game.all_sprites)
        self.game = game
        self._layer = Player_layer
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize
        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 1
        self.image = self.game.character_spritesheet.get_sprite(1, 6, 15, 22)
        self.image.set_colorkey(BLACK)  # Set black as transparent color

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movement()
        self.animate() 
    
        self.image.set_colorkey(BLACK)
        self.collide_enemy()
         # Update the animation based on movement and direction

        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0


    def movement(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.x_change -= Player_speed
            self.facing = 'left'
        if keys[pg.K_d]:
            self.x_change += Player_speed
            self.facing = 'right'
            
        if keys[pg.K_w]:
            self.y_change -= Player_speed
            self.facing = 'up'
           
        if keys[pg.K_s]:
            self.y_change += Player_speed
            self.facing = 'down'
          


    def collide_enemy(self):
        hits = pg.sprite.spritecollide(self, self.game.enemies, False)

        if hits:
            self.kill()
            self.game.playing = False

    def collide_blocks(self, direction):
        hits = pg.sprite.spritecollide(self, self.game.blocks, False)
        if direction == 'x':
            for block in hits:
                if self.x_change > 0: #player moving right
                    self.rect.right = block.rect.left
                elif self.x_change < 0: #player moving left
                    self.rect.left = block.rect.right
        elif direction == 'y':
            for block in hits:
                if self.y_change > 0: #player moving down
                    self.rect.bottom = block.rect.top
                elif self.y_change < 0: #player moving up
                    self.rect.top = block.rect.bottom 
    
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(17, 6, 15, 22),
                           self.game.character_spritesheet.get_sprite(32, 6, 15, 22),
                           self.game.character_spritesheet.get_sprite(47, 6, 15, 22)]

        up_animations = [self.game.character_spritesheet.get_sprite(1, 67, 15, 22),
                         self.game.character_spritesheet.get_sprite(16, 67, 15, 22),
                         self.game.character_spritesheet.get_sprite(31, 67, 15, 22),
                         self.game.character_spritesheet.get_sprite(47, 67, 15, 22)]

        left_animations = [self.game.character_spritesheet.get_sprite(2, 101, 15, 22),
                           self.game.character_spritesheet.get_sprite(17, 101, 15, 22),
                           self.game.character_spritesheet.get_sprite(32, 101, 15, 22),
                           self.game.character_spritesheet.get_sprite(47, 101, 15, 22)]

        right_animations = [self.game.character_spritesheet.get_sprite(2, 37, 15, 22),
                            self.game.character_spritesheet.get_sprite(17, 37, 15, 22),
                            self.game.character_spritesheet.get_sprite(32, 37, 15, 22),
                            self.game.character_spritesheet.get_sprite(47, 37, 15, 22)]
        
        # Determine the animation based on direction
        if self.facing == 'down':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 6, 15, 22)
                self.image.set_colorkey(BLACK)
            else: 
                animation_index = math.floor(self.animation_loop) % len(down_animations)
                self.image = down_animations[animation_index]
                self.image = down_animations[animation_index]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1
                    self.image.set_colorkey(BLACK)
        
        if self.facing == 'up':
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 67, 15, 22)
                self.image.set_colorkey(BLACK)
            else: 
                animation_index = math.floor(self.animation_loop) % len(up_animations)
                self.image = up_animations[animation_index]
                self.image = up_animations[animation_index]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1
                    self.image.set_colorkey(BLACK)


        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(2, 37, 15, 22)
                self.image.set_colorkey(BLACK)
            else: 
                animation_index = math.floor(self.animation_loop) % len(right_animations)
                self.image = right_animations[animation_index]
                self.image = right_animations[animation_index]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1
                    self.image.set_colorkey(BLACK)

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(2, 101, 15, 22)
                self.image.set_colorkey(BLACK)
            else: 
                animation_index = math.floor(self.animation_loop) % len(left_animations)
                self.image = left_animations[animation_index]
                self.image = left_animations[animation_index]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 1
                    self.image.set_colorkey(BLACK)

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.groups = self.game.all_sprites, self.game.enemies  # Assign groups
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize


        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(8,40) # here the enemy moves randomly withing a range of 8 pixels by 40 pixels.

        self.image = self.game.enemy_spritesheet.get_sprite(3,2,32,32)
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

    def update(self):
        self.movement()
        self.animate()
        self.image.set_colorkey(BLACK)
        self.rect.x += self.x_change
        self.rect.y += self.y_change 

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == 'left':
            self.x_change -= Enemy_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing ='right' 

        if self.facing == 'right':
            self.x_change += Enemy_speed
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = 'left' 

    def animate(self):
        
        left_animations = [self.game.enemy_spritesheet.get_sprite(2,99,32,32),
                            self.game.enemy_spritesheet.get_sprite(35,99,32,32),
                            self.game.enemy_spritesheet.get_sprite(67,99,32,32),]

        right_animations = [self.game.enemy_spritesheet.get_sprite(2,67,32,32),
                            self.game.enemy_spritesheet.get_sprite(35,67,32,32),
                            self.game.enemy_spritesheet.get_sprite(67,67,32,32),]
        
        # Determine the animation based on direction
       
        if self.facing == 'right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3,2,32,32)
                self.image.set_colorkey(BLACK)
            else: 
                animation_index = math.floor(self.animation_loop) % len(right_animations)
                self.image = right_animations[animation_index]
                self.image = right_animations[animation_index]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                    self.image.set_colorkey(BLACK)

        if self.facing == 'left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(3,2,32,32)
                self.image.set_colorkey(BLACK)
            else: 
                animation_index = math.floor(self.animation_loop) % len(left_animations)
                self.image = left_animations[animation_index]
                self.image = left_animations[animation_index]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                    self.image.set_colorkey(BLACK)


        





class Block(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game = game
        self._layer = Block_layer
        self.groups = self.game.all_sprites, self.game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)


        self.x = x*tilesize
        self.y = y*tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = pg.Surface((self.width, self.height))
        self.image.blit(self.game.terrain_spritesheet.get_sprite(0,0,self.width,self.height), (0, 0))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ground(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = Ground_layer
        self.groups = self.game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)

        self.x = x * tilesize
        self.y = y * tilesize
        self.width = tilesize
        self.height = tilesize

        self.image = self.game.ground_spritesheet.get_sprite(0,0,16,16)
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.x
        self.rect.y = self.rect.y

class Attack(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()  # Call the superclass constructor
        self.game = game
        self._layer = Player_layer
        self.groups = self.game.all_sprites, self.game.attacks 
        pg.sprite.Sprite.__init__(self, self.groups)
        self.x = x
        self.y = y
        self.width = tilesize
        self.height = tilesize 

        self.animation_loop = 0
        self.image = self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y 

    def update(self):
        self.animate()
        self.collide()
        self.image.set_colorkey(BLACK)

    def collide(self):
        hits = pg.sprite.spritecollide(self,self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing 

        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        down_animations = [self.game.attack_spritesheet.get_sprite(0, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 32, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 32, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]

        up_animations = [self.game.attack_spritesheet.get_sprite(0, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(32, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(64, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(96, 0, self.width, self.height),
                         self.game.attack_spritesheet.get_sprite(128, 0, self.width, self.height)]

        if direction == 'up':
            self.image = up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 
            if self.animation_loop >=5:
                self.kill()

        if direction == 'down':
            self.image = down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 
            if self.animation_loop >=5:
                self.kill()

        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 
            if self.animation_loop >=5:
                self.kill()

        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5 
            if self.animation_loop >=5:
                self.kill()
   