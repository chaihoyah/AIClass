import pygame as pg
from pygame.locals import *
import sys
import numpy as np
from DDopago import *

#게임 관련 변수 설정
player = 0 #흑 0 , 백 1
timeLimit = 10 # 시간 제한(초), 기본 10초
isFinished = False
isPlayerturn = True
board_img = pg.image.load('Images/OmokBoard.png')

pg.init()
# pygame 관련 변수 설정
board_color = (153, 102, 000)
bg_color = (150, 150, 150)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 50, 255)

window_width = 800 #18*40 각 칸 40
window_height = 800
board_width = 600
board_size = 19
grid_size = 30
empty = 0
black_stone = 1
white_stone = 2
tie = 100

moves = list() #모든 움직임 저장 list

screen = pg.display.set_mode((window_width, window_height))
screen.fill(white)

#오목판 흑 1, 백 2, None 0
board = np.zeros((19,19)).astype(int)

#게임 관련 변수 설정
player = 0 #흑 0 , 백 1
timeLimit = 10 # 시간 제한(초), 기본 10초
isFinished = False
board_img = pg.image.load('Images/OmokBoard.png')
board_img = pg.transform.scale(board_img,(720,720))
whitestone_img = pg.image.load('Images/WhiteStone.png')
whitestone_img = pg.transform.scale(whitestone_img,(36,36))
blackstone_img = pg.image.load('Images/BlackStone.png')
blackstone_img = pg.transform.scale(blackstone_img,(36,36))

def gameSet():
    global player
    global timeLimit

    player = int(input('흑백 선택: 흑이면 0, 백이면 1 입력'))
    if player != 0 and player != 1:
        player = 0

    timeLimit = int(input('시간 제한(초)을 정수로 입력해주세요'))

    print("게임을 시작합니다")
    gameStart()


# 게임 시작
def gameStart():
    global player
    global board_img
    global screen
    global isPlayerturn

    pg.display.set_caption("오목")
    clock = pg.time.Clock()
    #player = 0
    if player == 1: #플레이어가 백, AI 먼저 시작
        long = list()
        plong = list()
        gameState = State(board, moves, long, plong, 2)
        print(gameState)
        Opago = AI(gameState, 10)
        #Opago = AI(gameState)
        print(Opago.state)
        screen.blit(board_img, (40, 40))
        isPlayerturn = False
        while not isFinished:
            clock.tick(30)
            if isPlayerturn:
                for event in pg.event.get():
                    pos = pg.mouse.get_pos()
                    if event.type is QUIT:
                        pg.quit()
                        sys.exit()

                    if event.type is pg.MOUSEBUTTONDOWN:
                            X, Y = clickposCheck(pos)
                            if X != -10 and Y !=-10:
                                if not newthreebythreeCheck(X,Y,1):
                                    drawStone(X, Y, 1)
                                    finishCheck(X,Y,1)
                                    gameState.make_action(X,Y)
                                    finishCheck(X,Y,1)
                                    print("X" + str(X))
                                    print("Y" + str(Y))
                                    print("Long" + str(Opago.state.longest))
                                    print("LongP" + str(Opago.state.playerlongest))
                                    isPlayerturn = False
                                else:
                                    print("3x3은 금지입니다")
                            else:
                                print("둘수 없는 곳")
            else:
                a, b = Opago.findMove()
                finishCheck(a,b,1)
                drawStone(a, b, 0)
                gameState.make_action(a,b)
                print("X"+str(a))
                print("Y"+str(b))
                print("Long"+str(Opago.state.longest))
                print("LongP"+str(Opago.state.playerlongest))

                finishCheck(a,b,1)

                isPlayerturn = True

            pg.display.flip()


    else: #플레이어가 흑, 플레이어 먼저 시작
        long = list()
        plong = list()
        gameState = State(board, moves, long, plong, 1)
        print(gameState)
        Opago = AI(gameState, 10)
        #Opago = AI(gameState)
        print(Opago.state)
        screen.blit(board_img, (40, 40))
        while not isFinished:
            clock.tick(30)
            if isPlayerturn:
                for event in pg.event.get():
                    pos = pg.mouse.get_pos()
                    if event.type is QUIT:
                        pg.quit()
                        sys.exit()

                    if event.type is pg.MOUSEBUTTONDOWN:
                            X, Y = clickposCheck(pos)
                            if X != -10 and Y !=-10:
                                if not newthreebythreeCheck(X,Y,0):
                                    drawStone(X, Y, 0)
                                    finishCheck(X,Y,0)
                                    gameState.make_action(X,Y)
                                    finishCheck(X,Y,0)
                                    print("X" + str(X))
                                    print("Y" + str(Y))
                                    print("Long" + str(Opago.state.longest))
                                    print("LongP" + str(Opago.state.playerlongest))
                                    isPlayerturn = False
                                else:
                                    print("3x3은 금지입니다")
                            else:
                                print("둘수 없는 곳")
            else:
                a, b = Opago.findMove()
                finishCheck(a,b,1)
                drawStone(a, b, 1)
                gameState.make_action(a,b)
                print("X"+str(a))
                print("Y"+str(b))
                print("Long"+str(Opago.state.longest))
                print("LongP"+str(Opago.state.playerlongest))

                isPlayerturn = True



            pg.display.flip()


