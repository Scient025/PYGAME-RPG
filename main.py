import pygame as pg
import sys
from sprites import *
from config import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption('Minos')
        self.clock = pg.time.Clock()
        self.camera = pg.Rect(0, 0, width, height)  # Initialize camera
        self.running = True
        self.character_spritesheet = Spritesheet('C:\\Users\\bhate\\OneDrive\\Documents\\sem4\\mini\\gfx\\character.png')
        self.terrain_spritesheet = Spritesheet('C:\\Users\\bhate\\OneDrive\\Documents\\sem4\\mini\\gfx\\tri.png')
        self.ground_spritesheet = Spritesheet('C:\\Users\\bhate\\OneDrive\\Documents\sem4\\mini\gfx\\Overworld.png')
        self.enemy_spritesheet = Spritesheet("C:\\Users\\bhate\\OneDrive\\Documents\\sem4\\mini\\gfx\\enemy.png")
        self.attack_spritesheet = Spritesheet("C:\\Users\\bhate\\OneDrive\\Documents\\sem4\\mini\\gfx\\attack.png")
    
    def createTilemap(self):
        for i, row in enumerate(tilemap):
            for j, col in enumerate(row):
                if col == 'x':
                    Block(self, j, i)  # Render blocks
                elif col == 'p':
                    self.player = Player(self, j, i)  # Render player
                elif col == ' ':  # Empty space for ground
                    Ground(self, j, i)  # Render ground
                elif col == 'E':
                    Enemy(self,j,i)

                  

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.blocks = pg.sprite.LayeredUpdates()
        self.enemies = pg.sprite.LayeredUpdates()
        self.attacks = pg.sprite.LayeredUpdates()
        self.createTilemap()
        self.playing = True

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): 
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                if self.player.facing == 'up':
                    attack = Attack(self, self.player.rect.x, self.player.rect.y - tilesize)
                    self.attacks.add(attack)
                if self.player.facing == 'down':
                    attack = Attack(self, self.player.rect.x, self.player.rect.y + tilesize)
                    self.attacks.add(attack)
                if self.player.facing == 'right':
                    attack = Attack(self, self.player.rect.x + tilesize, self.player.rect.y)  
                    self.attacks.add(attack)
                if self.player.facing == 'left':
                    attack = Attack(self, self.player.rect.x - tilesize, self.player.rect.y)
                    self.attacks.add(attack)



    def update(self):
        self.all_sprites.update()
        

    def draw(self):
        # Fill the screen with the ground texture
        for y in range(0, height, 16):
            for x in range(0, width, 16):
                ground_texture = self.ground_spritesheet.get_sprite(0, 0, 16, 16)
                self.screen.blit(ground_texture, (x, y))

        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pg.display.update()

    def introscreen(self):
        pass

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.running = False 
g = Game()
g.introscreen()
g.new()
while g.running:
    g.main()

pg.quit()
sys.exit()  