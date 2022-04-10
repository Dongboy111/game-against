#宏动作定义
import copy
import os
import time

import tensorflow as tf

gpus = tf.config.list_physical_devices("GPU")
#print(gpus)
if gpus:
    gpu0 = gpus[0]  # 如果有多个GPU，仅使用第0个GPU
    tf.config.experimental.set_memory_growth(gpu0, True)  # 设置GPU显存用量按需使用

    tf.config.set_visible_devices([gpu0], "GPU")

UP = [0,-1]
DOWN = [0,1]
LEFT = [-1,0]
RIGHT= [1,0]
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

# #print(id(gezi[0]))
# #print(id(gezi[1]))
# gezi = [[BasicCell for _ in range(width)] for _ in range(height)]



#  刷白墙

import easygui as eg
import tensorflow as tf
import sys
import random
from pygame.locals import *
import pygame
from utils.utils import DrowBackground
from agent.agent1 import Agent1
from agent.agent2 import Agent2
from agentProcess.allProcess import allProcess





#初始化
pygame.init()
size = 1000,600
geziNumber = 500,300

pygame.display.set_caption("bs")
Background = pygame.display.set_mode((1360 ,720))

#记录画完的方格所有的点
allPoints = DrowBackground(Background)




agentStartPoints = [[],[]]
#初始化智能体的初始位点
for i in range(Number[0]):
    # #print(i)
    # #print(allPoints[50][i + 10])
    agentStartPoints[0].append(allPoints[random.randint(20,25)][random.randint(20,25)])

#智能体2团体所有智能体形成初始点位
for i in range(Number[1]):

    agentStartPoints[1].append(allPoints[random.randint(50,55)][random.randint(20,25)])

#创建每个团队初始化地盘
agentStartMap = [[],[]]

#初始化两队智能体处理中心
allProcess = allProcess(Number,allPoints,Background)


#
# agent1 = Agent1()
# agent2 = Agent2()




#
# #创建中央调度类 实现功能为 碰撞检测  返回信息  传入指令驱动
#
# from utils.utils import MyProcess
#
# MyProcess = MyProcess(screen)



#allpoints是所有方格点位位置
# 所有智能体属性初始化
agent1Num = 2  #智能体1数量
agent2Num = 2  #智能体2数量

# agent1HisAllPoints = []#智能体1团体已经形成的所有点位
# agent2HisAllPonits = []#智能2团体已经形成的所有点位
# agent1AllPoints = [[] for _ in range(agent1Num)]
# agent2AllPoints = [[] for _ in range(agent2Num)]
# #print(agent1AllPoints)
#
# #智能体1团体所有智能体形成初始点位
# for i in range(agent1Num):
#     # #print(i)
#     # #print(allPoints[50][i + 10])
#     agent1AllPoints[i].append(allPoints[random.randint(20,25)][random.randint(20,25)])
#     # #print(agent1AllPoints)
#
# #智能体2团体所有智能体形成初始点位
# for i in range(agent2Num):
#
#     agent2AllPoints[i].append(allPoints[random.randint(50,55)][random.randint(20,25)])
#
# #print(agent1AllPoints)
# #print(agent2AllPoints)
#画出所有智能体  agent1
# for i in agent1AllPoints:
#     Background.blit(shu,i[0])
#
#
#
# for i in agent2AllPoints:
#     Background.blit(mao, i[0])


#构建完毕之后 进行动作数组搭建   1 是代表上方移动  2 是下方移动  3 是左方移动  4是右方移动
# agent1Action = [[] for _ in range(agent1Num)]
# agent2Action = [[] for _ in range(agent2Num)]



#测试动作用一个固定列表进行
# agent1Action[0].append(4)
# agent1Action[1].append(4)
#
# agent2Action[0].append(3)
# agent1Action[1].append(3)

# pygame.draw.rect(Background, (255, 255, 255), self.allPosition[-1], 0, border_radius=1)
# action1 = [UP,UP]
# action2 = [UP,UP]
from agent.Dqn import DQNAgent
from agent.Dqn2 import DQNAgent2
import numpy as np
#初始化 两队智能体
trainNum = 1
dqnAgent1 = DQNAgent()
dqnAgent2 = DQNAgent2()

start_time = pygame.time.get_ticks()

my = 0
for k in range(2):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    state = allProcess.getNowS()
    folder = os.getcwd()
    imageList = os.listdir(folder)
    for item in imageList:
        if os.path.isfile(os.path.join(folder, item)):
            if item == 'dqn.h5':
                tf.keras.models.load_model('dqn.h5')
    newDone = False
    for _ in range(100):
        newDone = True


        for i in range(1000):  # one cunchu should

            action1 = dqnAgent1.act(state)  # 格式应该为[]
            # #print(action1,"这是我的模型获取的")
            action2 = dqnAgent2.act(state)  # 格式应该为[]
            stateP, action, reward, nextSte, done = allProcess.move([action1, action2], start_time, newDone)
            # print("===================================================================")
            # print("这是reward1", reward[0])
            # print("this is action1 ", action[0])
            #
            # print("这是reward2", reward[1])
            # print("this is action1 ", action[1])
            # print("=====================================================================")
            newDone = False
            if max(reward)>23:
                my = my +1
                print(i,"this is numbers")
                dqnAgent1.save_exp(state, action[0], reward[0], nextSte, done)
                dqnAgent2.save_exp(state, action[1], reward[1], nextSte, done)
            state = copy.deepcopy(nextSte)
            # if done:
            #     print("\n\n")
            #     print("=====================done=========================")
            #
            #     trainNum = trainNum+1
            #     if trainNum==3:
            #         model1Name = "Dqn1.h5"
            #         dqnAgent1.model.save(model1Name)
            #         model2Name = "Dqn2.h5"
            #         dqnAgent2.model.save(model2Name)
            #         eg.msgbox("模型保存完毕", "模型保存完毕")
            #         print("开始第")
            #         print(k)
            #         print("遍，第")
            #         print(trainNum)
            #         print("次训练")
            #         eg.msgbox("this ",trainNum,"num ")
            #         eg.msgbox("moxingyijingbaocun","moxingyijingbaocun")
            #         break
            #
            #
            #
            #     from utils.utils import DrowBackground
            #     DrowBackground(Background)
            #     state = allProcess.getNowS()
            #     # state = np.expand_dims(state,axis=0)
            #     start_time = pygame.time.get_ticks()
            #     newDone = True
        dqnAgent1.train_exp(20)
        dqnAgent2.train_exp(20)
        time.sleep(1)
        print("stop training")
        eg.msgbox("shuliang",my)
        dqnAgent1.memory = []
        dqnAgent2.memory = []




    # action1 = agent1.getAction(state)
    # action2 = agent2.getAction(state)
    #
    #
    # stateP,action,re,stateN,done = allProcess.move([action1,action2],start_time)






    pygame.display.update()


