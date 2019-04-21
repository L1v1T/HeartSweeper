#coding=utf-8

import pygame
import random
from pygame.locals import *
#刷新率控制
FPSCLOCK = pygame.time.Clock()
time = 0

# pygame初始化
screen_size = (480, 640)
backgroundcolor = (255, 195, 205)
# 创建了一个窗口
pygame.init()
# 创建一个窗口
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption("扫雷")
# 设置窗口标题
# 背景填充
screen.fill(backgroundcolor)
my_font = pygame.font.SysFont('arialrounded', 20)
# 创建字体对象
losetext = "You Lose"
wintext = "You Win"
text_time = "Time:"
text_fps = "FPS:"
startbutton = "start"

table = [[0 for i in range(10)] for j in range(10)]
#生成坐标

remain = 100

gameover = 3
#游戏结束标志,1表示输，2表示赢,3表示游戏未开始

def create():

    for i in range(10):
        for j in range(10):
            table[i][j] = 0

    #生成地雷坐标
    count = 0   #地雷个数
    while count <= 9:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if table[x][y] != 9:
            table[x][y] = 9
            count = count + 1
    remain = count
    # 统计正下方雷
    for myx in range(0, 9):
        for myy in range(0, 10):
            if table[myx][myy] != 9:
                if table[myx + 1][myy] == 9:
                    table[myx][myy] = table[myx][myy] + 1
    # 统计正上方雷
    for myx in range(1, 10):
        for myy in range(0, 10):
            if table[myx][myy] != 9:
                if table[myx - 1][myy] == 9:
                    table[myx][myy] = table[myx][myy] + 1
    # 统计正左雷
    for myx in range(0, 10):
        for myy in range(1, 10):
            if table[myx][myy] != 9:
                if table[myx][myy - 1] == 9:
                    table[myx][myy] = table[myx][myy] + 1
    # 统计正右雷
    for myx in range(0, 10):
        for myy in range(0, 9):
            if table[myx][myy] != 9:
                if table[myx][myy + 1] == 9:
                    table[myx][myy] = table[myx][myy] + 1
    # 统计左上雷
    for myx in range(1, 10):
        for myy in range(1, 10):
            if table[myx][myy] != 9:
                if table[myx - 1][myy - 1] == 9:
                    table[myx][myy] = table[myx][myy] + 1
    # 统计右上方雷
    for myx in range(1, 10):
        for myy in range(0, 9):
            if table[myx][myy] != 9:
                if table[myx - 1][myy + 1] == 9:
                    table[myx][myy] = table[myx][myy] + 1
    # 统计左下方雷
    for myx in range(0, 9):
        for myy in range(1, 10):
            if table[myx][myy] != 9:
                if table[myx + 1][myy - 1] == 9:
                    table[myx][myy] = table[myx][myy] + 1
    # 统计右下方雷
    for myx in range(0, 9):
        for myy in range(0, 9):
            if table[myx][myy] != 9:
                if table[myx + 1][myy + 1] == 9:
                    table[myx][myy] = table[myx][myy] + 1


# 生成坐标
create()


class block_x7(object):
    x = 0
    y = 0   #坐标
    value = 0   #数值，value = 9表示地雷
    click_l = 0     #是否被左键点击,0表示被点击过了
    click_r = 0    #被右键点击的次数,click_r = 0 显示ok.jpg, click_r = 1 显示 sign.jpg

    def __init__(self, in_x, in_y, in_value, in_click_l = 0,in_click_r = 0):
        self.x = in_x
        self.y = in_y
        self.value = in_value
        self.click_l = in_click_l
        self.click_r = in_click_r
    def show(self):
        if self.click_l == 0:
            if self.click_r == 0:
                image = pygame.image.load('ok1.jpg')
                screen.blit(image, [self.x, self.y])
            else:
                if self.click_r == 1:
                    if gameover == 1:   #失败
                        if self.value == 9: #该格是地雷，标记正确
                            image = pygame.image.load('heart.jpg')
                        else:   #不是地雷，标记错误
                            image = pygame.image.load('faultsign.jpg')
                    elif gameover == 2:
                        image = pygame.image.load('heart.jpg')
                    elif gameover == 0:
                        image = pygame.image.load('sign.jpg')
                    screen.blit(image, [self.x, self.y])
                else:
                    image = pygame.image.load('unclear.jpg')
                    screen.blit(image, [self.x ,self.y])
        else:
            if self.value == 9:
                image = pygame.image.load('brokenheart.jpg')
                screen.blit(image, [self.x, self.y])
            else:
                im_srt = 'flag' + str(self.value) + '.jpg'
                image = pygame.image.load(im_srt)
                screen.blit(image, [self.x, self.y])

