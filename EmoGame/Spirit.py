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
        self.candy_rect = self.rect

        # behaviour parameters
        self.v = 6.0
        self.w = 0.05
        self.k_candy = 0

        # internal parameters
        self.dir = random.random()*math.pi*2

        self.affected = 0


    def update(self):

        if self.affected:
            self.k_candy += candy_factor_rate
            if self.k_candy > 1:
                self.k_candy = 1
        else:
            self.k_candy -= candy_factor_rate*5
            if self.k_candy < 0:
                self.k_candy = 0

        self.__walk()

    def __walk(self):

        # calculate candy direction
        candy_dir = math.atan2(self.candy_rect.y - self.rect.y, self.candy_rect.x - self.rect.x)

        # compute new angle
        self.dir = (1 - self.k_candy)*(self.dir+self.w) + self.k_candy*candy_dir

        # wrapping direction to 2*pi
        self.dir = math.fmod(self.dir, 2*math.pi)
        print self.dir
        # computing the new position
        dx = round(self.v*math.cos(self.dir))
        dy = round(self.v*math.sin(self.dir))
        newpos = self.rect.move(dx, dy)

        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right or \
               self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
                self.dir = self.dir - math.pi
                newpos = self.rect.move(-dx, -dy)
        self.rect = newpos


    def candyed(self, candy_rect):
        if not self.affected:
            self.affected = 1
        self.candy_rect = candy_rect

    def uncandyed(self):
        if self.affected:
            self.affected = 0

