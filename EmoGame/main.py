import os, sys
import pygame
from pygame.locals import *
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'
import math


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    #image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound


class Candy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image, self.rect = load_image('ball.gif')
        self.candying = 0

    def update(self):
        "move the candy based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop=pos
        if self.candying:
            self.rect.move_ip(5,10)
    def candy(self, target):
        "returns true if the fist collides with the target"
        if not self.candying:
            self.candying = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)
    def uncandy(self):
        "called to pull the fist back"
        self.candying = 0

class Spirit(pygame.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('ball.gif', -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self.__spin()
        else:
            self.__walk()

    def __walk(self):
        "move the monkey across the screen, and turn at the ends"
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, 1, 0)
            self.rect = newpos

    def __spin(self):
        "spin the monkey image"
        center = self.rect.center
        self.dizzy += 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        "this will cause the monkey to start spinning"
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image

pygame.init()
size = (800, 100)
screen = pygame.display.set_mode(size, pygame.RESIZABLE)
pygame.display.set_caption('EmoGame')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

if pygame.font:
    font = pygame.font.Font(None, 36)
    text = font.render("Feed the spirit", 1, (10, 10, 10))
    textpos = text.get_rect(centerx=background.get_width()/2)
    background.blit(text, textpos)

spirit = Spirit()
candy = Candy()
allsprites = pygame.sprite.RenderPlain((candy, spirit))
clock = pygame.time.Clock()

while 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if candy.candy(spirit):
                spirit.punched()
        elif event.type == MOUSEBUTTONUP:
            candy.uncandy()
        elif event.type == VIDEORESIZE:
            size = event.size

    allsprites.update()

    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()