def drawStone(x,y,blackOrwhite):
    global screen
    if blackOrwhite is 0:
        screen.blit(blackstone_img, ((x+1)*40-16,(y+1)*40-16))
        board[y,x] = 1
    else:
        screen.blit(whitestone_img, ((x+1)*40-16,(y+1)*40-16))
        board[y,x] = 2

def clickposCheck(pos):
    X = int(pos[0]/40)
    Y = int(pos[1]/40)
    if X < 1 or Y < 1 or X > 20 or Y >20:
        return -10,-10
    print(X)
    if (pos[0]-X*40) < -18:
        X = X-1
    elif (pos[0]-X*40) > 18:
        X = X+1

    if (pos[1]-Y*40) < -18:
        Y = Y-1
    elif (pos[1]-Y*40) > 18:
        Y = Y+1
    X = X-1
    Y = Y-1
    if X < 1 or Y < 1 or X > 20 or Y > 20:
        return -10,-10
    if board[Y,X] == 0:
        return X,Y
    else:
        print("II")
        return -10,-10

def finishCheck(new_x,new_y, blackOrwhite):
    global isFinished
    global  board
    movement = [[-1,-1], [-1,0], [-1,1], [0,-1], [0,1], [1,-1], [1,0], [1,1]]
    count = 1
    backCount = 0
    dx = new_x
    dy = new_y
    for i in range(4):
        if count >= 5:
            print("FINISHED")
            isFinished = True
            break
        count = 1
        backCount = 0
        dx = new_x
        dy = new_y
        while True:
            if backCount == 0:
                dx += movement[i][0]
                dy += movement[i][1]
            else:
                dx += movement[7-i][0]
                dy += movement[7-i][1]
            try:
                if board[dy, dx] == blackOrwhite+1:
                    count += 1
                else:
                    if backCount == 0:
                        dx = new_x
                        dy = new_y
                        backCount += 1
                    else:
                        break
            except IndexError:
                print("OutOfRange")
                break

def newthreebythreeCheck(new_x, new_y, blackOrwhite): #3x3 Check
    global board
    movement = [[-1,-1], [0,-1], [1,-1], [-1, 0], [1,0], [-1,1], [0,1], [1,1]]
    count = 1
    needmore_check = False
    yes_three = False
    direction = 10
    dx = new_x
    dy = new_y
    for i in range(8):
        count = 1
        dx = new_x
        dy = new_y
        #print(i)
        for j in range(3):
            dx += movement[i][0]
            #print(dx)
            dy += movement[i][1]
            #print(dy)
            #print("board: " + str(board[dy,dx])+" "+ str(board[dx,dy]))
            #print(board)
            try:
                if board[dy, dx] == blackOrwhite + 1:
                    count += 1
                else:
                    break
            except IndexError:
                print("OutOfRange")
                break
        #print(count)
        if count == 3:
            if board[new_y+movement[7-i][1], new_x+movement[7-i][0]] == 0:
                #print("i"+str(i))
                if yes_three:
                    return True
                else:
                    direction = i
                   # print("dir"+str(direction))
                    yes_three = True

    dx = new_x
    dy = new_y
    for i in range(4):
        if i == direction or i == 7-direction:
            print(direction)
            break
        count = 1
        dx = new_x + movement[i][0]
        dy = new_y + movement[i][1]
        if board[dy, dx] == blackOrwhite + 1 and board[dy+movement[i][1],dx+movement[i][0]] == 0:
            dx = new_x + movement[7-i][0]
            dy = new_y + movement[7-i][1]
            if board[dy, dx] == blackOrwhite + 1 and board[dy + movement[i][1], dx + movement[i][0]] == 0:
                if yes_three:
                    return True
                else:
                    yes_three = True

    return False

gameSet()
pg.quit()
sys.exit()


