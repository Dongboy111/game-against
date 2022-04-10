#宏动作定义
import copy
import os

import tensorflow as tf

gpus = tf.config.list_physical_devices("GPU")
print(gpus)
if gpus:
    gpu0 = gpus[0]  # 如果有多个GPU，仅使用第0个GPU
    tf.config.experimental.set_memory_growth(gpu0, True)  # 设置GPU显存用量按需使用

    tf.config.set_visible_devices([gpu0], "GPU")

UP = [0,-1]
DOWN = [0,1]
LEFT = [-1,0]
RIGHT= [1,0]
allAction = [UP,DOWN,LEFT,RIGHT]
myAction = []
for i in allAction:
    for j in allAction:
        myAction.append([i,j])
from utils.utils import getPs

Team1Color = (255, 80, 80)
Team2Color = (51, 51, 204)
#智能体数量
Number = (2,2)


#记录画完方格所有的点


width = 85
height = 45
BasicCell = {
    "team":-2,#初始默认没有人
    "member":-2,
    "whoIn":[],
}
gezi = []




for i in range(height):
    gezi.append([])
    for j in range(width):
        gezi[i].append({
    "team":-2,#初始默认没有人
    "member":-2,
    "whoIn":[],
})

# print(id(gezi[0]))
# print(id(gezi[1]))
# gezi = [[BasicCell for _ in range(width)] for _ in range(height)]



#  刷白墙

import easygui as eg
import tensorflow as tf
import sys
import random
from pygame.locals import *
import pygame
from utils.utils import DrowBackground,getActionByPre
from agent.agent1 import Agent1
from agent.agent2 import Agent2
from agentProcess.allProcess import allProcess

import numpy as np



#初始化
pygame.init()
size = 1000,600
geziNumber = 500,300

pygame.display.set_caption("bs")
Background = pygame.display.set_mode((576,448))

#记录画完的方格所有的点
allPoints = DrowBackground(Background)




agentStartPoints = [[],[]]
#初始化智能体的初始位点
# for i in range(Number[0]):
#     # print(i)
#     # print(allPoints[50][i + 10])
#     agentStartPoints[0].append(allPoints[random.randint(15,23)][random.randint(15,23)])
#
# #智能体2团体所有智能体形成初始点位
# for i in range(Number[1]):
#
#     agentStartPoints[1].append(allPoints[random.randint(20,30)][random.randint(15,23)])

#创建每个团队初始化地盘
agentStartMap = [[],[]]

#初始化两队智能体处理中心
allProcess = allProcess(Number,allPoints,Background)



agent1 = Agent1()
agent2 = Agent2()




#
# #创建中央调度类 实现功能为 碰撞检测  返回信息  传入指令驱动
#
# from utils.utils import MyProcess
#
# MyProcess = MyProcess(screen)



# 所有智能体属性初始化
agent1Num = 2  #智能体1数量
agent2Num = 2  #智能体2数量






start_time = pygame.time.get_ticks()
folder = os.getcwd()
imageList = os.listdir(folder)
model1 = None
model2 = None
for item in imageList:
    if os.path.isfile(os.path.join(folder, item)):
        if item == 'Dqn1.h5':
            model2 = tf.keras.models.load_model('Dqn1.h5')
        if item == 'Dqn2.h5':
            model1 = tf.keras.models.load_model('Dqn2.h5')

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    state = allProcess.getNowS()
    print(state.shape)
    state = np.expand_dims(state, axis=0)
    predict1  = model1.predict(state)
    predict2 = model2.predict(state)

    action1 = getActionByPre(predict1)
    action2 = getActionByPre(predict2)
    # for i in range(1000):
    newDone = False
    for i in range(1000):


        stateP, action, reward, nextSte, done = allProcess.move([action1, action2], start_time,newDone)
        newDone=False
        print(nextSte.shape)
        stateP = np.expand_dims(stateP, axis=0)
        predict1 = model1.predict(stateP)
        predict2 = model2.predict(stateP)
        print(predict1)
        print(predict2)

        if random.randint(0,10)<3:
            action1 = [random.choice(allAction),random.choice(allAction)]
            action2 = [random.choice(allAction),random.choice(allAction)]
        else:
            action1 = getActionByPre(predict1)

            action2 = getActionByPre(predict2)

        if done:
            print("=====================done=========================")

            from utils.utils import resetEnv

            resetEnv(Background)
            state = allProcess.getNowS()
            # state = np.expand_dims(state,axis=0)
            start_time = pygame.time.get_ticks()
            newDone = True





    # action1 = agent1.getAction(state)
    # action2 = agent2.getAction(state)
    #
    #
    # stateP,action,re,stateN,done = allProcess.move([action1,action2],start_time)






    pygame.display.update()


