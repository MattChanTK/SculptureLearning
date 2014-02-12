from setup import *
import random

random.seed()

class Spirit(pygame.sprite.Sprite):

    def __init__(self, spirit_size = spirit_size):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = load_image('bluedot.jpg', -1)

        # resize the image
        self.image = pygame.transform.scale(self.image, spirit_size)
        # resize the rect
        self.rect.size = spirit_size

        # copy the screen
        screen = pygame.display.get_surface()

        self.area = screen.get_rect()

        #randomize the initial location of the dot
        self.rect.move_ip(random.randint(self.area.left, self.area.right),
                          random.randint(self.area.top, self.area.bottom))

        # behaviour parameters
        self.v = 6.0
        self.w = 0.05

        # internal parameters
        self.dir = random.random()*math.pi*2

        self.dizzy = 0

    def update(self):
        "walk or spin, depending on the monkeys state"
        if self.dizzy:
            self.__spin()
        else:
            self.__walk()

    def __walk(self):

        # compute new angle
        self.dir += self.w
        dx = round(self.v*math.cos(self.dir))
        dy = round(self.v*math.sin(self.dir))
        newpos = self.rect.move(dx, dy)

        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right or \
               self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
                self.dir = self.dir - math.pi
                newpos = self.rect.move(-dx, -dy)
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
