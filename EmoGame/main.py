from setup import *
import Spirit
import Candy

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('EmoGame')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bg_colour)

spirit = Spirit.Spirit()
candy = Candy.Candy()
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


