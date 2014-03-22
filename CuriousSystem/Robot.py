from setup import *
import random
import Motor
import Sensor
import Memory
import Exemplar

random.seed()

class Robot(pygame.sprite.Sprite):

    def __init__(self, this_robot_size=robot_size):

        # pygame parameters
        # call Sprite intializer
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('bluedot.jpg', -1)

        # resize the image
        self.image = pygame.transform.scale(self.image, robot_size)
        # resize the rect
        self.rect.size = this_robot_size

        # copy the screen
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()

        # state of the robot
        self.x = random.randint(self.area.left, self.area.right)
        self.y = random.randint(self.area.top, self.area.bottom)
        self.dir = random.random()*math.pi*2

        # randomize the initial location of the dot
        self.rect.x = self.x
        self.rect.y = self.y

        self.motor = Motor.Motor()
        self.sensor = Sensor.Sensor()

        # instantiate the robot's memory
        self.memory = Memory.Memory()

    def update(self, user):

        # Sense the user
        self.__sense(user)
        s1 = self.sensor
        # select action
        self.__act()
        m = self.motor
        # perform action
        self.__move()
        # check for actuation sensor inputs
        self.__sense(user)
        s2 = self.sensor

        self.memory.addExemplar(s1, m, s2)

        self.printRegionPop();


    def __move(self):

        # calculate robot direction
        self.dir += self.motor.w

        # computing the new position
        dx = self.motor.v*math.cos(self.dir)
        dy = self.motor.v*math.sin(self.dir)

        # updating pygame rect position
        newpos = self.rect.move(dx, dy)

        # check if it hits hall
        move_x = dx
        move_y = dy
        if not self.area.contains(newpos):
            # change direction if it does
            if newpos.left < self.area.left or newpos.right > self.area.right:
                move_x = -dx
            if newpos.top > self.area.top or newpos.bottom < self.area.bottom:
                move_y = -dy

            newpos = self.rect.move(move_x, move_y)
        self.rect = newpos

        # updating state
        self.x += move_x
        self.y += move_y

        # calculate new direction (will change if it hits wall)
        self.dir = math.atan2(move_y, move_x)

    def __sense(self, user):
        self.sensor.hr = user.hr
        self.sensor.skin = user.skin
        self.sensor.interest = user.interest

    def __act(self):
        self.motor.v = self.sensor.hr/8
        self.motor.w = self.sensor.interest/0.2

    def setState(self, new_x=None, new_y=None, new_dir=None):
        if new_x is not None:
            self.x = new_x

        if new_y is not None:
            self.y = new_y

        if new_dir is not None:
            self.dir = new_dir

        self.rect.x = self.x
        self.rect.y = self.y

    def printRegionPop(self):
        print len(self.memory.exp), '-->'
        self.memory.R.getNumExemplarRecursive()
        print('-----------')