#实例化格子数组
block = []
# 给实例格子赋值
for i in range(10):
    for j in range(10):
        block.insert((i * 10) + j, block_x7(90 + (30 * i), 240 + (30 * j), table[i][j]))

#判断格子是有有上下左右格子
def upexist(x, y):
    if x == 0:
        return False
    else:
        return True
def downexist(x, y):
    if x == 9:
        return False
    else:
        return True
def leftexist(x, y):
    if y == 0:
        return False
    else:
        return True
def rightexist(x, y):
    if y == 9:
        return False
    else:
        return True


#左键点击后设置block_x7的click_l值
def set_clickl(set_x, set_y):
    global gameover
    global remain
    remain -= 1
    if block[(set_x * 10) + set_y].click_r == 0:
        block[(set_x * 10) + set_y].click_l = 1
        block[(set_x * 10) + set_y].show()
        if block[(set_x * 10) + set_y].value == 0:
            if upexist(set_x, set_y) and block[((set_x - 1) * 10) + set_y].click_l == 0:
                set_clickl(set_x - 1, set_y)
            if downexist(set_x, set_y) and block[((set_x + 1) * 10) + set_y].click_l == 0:
                set_clickl(set_x + 1, set_y)
            if leftexist(set_x, set_y) and block[(set_x * 10) + set_y - 1].click_l == 0:
                set_clickl(set_x, set_y - 1)
            if rightexist(set_x, set_y) and block[(set_x * 10) + set_y + 1].click_l == 0:
                set_clickl(set_x, set_y + 1)
            if upexist(set_x, set_y) and leftexist(set_x, set_y) and block[((set_x - 1) * 10) + set_y - 1].click_l == 0:
                set_clickl(set_x - 1, set_y - 1)
            if upexist(set_x, set_y) and rightexist(set_x, set_y) and block[((set_x - 1) * 10) + set_y + 1].click_l == 0:
                set_clickl(set_x - 1, set_y + 1)
            if downexist(set_x, set_y) and leftexist(set_x, set_y) and block[((set_x + 1) * 10) + set_y - 1].click_l == 0:
                set_clickl(set_x + 1, set_y - 1)
            if downexist(set_x, set_y) and rightexist(set_x, set_y) and block[((set_x + 1) * 10) + set_y + 1].click_l == 0:
                set_clickl(set_x + 1, set_y + 1)
        elif block[(set_x * 10) + set_y].value == 9:  # 失败
            gameover = 1
        elif remain == 10:  # 胜利
            gameover = 2


#开始按钮类
class button(object):
    start_x = 0
    start_y = 0
    replay_x = 0
    replay_y = 0
    start_click = 0     #开始按钮是否被点击
    replay_click = 0    #重开按钮是否被点击
    def __init__(self, int_sx, int_sy, int_sc = 0):
        self.start_x = int_sx
        self.start_y = int_sy
        self.start_click = 0
    #显示开始按钮
    def start_show(self):
        pygame.draw.rect(screen, [255, 255, 255], [self.start_x, self.start_y, 100, 50], 0)
        screen.blit(my_font.render(startbutton, True, (0, 0, 0), [255, 255, 255]), (self.start_x + 25, self.start_y + 15))
    #检测是否点击开始按钮
    def detect_start(self, pos):
        if pos[0] > self.start_x and pos[0] < self.start_x + 100 and pos[1] > self.start_y and pos[1] < self.start_y + 50:
            return 1
        else:
            return 0

