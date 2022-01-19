import pygame as pg
from pygame.locals import *
import random

BLACK = (0, 0, 0)

class Character:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velocity = 0
    
    def put_img(self, address):
        if address[-3:] == "png":
            self.img = pg.image.load(address).convert_alpha()
        else:
            self.img = pg.image.load(address)
        self.width, self.height = self.img.get_size()
    
    def change_size(self, width, height):
        self.img = pg.transform.scale(self.img, (width, height))
        self.width, self.height = self.img.get_size()
    
    def show(self):
        screen.blit(self.img, (self.x, self.y))

class Enemy(Character):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.velocity = 0
        self.hp = 0

def crash(a, b):
    if (a.x - b.width + 10 <= b.x <= a.x + a.width - 10 and 
        a.y - b.height + 10 <= b.y <= a.y + a.height - 10):
        return True
    else:
        return False

      
def main():
    left_go = False
    right_go = False
    space_go = False
    k = 0

    attacks = []
    enemies = []

    player = Character()
    player.put_img("image/fighter.png")
    player.change_size(70, 70)
    player.x = round(size[0] / 2) - round(player.width / 2)
    player.y = size[1] - player.height - 15
    player.velocity = 5

    running = True
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
                return running
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    left_go = True
                elif event.key == K_RIGHT:
                    right_go = True
                elif event.key == K_SPACE:
                    space_go = True
                    k = 0
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    left_go = False
                elif event.key == K_RIGHT:
                    right_go = False
                elif event.key == K_SPACE:
                    space_go = False
        if left_go == True:
            player.x -= player.velocity
            if player.x <= 0:
                player.x = 0
        elif right_go == True:
            player.x += player.velocity
            if player.x >= size[0] - player.width:
                player.x = size[0] - player.width
        
        if space_go == True and k % 15 == 0:
            lightning = Character()
            lightning.put_img("image/lightning.png")
            lightning.change_size(50, 50)
            lightning.x = round(player.x + (player.width - lightning.width) / 2)
            lightning.y = player.y
            lightning.velocity = 12
            attacks.append(lightning)
        k += 1

        garbage = []
        for i in range(len(attacks)):
            attack = attacks[i]
            attack.y -= attack.velocity
            if attack.y <= -attack.height:
                garbage.append(i)
        garbage.reverse()
        for i in garbage:
            del attacks[i]
    
        if random.random() > 0.98:
            mob = Enemy()
            mob.put_img("image/enemy1.png")
            mob.change_size(60, 60)
            mob.x = random.randrange(0, size[0] - mob.width - round(player.width / 2))
            mob.y = 10
            mob.velocity = random.randrange(3, 7)
            mob.hp = 1
            enemies.append(mob)
        
        if random.random() > 0.998:
            boss = Enemy()
            boss.put_img("image/enemy2.png")
            boss.change_size(150, 130)
            boss.x = random.randrange(0, size[0] - boss.width - round(player.width / 2))
            boss.y = 10
            boss.velocity = 1
            boss.hp = 10
            enemies.append(boss)

        garbage = []  # 초기화
        for i in range(len(enemies)):
            enemy = enemies[i]
            enemy.y += enemy.velocity
            if enemy.y >= size[1]:
                garbage.append(i)
        garbage.reverse()
        for i in garbage:
            del enemies[i]

        crashed_attacks, crashed_enemies = [], []
        for i in range(len(attacks)):
            for j in range(len(enemies)):
                attack, enemy = attacks[i], enemies[j]
                if crash(attack, enemy):
                    crashed_attacks.append(i)
                    crashed_enemies.append(j)
                    enemy.hp -= 1

        crashed_attacks = list(set(crashed_attacks))
        crashed_enemies = list(set(crashed_enemies))
        crashed_attacks.reverse()
        crashed_enemies.reverse()

        for i in crashed_attacks:
            del attacks[i]
        for i in crashed_enemies:
            if enemies[i].hp == 0:
                if enemies[i].width == 60:
                    del enemies[i]
                else:
                    del enemies[i]
        for i in range(len(enemies)):
            enemy = enemies[i]
            if crash(enemy, player):
                running = False # while문 종료

        screen.fill(BLACK)
        player.show()
        for attack in attacks:
            attack.show()
        for enemy in enemies:
            enemy.show()
        pg.display.flip()


if __name__ == "__main__":
    pg.init()
    clock = pg.time.Clock()
    size = [500, 800]
    screen = pg.display.set_mode(size)
    title = "Shoot'Em Up!!"
    pg.display.set_caption(title)

    while True:
        going = main()
        if not going:
            break
    pg.quit()