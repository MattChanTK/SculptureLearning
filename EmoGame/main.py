from setup import *
import Spirit


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

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('EmoGame')
pygame.mouse.set_visible(0)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((200, 250, 250))

spirit = Spirit.Spirit()
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


