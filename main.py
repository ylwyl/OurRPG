import pygame
import sys
import traceback
from pygame import *
from character import *
from map import *
from building import *
from entrance import *
from bag import *
from item import *
from messageBox import *
"""--------碰撞检测会卡位，飞到另一边;贴图全是基于屏幕QAQ---------"""
"""initial"""
pygame.init()
pygame.mixer.init()
bg_size = width, height = 1000, 600
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("MyRPG")

"""this is our main character"""
main_chara = Character()
main_chara.load('image/male.png', 32, 48, 4)

""""将主角单独加入一组？"""
chara_group = pygame.sprite.Group()
chara_group.add(main_chara)
chara_group.update(pygame.time.get_ticks(), 120)

"""创建角色， 指定初始位置(相对屏幕)"""
"""测试人员QwQ"""
chara_1 = Character()
chara_1.load('image/female.png', 32, 48, 4)
chara_1.rect.left, chara_1.rect.top = 500, 250
chara_1.messages.append('ugly code')
chara_1.messages.append('I want your plane')

"""加载地图，文件地址， 绘制坐标， 人物起始位置"""
map1 = Map('image/map1.png', 0, 0, 300, 500)
map2 = Map('image/inner1.jpg', 250, 0, 365, 370)

"""为地图添加建筑，人物，物品（数字为相对地图位置，非屏幕）"""
"""entrance:交互点， 通往地图、及位置"""
map1.add_building(Building('image/house1.png', [146+map1.rect.left, 6+map1.rect.top]))
map1.add_entrance(Entrance(295+map1.rect.left, 305+map1.rect.left, 400+map1.rect.top,\
                           420+map1.rect.top, map2, 365+map2.rect.left, 370+map2.rect.top))
map2.add_entrance(Entrance(355+map2.rect.left, 420+map2.rect.left, 420+map2.rect.top,\
                           450+map2.rect.top, map1, 300+map1.rect.left, 444+map1.rect.top))
map2.add_chara(chara_1)

"""建立背包"""
bag = Bag(bg_size)
"""测试物品"""
plane = Item('image/enemy0.png', '飞机', '捡到的飞机,或许可以发射子弹~~', \
             (350+map2.rect.left, 250+map2.rect.top))
plane_2 = Item('image/plane.png', '又一架飞机', '捡到的飞机,究竟是谁打下来的~~', \
             (150+map2.rect.left, 250+map2.rect.top))
"""地图物品"""
map2.items.add(plane)
map2.items.add(plane_2)

"""添加到背包"""
"""对话框"""
message_box = MessageBox()


def collide_test(main_chara, c_map):
    """人物与建筑碰撞"""
    if pygame.sprite.spritecollide(main_chara, c_map.buildings, False, pygame.sprite.collide_mask):
        return True
    """人物与物品碰撞"""
    if pygame.sprite.spritecollide(main_chara, c_map.items, False, pygame.sprite.collide_mask):
        return True
    """人物与人物碰撞"""
    if pygame.sprite.spritecollide(main_chara, c_map.charas, False, pygame.sprite.collide_mask):
        return True
    return False


def at_point(main_chara, point):
    """人物处于某交互点"""
    if point[0] <= main_chara.rect.left <= point[1] and point[2] <= main_chara.rect.top <= point[3]:
        return True
    else:
        return False


def main():
    """设置时钟"""
    frame_rate = pygame.time.Clock()
    """???"""
    message_tick = 0
    """初始地图及初始位置"""
    c_map = map1
    main_chara.rect.left = c_map.start_left
    main_chara.rect.top = c_map.start_top

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            """松开方向键，停止加载移动图"""
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    main_chara.moving = False
                if event.key == K_UP:
                    main_chara.moving = False
                if event.key == K_DOWN:
                    main_chara.moving = False
                if event.key == K_LEFT:
                    main_chara.moving = False
            if event.type == KEYDOWN:
                if event.key == K_x:
                    if c_map == map2:
                        """按x与当前地图物品交互"""
                        for each in map2.items:
                            """添加物品进入背包"""
                            if at_point(main_chara, each.check_point):
                                bag.add_item(each)
                                each.taked = True
                                map2.items.remove(each)
                if event.key == K_c:
                    """按c与人物互动"""
                    if c_map == map2:
                        for each in map2.charas:
                            if at_point(main_chara, each.check_point):
                                message_tick = pygame.time.get_ticks()
                                message_box.show_message = True
                                if plane_2.taked:
                                    message_box.render(chara_1.messages[1])
                                    plane_2.taked = False
                                    bag.items.remove(plane_2)
                                    bag.bag_details = pygame.image.load('image/bag_detail.jpg')
                                else:
                                    message_box.render(chara_1.messages[0])

            if event.type == MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                """鼠标点击， 展开、折叠背包"""
                if bag.rect.left <= pos_x <= bag.rect.right and \
                        bag.rect.top <= pos_y <= bag.rect.bottom:
                    bag.show_details = not bag.show_details

        """获取按键"""
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_RIGHT]:
            main_chara.go_right()
            """发生碰撞，该方向上退两个像素"""
            while collide_test(main_chara, c_map):
                main_chara.rect.right -= 2
        if key_pressed[K_UP]:
            main_chara.go_up()
            while collide_test(main_chara, c_map):
                main_chara.rect.top += 2
        if key_pressed[K_LEFT]:
            main_chara.go_left()
            while collide_test(main_chara, c_map):
                main_chara.rect.left += 2
        if key_pressed[K_DOWN]:
            main_chara.go_down()
            while collide_test(main_chara, c_map):
                main_chara.rect.bottom -= 2


        """设置帧率"""
        frame_rate.tick(60)
        """获取当前时间"""
        ticks = pygame.time.get_ticks()
        """绘制当前地图"""
        screen.fill((0, 0, 0))
        screen.blit(c_map.image, c_map.rect)
        for each in c_map.buildings:
            screen.blit(each.image, each.rect)
        for each in c_map.items:
            if not each.taked:
                screen.blit(each.image, each.rect)
        """当前位于map1"""
        if c_map == map1:
            for each in map1.entrances:
                """主角位于entrance"""
                if at_point(main_chara, each.check_point):
                    """切换地图"""
                    c_map = each.next_map
                    screen.fill((0, 0, 0))
                    main_chara.rect.left = each.to_point[0]
                    main_chara.rect.top = each.to_point[1]

        if c_map == map2:
            """人物交互???"""
            # test
            # if main_chara.rect.left > chara_1.rect.left:
            #     chara_1.go_right()
            map2.charas.update(pygame.time.get_ticks(), 120)
            map2.charas.draw(screen)
            for each in map2.entrances:
                if at_point(main_chara, each.check_point):
                    c_map = each.next_map
                    screen.fill((0, 0, 0))
                    main_chara.rect.left = each.to_point[0]
                    main_chara.rect.top = each.to_point[1]

        """更新主角儿"""
        if main_chara.moving:
            chara_group.update(ticks, 120)
        chara_group.draw(screen)

        """"绘制背包"""
        screen.blit(bag.image, bag.rect)
        if bag.show_details:
            bag.blit_items()
            screen.blit(bag.bag_details, bag.bag_details_rect)

        """绘制对话框"""
        if ticks > message_tick + 1200:
            message_box.show_message = False
        if message_box.show_message:
            screen.blit(message_box.image, message_box.rect)
        """更新画面"""
        pygame.display.update()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()