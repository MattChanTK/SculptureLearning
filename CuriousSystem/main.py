from setup import *
import Robot
import Simson
import Slider


# pygame set up
pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Experiment Interface')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bg_colour)

# instantiate robots
robots = []
for i in range(0, num_robot):
    robot = Robot.Robot()
    robots.append(robot)

# instantiate user
user = Simson.Simson()

# add elements to pygame space
allRobots = pygame.sprite.Group()

for i in range(0, num_robot):
    allRobots.add(robots[i])

#timing
clock = pygame.time.Clock()

while 1:

    clock.tick(fps)

    # pygame update
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()


    # robots move
    allRobots.update(user)

    # user reacts to the animation
    num_robot = 0
    for robot in pygame.sprite.Group.sprites(allRobots):
        # just average speed for now
        hrFea = abs(robot.motor.v)
        # distance to centre
        skinFea = abs(robot.motor.v*robot.motor.w)
        # average angular velocity
        interestFea = abs(robot.motor.w/(math.pi/4))
        num_robot += 1
        #print robot.memory.R.getNumRegion()
    fea = [hrFea/num_robot, skinFea/num_robot, interestFea/num_robot]

    user.react(fea)


    screen.blit(background, (0, 0))
    allRobots.draw(screen)

    pygame.display.flip()


