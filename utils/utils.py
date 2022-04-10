import json
# 读取json文件
from random import random

import pygame
import operator
# from agentProcess.allProcess import allProcess
UP = [0,-1]
DOWN = [0,1]
LEFT = [-1,0]
RIGHT= [1,0]
allAction = [UP,DOWN,LEFT,RIGHT]
myAction = []
for i in allAction:
    for j in allAction:
        myAction.append([i,j])


# def move(action):
#     allProcess.move(action)
from PIL import Image


def DrowBackground(Background):
    allPoints = []
    for x in range(0, 576, 16):
        tempPoints = []
        for y in range(0, 448, 16):
            tempPoints.append(pygame.draw.rect(Background, (150, 255, 255), (x, y, 16, 16), 0, border_radius=1))
        allPoints.append(tempPoints)
    for i in range(0, 576, 16):
        pygame.draw.line(Background, (0, 0, 0), (0, i), (576, i))
        pygame.draw.line(Background, (0, 0, 0), (i, 0), (i, 576))
    pygame.display.update()
    print(np.array(allPoints).shape)
    print("#################################################dian wei")
    return allPoints
#我需要一个方格表  确定哪个方格被哪个人锁定    并且是否方格里有其他人
#每次运动完后需要有一个函数判断时候同一个队伍的有环锁  以及是否有人死亡    
agent1Num = 2  #智能体1数量
agent2Num = 2  #智能体2数量

agent1AllPoints = [{} for _ in range(agent1Num)]
agent2AllPoints = [{} for _ in range(agent2Num)]

allInf = [agent1AllPoints,agent2AllPoints]

# print(allInf)
team1Color = (255, 153, 153)
team2Color = (223, 191, 159)

# class MyProcess:
#     def __init__(self,screen):
#         self.screen = screen
#
#     def initDraw(self,agent1,agent2,agent1Num,agent2Num):
#         pass
#
#     def readJson(self,filename):
#
#         f = open(filename, 'r')
#         content = f.read()
#         a = json.loads(content)
#         f.close()
#         return a
#
#     #画矩形框
#     def DrawRect(self,size,mycolcor):
#
#         position = size
#         width = 0
#         pygame.draw.rect(self.screen, mycolcor, position, width)
#
#     def DrawIrrRect(self,pointSet,color):
#         pygame.draw.polygon(self.screen,points=pointSet,color=color)

def find(a, b):  # 根据横纵坐标 高等找到对应数格 a是待寻找的列表

    for i in range(len(a)):
        for j in range(len(a[i])):
            if operator.eq(a[i][j], b):
                return (j, i)
def findFan(a,b):#反向寻找
    return a[b(0),b[1]]

def getBeforeColor(b):#获取之前方格的颜色
    print()
    allColor = ()
    item = b
    if item[1] % 2 != 0:
        allColor= (150, 255, 255)
    elif item[1] % 2 == 0 and item[0] % 2 != 0:
        allColor=  (204, 255, 204)
    elif item[1] % 2 == 0 and item[0] % 2 == 0:
        allColor= (150, 255, 255)
    return allColor

# def getBeforeColor(b):#获取之前方格的颜色
#     print()
#     allColor = []
#     item = b
#     if item[1] % 2 != 0:
#         allColor.append((204, 255, 204))
#     elif item[1] % 2 == 0 and item[0] % 2 != 0:
#         allColor.append((150, 255, 255))
#     elif item[1] % 2 == 0 and item[0] % 2 == 0:
#         allColor.append((204, 255, 204))
#     return allColor



#游戏人物移动类

