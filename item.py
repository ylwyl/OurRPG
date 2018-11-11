import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, filename, name, introduction, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position[0], position[1]
        self.check_point = self.rect.left - self.rect.width, self.rect.left + self.rect.width, \
                           self.rect.top - self.rect.height, self.rect.top + self.rect.height
        self.name = name
        self.introduction = introduction
        self.mask = pygame.mask.from_surface(self.image)
        self.taked = False
