import pygame


class Bag():
    def __init__(self, bg_size):
        self.image = pygame.image.load('image/bag.jpg').convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = bg_size[0] - self.rect.width - 10, 10
        self.bag_details = pygame.image.load('image/bag_detail.jpg')
        self.bag_details_rect = self.bag_details.get_rect()
        self.bag_details_rect.left, self.bag_details_rect.top = \
            bg_size[0] - self.bag_details_rect.width - 10, self.rect.height + 10
        self.items = []
        self.show_details = False

    def add_item(self, item):
        self.items.append(item)

    def blit_items(self):
        for index, each in enumerate(self.items):
            each.rect.left, each.rect.top = 0, index*47 + 5
            self.bag_details.blit(each.image, each.rect)