#按钮实例化
button_s = button(190, 150)

def draw():
    #开始按钮
    button_s.start_show()

    #显示计时
    screen.blit(my_font.render(text_time + str(int(time)) + " ", True, (0, 0, 0),backgroundcolor), (200, 50))
    #显示方块
    for i in range(100):
        block[i].show()
    '''
    if gameover == 1:   #游戏结束，负
        screen.blit(my_font.render(losetext, True, (0, 0, 0), backgroundcolor), (190, 100))
    if gameover == 2: #游戏结束，赢
        screen.blit(my_font.render(wintext, True, (0, 0, 0), backgroundcolor), (200, 100))
    '''
def gameInit():
    global time
    global remain
    global gameover
    # 游戏初始化

    # 初始化游戏参数
    # time 表示游戏已进行的时间
    # remain 表示未打开的格子数量
    # gameover 表示游戏状态 0表示游戏进行中，1表示输，2表示赢，3表示游戏未开始
    time = 0
    remain = 100
    gameover = 3

    # 重新生成地雷分布
    create()
    for i in range(10):
        for j in range(10):
            block[(i * 10) + j].value = table[i][j]
            block[(i * 10) + j].click_l = 0
            block[(i * 10) + j].click_r = 0

    # 清屏
    pygame.draw.rect(screen, backgroundcolor, [190, 50, 290, 100], 0)

    # 绘制游戏界面
    draw()
    pygame.display.update()

gameInit()

gameFPS = 0

while True:
    # 游戏开始
    #处理点击事件
    event = pygame.event.poll()
    if event.type == QUIT:  # 关闭游戏
        exit()
      #重新开始游戏
    if event.type == MOUSEBUTTONDOWN and event.button == 1 and button_s.detect_start(event.pos) == 1:
        gameInit()
        gameover = 0
    if gameover == 0 \
            and event.type == MOUSEBUTTONDOWN \
            and event.pos[0] > 90 \
            and event.pos[0] < 390 \
            and event.pos[1] > 240 \
            and event.pos[1] < 540:  # 点击在有效范围内
        get_x = int((event.pos[0] - 90) / 30)
        get_y = int((event.pos[1] - 240) / 30)
        if block[(get_x * 10) + get_y].click_l == 0:  # 未被左键点击过
            if event.button == 1:  # 左键点击
                if block[(get_x * 10) + get_y].click_r == 0:
                    set_clickl(get_x, get_y)
            elif event.button == 3:  # 右键点击
                block[(get_x * 10) + get_y].click_r = (block[(get_x * 10) + get_y].click_r + 1) % 3
                block[(get_x * 10) + get_y].show()

    #计算时间
    time_passed = FPSCLOCK.tick()
    time_passed_seconds = time_passed / 1000.0
    if gameover == 0:
        time += time_passed_seconds

    gameFPS = FPSCLOCK.get_fps()

    #更新画面
    screen.blit(my_font.render(text_time + str(int(time)) + "  ", True, (0, 0, 0), backgroundcolor), (200, 50))
    screen.blit(my_font.render(text_fps + str(int(gameFPS)) + "  ", True, (0, 0, 0), backgroundcolor), (380, 10))
    pygame.display.update()

    if gameover == 1:   #游戏结束，负
        screen.blit(my_font.render(losetext, True, (0, 0, 0), backgroundcolor), (190, 100))
        for i in range(10):
            for j in range(10):
                if block[i * 10 + j].value == 9:
                    set_clickl(i, j)
                block[i * 10 + j].show()
        gameover = 3
    if gameover == 2: #游戏结束，赢
        for i in range(10):
            for j in range(10):
                if block[i * 10 + j].value == 9:
                    block[i * 10 + j].show()
        screen.blit(my_font.render(wintext, True, (0, 0, 0), backgroundcolor), (200, 100))
    pygame.display.update()
