import pygame
Agent1PngPath = "./resource/images/team1.png"
from agentProcess.allProcess import getObsInif
# UP = [0,-16]
# DOWN = [0,16]
# LEFT = [-16,0]
# RIGHT= [16,0]
UP = [0,-1]
DOWN = [0,1]
LEFT = [-1,0]
RIGHT= [1,0]
all = [UP,DOWN,LEFT,RIGHT]

from model.DQN import DQNAgent

from model.DQN2 import DQN

from agentProcess.allProcess import agent1PublicPoints
class Agent1:
    def __init__(self,):#创建这一队伍的所有初始点以及 智能体所在位置
        # self.startPosition = startPosition  # 记录初始点位
        self.i = -1
        self.mylist = [[UP,DOWN],[UP,DOWN],[UP,DOWN],[UP,DOWN],[UP,DOWN],[UP,DOWN],[UP,DOWN],[UP,DOWN],[UP,DOWN],[LEFT,DOWN]
                       ,[LEFT,DOWN],[LEFT,DOWN],[DOWN,DOWN],[DOWN,DOWN],[DOWN,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN]]
        self.mylist1 = [[UP,DOWN],[UP,DOWN],[UP,DOWN],[UP,DOWN],[UP,DOWN],[UP,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],
                        [RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],[RIGHT,DOWN],]
        self.mylist2 = [[UP, DOWN], [UP, DOWN], [UP, DOWN], [UP, DOWN], [UP, DOWN], [UP, DOWN], [RIGHT, DOWN],
                        [RIGHT, DOWN],


                        [DOWN,DOWN],[DOWN,DOWN],[DOWN,DOWN],[DOWN,DOWN],[DOWN,DOWN],[DOWN,DOWN],[DOWN,DOWN],[DOWN,DOWN],[DOWN,DOWN]]
        self.mylist3 = [[[0, -1], [1, 0]], [[-1, 0], [0, -1]], [[-1, 0], [1, 0]], [[-1, 0], [-1, 0]], [[-1, 0], [0, 1]], [[-1, 0], [0, -1]], [[0, 1], [-1, 0]], [[0, 1], [0, 1]], [[0, 1], [1, 0]], [[0, 1], [1, 0]], [[0, 1], [0, 1]], [[1, 0], [1, 0]], [[-1, 0], [0, 1]], [[0, -1], [0, 1]], [[0, -1], [0, -1]], [[0, -1], [0, 1]], [[0, 1], [-1, 0]], [[0, -1], [0, -1]], [[0, 1], [1, 0]], [[-1, 0], [-1, 0]], [[1, 0], [1, 0]], [[-1, 0], [0, -1]], [[-1, 0], [-1, 0]], [[0, -1], [0, -1]], [[-1, 0], [0, -1]], [[1, 0], [-1, 0]], [[0, -1], [-1, 0]], [[0, -1], [0, 1]], [[0, -1], [0, 1]], [[0, 1], [0, 1]], [[1, 0], [-1, 0]], [[0, 1], [-1, 0]], [[-1, 0], [-1, 0]], [[0, -1], [0, -1]], [[1, 0], [0, -1]], [[0, 1], [1, 0]], [[0, 1], [0, -1]], [[0, 1], [-1, 0]], [[1, 0], [0, 1]], [[1, 0], [-1, 0]], [[0, -1], [1, 0]], [[0, -1], [-1, 0]], [[0, -1], [-1, 0]], [[-1, 0], [1, 0]], [[0, 1], [0, -1]], [[0, 1], [0, -1]], [[0, -1], [1, 0]], [[0, -1], [0, -1]], [[-1, 0], [-1, 0]], [[-1, 0], [-1, 0]]]
        self.agentDqn = DQNAgent()

        self.historyPositions = []  # 记录一队所有智能体走过的点位但是还没有成为团队公共区域的点位
    def getObsInif(self):
        #获取观察到的信息

        return getObsInif()
    def getAction(self,state):
       action = [UP,UP]


       return action


