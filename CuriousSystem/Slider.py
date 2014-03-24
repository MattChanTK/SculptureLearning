from setup import *

class Slider(pygame.sprite.Sprite):

    img1, rect1 = load_image('fist_icon.png')
    img2, rect2 = load_image('open_hand_icon.png')
    # resize the image
    #img1 = pygame.transform.scale(img1, candy_up_size)
    #img2 = pygame.transform.scale(img2, candy_down_size)
    # resize the rect
    #rect1.size = slider_up_size
    #rect2.size = candy_down_size

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = Slider.img1
        self.rect = Slider.rect1
        self.sliding = 0

    def update(self):
        "move the candy based on the mouse position"
        pos = pygame.mouse.get_pos()
        self.rect.midtop=pos
        #if self.candying:

    def candy(self, target):
        "returns true if the fist collides with the target"
        if not self.sliding:
            self.sliding = 1
            self.image = Slider.img2
            return self.rect.colliderect(target.rect)
    def uncandy(self):
        "called to pull the fist back"
        self.sliding = 0
        self.image = Slider.img1
