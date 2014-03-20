from setup import *
import Spirit
import Slider

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Experiment Interface')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(bg_colour)

spirits = []

for i in range(0, num_spirit):
    spirit = Spirit.Spirit()
    spirits.append(spirit)
#candy = Candy.Candy()

#allsprites = pygame.sprite.RenderPlain(candy)
allsprites = pygame.sprite.RenderPlain()
for i in range(0, num_spirit):
    allsprites.add(spirits[i])


clock = pygame.time.Clock()
candy_start_time = pygame.time.get_ticks()

while 1:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit()
        '''
        elif event.type == MOUSEBUTTONDOWN:
            if not candy.candying:
                candy_start_time = pygame.time.get_ticks()
                candy.candy(spirit)


            for i in range(0, num_spirit):
                spirits[i].candyed(candy.rect, candy_start_time)

        elif event.type == MOUSEBUTTONUP:
            candy.uncandy()
            for i in range(0, num_spirit):
                spirits[i].uncandyed()

        elif event.type == VIDEORESIZE:
            size = event.size
        '''
    allsprites.update()

    screen.blit(background, (0, 0))
    allsprites.draw(screen)
    pygame.display.flip()


