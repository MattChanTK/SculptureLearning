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
        self.candy_start_time = 0

        # behaviour parameters for "walk"
        self.v = 6.0
        self.w = 0.05
        self.k_candy = 0

        # behaviour paremeters for "walk2"
        self.a_x = -0.02
        self.b_x = -0.00
        self.c_x = 5
        self.a_y = -0.00
        self.b_y = -0.02
        self.c_y = 5


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

        self.__walk2()

    def __walk(self):

        # calculate candy direction
        candy_dir = math.atan2(self.candy_rect.y - self.rect.y, self.candy_rect.x - self.rect.x)

        # calculate spirit direction
        spirit_dir = self.dir+self.w

         # wrapping direction from pi to -pi
        if spirit_dir  > math.pi:
            spirit_dir  = -math.pi
        elif spirit_dir  < -math.pi:
            spirit_dir  = math.pi


        # compute new angle
        self.dir = (1 - self.k_candy)*spirit_dir + self.k_candy*candy_dir


        # computing the new position
        dx = round(self.v*math.cos(self.dir))
        dy = round(self.v*math.sin(self.dir))
        newpos = self.rect.move(dx, dy)

        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right or \
               self.rect.top < self.area.top or self.rect.bottom > self.area.bottom:
                if self.dir > 0:
                    self.dir = self.dir - math.pi
                else:
                    self.dir = self.dir + math.pi
                newpos = self.rect.move(-dx, -dy)
        self.rect = newpos

    def __walk2(self):

        if not self.affected:
            # calculate spirit direction
            self.dir += self.w

            # computing the new position
            dx = round(self.v*math.cos(self.dir))
            dy = round(self.v*math.sin(self.dir))
            '''
            #random change in w and v
            self.v += (random.random() - 0.5) * 0.5
            self.w += (random.random() - 0.5) * 0.01
            '''
        else:
            candy_dt = pygame.time.get_ticks() - self.candy_start_time
            dx = self.a_x*(self.rect.x - self.candy_rect.x) + \
                 self.b_x*(self.rect.y - self.candy_rect.y) + \
                 self.c_x*math.cos(0.01*candy_dt)
            dy = self.a_y*(self.rect.x - self.candy_rect.x) + \
                 self.b_y*(self.rect.y - self.candy_rect.y) + \
                 self.c_y*math.sin(0.01*candy_dt)

            # random change in the coefficient
            self.a_x += (random.random() - 0.5) * 0.004
            self.b_x += (random.random() - 0.5) * 0.001
            self.c_x += (random.random() - 0.5) * 0.1
            self.a_y += (random.random() - 0.5) * 0.001
            self.b_y += (random.random() - 0.5) * 0.004
            self.c_y += (random.random() - 0.5) * 0.1

        newpos = self.rect.move(dx, dy)
        move_x = dx
        move_y = dy

        if not self.area.contains(newpos):

            if newpos.left < self.area.left or newpos.right > self.area.right:
                move_x = -dx
            if newpos.top > self.area.top or newpos.bottom < self.area.bottom:
                move_y = -dy

            newpos = self.rect.move(move_x, move_y)

        self.rect = newpos
        self.dir = math.atan2(move_y, move_x)



    def candyed(self, candy_rect, candy_start_time):
        if not self.affected:
            self.affected = 1
        self.candy_rect = candy_rect
        self.candy_start_time = candy_start_time

    def uncandyed(self):
        if self.affected:
            self.affected = 0

