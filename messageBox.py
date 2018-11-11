import pygame


class MessageBox():
    def __init__(self):
        self.image = pygame.image.load('image/message_box.jpg').convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, 0
        self.chara = None
        self.message = None
        self.show_message = False

    def render(self, text):
        myfont = pygame.font.Font(None, 60)
        text_image = myfont.render(text, True, (255, 255, 255))
        text_image_rect = text_image.get_rect()
        text_image_rect.left, text_image_rect.top = 10, 10
        self.image = pygame.image.load('image/message_box.jpg').convert()
        self.image.blit(text_image, text_image_rect)