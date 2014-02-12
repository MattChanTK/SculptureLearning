from setup import *

class Candy(pygame.sprite.Sprite):

    img1, rect1 = load_image('fist_icon.png')
    img2, rect2 = load_image('open_hand_icon.png')
    # resize the image
    img1 = pygame.transform.scale(img1, candy_up_size)
    img2 = pygame.transform.scale(img2, candy_down_size)
    # resize the rect
    rect1.size = candy_up_size
    rect2.size = candy_down_size

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = Candy.img1, Candy.rect1
        self.candying = 0

    def update(self):
        "move the candy based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop=pos
        #if self.candying:

    def candy(self, target):
        "returns true if the fist collides with the target"
        if not self.candying:
            self.candying = 1
            self.image = Candy.img2
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)
    def uncandy(self):
        "called to pull the fist back"
        self.candying = 0
        self.image = Candy.img1
