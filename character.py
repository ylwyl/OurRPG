import pygame


class Character(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # self.target_surface = target
        ## 当前帧图片
        self.image = None
        ## 移动序列图
        self.master_image = None
        self.rect = None
        ## 用于设置初始位置
        self.left, self.top = 0, 0
        ## 序列图列数
        self.columns = 0
        ## direction  up=3, right=2, left=1, down=0
        self.direction = 0
        ## 当前所在帧
        self.frame = 0
        self.old_frame = -1
        ## 每一帧图片宽、高
        self.frame_width = 0
        self.frame_height = 0
        ## 用于帧数循环
        self.first_frame = 0
        self.last_frame = 0
        self.last_time = 0
        ## 是否处于移动状态
        self.moving = False
        ## speed
        self.speed = [0, 0]
        ## 用于碰撞检测
        self.mask = None
        """角色交互点"""
        self.check_point = None
        self.messages = []
        self.event_flag = False

    def load(self, filename, width, height, columns):
        self.master_image = pygame.image.load(filename).convert_alpha()
        self.frame_width = width
        self.frame_height = height
        image = pygame.Surface([self.frame_width, self.frame_height])
        image.set_colorkey((0, 0, 0))
        image.blit(self.master_image, (0, 0), (0, 0, self.frame_width, self.frame_height))
        self.rect = image.get_rect()
        self.rect.left, self.rect.top = self.left, self.top
        # self.rect = self.left, self.top, self.frame_width, self.frame_height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1

    def update(self, current_time, rate):
        ## 该方向上始末帧
        self.first_frame = self.direction * self.columns
        self.last_frame = self.first_frame + self.columns - 1
        ## 当前帧图不在该方向上第一张
        if self.frame < self.first_frame:
            self.frame = self.first_frame
        ## 每rate换一帧
        if self.moving:
            if current_time > self.last_time + rate:
                self.frame += 1
                if self.frame > self.last_frame:
                    self.frame = self.first_frame
                self.last_time = current_time
        if self.frame != self.old_frame:
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = (frame_x, frame_y, self.frame_width, self.frame_height)
            self.image = self.master_image.subsurface(rect)
            self.mask = pygame.mask.from_surface(self.image)
            self.old_frame = self.frame
            self.check_point = self.rect.left - self.rect.width, self.rect.left + self.rect.width,\
                               self.rect.top - self.rect.height, self.rect.top + self.rect.height

    def go_up(self):
        self.moving = True
        ## 确定方向
        self.direction = 3
        self.speed = [0, -2]
        ## 改变位置
        self.rect = self.rect.move(self.speed)

    def go_down(self):
        self.moving = True
        self.direction = 0
        self.speed = [0, 2]
        self.rect = self.rect.move(self.speed)

    def go_left(self):
        self.moving = True
        self.direction = 1
        self.speed = [-2, 0]
        self.rect = self.rect.move(self.speed)

    def go_right(self):
        self.moving = True
        self.direction = 2
        self.speed = [2, 0]
        self.rect = self.rect.move(self.speed)


