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
dx = 0
while 1:
    clock.tick(60)

    # pygame update
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()

    allRobots.update(user)

   # user reacts to the animation
    num_robot = 0
    for robot in pygame.sprite.Group.sprites(allRobots):
        # just average speed for now
        hrFea = robot.motor.v
        # distance to centre
        skinFea = math.sqrt((robot.x - size[0]/2)**2 + (robot.y - size[1]/2)**2)
        # average angular velocity
        interest = robot.motor.w
        num_robot += 1
    fea= [hrFea/num_robot, skinFea/num_robot, interest/num_robot]
    user.react(fea)




    screen.blit(background, (0, 0))
    allRobots.draw(screen)

    pygame.display.flip()


