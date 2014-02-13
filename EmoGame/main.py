from setup import *
import Spirit
import Candy

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Mist of Spirits')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bg_colour)

spirits = []

for i in range(0, num_spirit):
    spirit = Spirit.Spirit()
    spirits.append(spirit)
candy = Candy.Candy()

allsprites = pygame.sprite.RenderPlain(candy)
for i in range(0, num_spirit):
    allsprites.add(spirits[i])


clock = pygame.time.Clock()

while 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            candy.candy(spirit)
            for i in range(0, num_spirit):
                spirits[i].candyed(candy.rect)

        elif event.type == MOUSEBUTTONUP:
            candy.uncandy()
            for i in range(0, num_spirit):
                spirits[i].uncandyed()

        elif event.type == VIDEORESIZE:
            size = event.size

    allsprites.update()

    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()


