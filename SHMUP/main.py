import pygame as pg
from pygame.locals import *

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


def main():
    left_go = False
    right_go = False
    space_go = False

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
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    left_go = False
                elif event.key == K_RIGHT:
                    right_go = False
        if left_go == True:
            player.x -= player.velocity
            if player.x <= 0:
                player.x = 0
        elif right_go == True:
            player.x += player.velocity
            if player.x >= size[0] - player.width:
                player.x = size[0] - player.width

        screen.fill(BLACK)
        player.show()
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