class AgentAction():

    def __init__(self,team,nowPosition,allPoints,ziyuan):
        self.ziyuan = ziyuan
        self.allPositions = allPoints  #代表着所有的方格点  全局
        self.team = team
        #team = 0,0 代表第一队第一个
        #team = 1，0 代表第二队第一个
        self.allPosition = []
        self.allPosition.append(nowPosition)
    def move(self,Background,ziyuan,action,speedUp=0): #speedUp 0 不加速 1 加速 action格式为[x,y] 输入动作之后就进行self.alllpointion 最后一个点进行遍历

        agentPosition = self.allPosition[-1].move(action)
        if self.allPosition[-1].top == 0:
            return False
        if self.allPosition[-1].bottom == 576:
            return False
        if self.allPosition[-1].left == 0:
            return False
        if self.allPosition[-1].right == 448:
            return False

        pygame.display.flip()
        try:
            flag = agentPosition == self.allPosition[-2]
        except Exception as e:
            flag = False

        if  flag:
            # b=self.sDe(agentPosition)
            # print(b,"这是返回的颜色  ")


            # pygame.draw.rect(Background, b[0], self.allPosition[-2], 0, border_radius=1)
            pygame.draw.rect(Background, (255,255,255), self.allPosition[-1], 0, border_radius=1)
            pygame.draw.rect(Background, (150, 255, 255), self.allPosition[-1], 0, border_radius=1)
            if self.team[0]==0:

                pygame.draw.rect(Background, (255, 255, 255), agentPosition, 0, border_radius=1)
                pygame.draw.rect(Background, team1Color, agentPosition, 0, border_radius=1)
                Background.blit(self.ziyuan, agentPosition)
            else:

                pygame.draw.rect(Background, (255, 255, 255), agentPosition, 0, border_radius=1)
                pygame.draw.rect(Background, team2Color, agentPosition, 0, border_radius=2)
                Background.blit(self.ziyuan, agentPosition)
            self.allPosition.remove(self.allPosition[-1])



                # pygame.draw.rect(Background, b[0], self.allPosition[-2], 0, border_radius=1)
        else:

            pygame.display.flip()
            self.allPosition.append(agentPosition)
            if self.team[0] == 0:
                pygame.draw.rect(Background, team1Color,self.allPosition[-2], 0,border_radius=1)
                pygame.draw.rect(Background, team1Color,self.allPosition[-1], 0,border_radius=1)
            else:
                pygame.draw.rect(Background, team2Color,self.allPosition[-1], 0,border_radius=1)

                pygame.draw.rect(Background, team2Color,self.allPosition[-2], 0,border_radius=1)

            Background.blit(ziyuan, agentPosition)
        allInf[self.team[0]][self.team[1]].update({"nowPosition":self.allPosition[-1]})

    def getInf(self):
        return  allInf


import numpy as np
import tensorflow as tf
import random
#预测结果 转化成 动作值
def getActionByPre(pre):
    # tempF = False
    # for i in pre[0]:
    #     if i < 0:
    #         tempF = True
    #         break
    # if tempF:
    #     for i in range(len(pre[0])):
    #         pre[0][i] = pre + random.uniform(0, 0.5)

    action = list(pre[0]).index(max(list(pre[0])))

    return myAction[action]

#归一化
def GuiY(x,Max=20,Min=-20):
    x = (x - Min) / (Max - Min)
    return x

#获取屏幕截图
def getPs(suf):
    data = pygame.image.tostring(suf, 'RGB')
    img = Image.frombytes('RGB',(576, 448), data)
    img = np.array(img)
    # img = np.expand_dims(img,axis=-1)
    # img = np.array([img,img,img,img])
    # img = tf.reshape(img,(1,576,448,3))
    # print(img.shape,"============================================")
    return img



#重置环境
def resetEnv(Background):
    i = 0
    j = 0
    for x in range(0, 576, 16):
        j = j + 1
        i = 0
        tempPoints = []
        for y in range(0, 448, 16):
            i = j + 1 + i
            if i % 2 == 0:
                color = (204, 255, 204)
            else:
                color = (150, 255, 255)
            pygame.draw.rect(Background, color, (x, y, 16, 16), 0, border_radius=1)

    for i in range(0, 576, 16):
        pygame.draw.line(Background, (0, 0, 0), (0, i), (576, i))
        pygame.draw.line(Background, (0, 0, 0), (i, 0), (i, 576))


def DrawLine(Background):
    for i in range(0, 576, 16):
        pygame.draw.line(Background, (0,0,0), (0, i), (576, i))
        pygame.draw.line(Background, (0, 0, 0), (i, 0), (i, 576))