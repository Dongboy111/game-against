#85*45 定义基础格子信息
import pygame
Agent1PngPath = "./resource/images/team1.png"
agent1 = pygame.image.load(Agent1PngPath)
agent1Num = 2
agent2Num = 2
from utils.utils import getPs
import numpy as np
# 需要每队智能体 路线点位  agentnum  [[],[],[]*agentnum] [[],[],[]*agentnum]
# 需要每个队公共区域点位   two          [] []
# 每个智能体所在位置的组合               [] []

agent1PathPoints = [[] for _ in range(agent1Num)]
# agent1LastPathPoints = [[] for _ in range(agent1Num)]
agent2PathPoints = [[] for _ in range(agent2Num)]
# agent2LastPathPoints = [[] for _ in range(agent2Num)]

lastAgent1Dis = [] #智能体1之前的距离值
lastAgent2Dis = [] # 智能体2上一次的距离值
lastAgent1Len = []#智能体1上一次的长度值
lastAgent2Len = [] #智能体2上一次的长度值

agent1PublicPoints = []
agent2PublicPoints = []

agent1AllAgentNowPoints = []
agent2AllAgentNowPoints = []

agentReward = [0,0]

import threading
from utils.utils import GuiY
gameTime = 180#初始两分钟

#计算游戏时长的
def getTime(start_time):
    end_time = pygame.time.get_ticks()
    time = (end_time - start_time) // 1000
    #print(time)
    if time>gameTime:
        return True
    else:
        return False

# class  myThread(threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         pass

"""
先初始化 公共点位  智能体点位   

传输动作  根据动作给变上面五个变量  
之后根据五个变量 重新生成gezi变量   

之后画出全部   

重点是 传输动作时候我们需要进行检测  回环检测  碰撞检测  合作检测    


"""
import random
Agent2PngPath = "./resource/images/team2.png"
agent2 = pygame.image.load(Agent2PngPath)
BackgroundColor =  (150, 255, 255)
TeamColor = [(255, 0, 153),(223, 191, 159)]

agentR = [agent1,agent2]
from utils.utils import DrowBackground,DrawLine,find
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


# [[[]*85]*45]
# 1，哪个队的 ,
# 2，队里的哪一个人(如果已经变成公共的了那就设置成-1),
# 3，哪个人在这个格子里 如果没有人在就是-1(可以是多个)
def clear():
    agent1PathPoints = [[], []]
    agent2PathPoints = [[], []]

    agent1PublicPoints = []
    agent2PublicPoints = []

    agent1AllAgentNowPoints = []
    agent2AllAgentNowPoints = []


class allProcess:
    def __init__(self,agentNum,allPoints,screen):
        self.agentNum = agentNum
        #初始化历史点列表字典
        self.agentHistoryPosition = [{"team1":[] for _ in range(self.agentNum[0])},{"team1":[] for _ in range(self.agentNum[1])}]
        #记录所有的点位
        self.agentNowPosition = [[],[]]#rect类型
        #原始画表形成的表格
        self.allPoints = allPoints
        # print("111")
        # print(len(self.allPoints[0]))
        # print(len(self.allPoints))
        # print("1111")


        #公共点位初始化
        #智能体1公共点位初始化
        for i in range(25,29):
            for j in range(30,34):
                agent1PublicPoints.append((j,i))
        #智能体2点位初始化
        for i in range(25,29):
            for j in range(40,44):
                agent2PublicPoints.append((j,i))
        #初始化智能体1的初始点位
        for i in range(agentNum[0]):
            agent1AllAgentNowPoints.append(random.choice(agent1PublicPoints))

        #初始化智能体2的初始点位
        for i in range(agentNum[1]):
            agent2AllAgentNowPoints.append(random.choice(agent2PublicPoints))


        #获取画的屏幕句柄
        self.screen = screen

        # self.agentStartPosints = agentStartPosints

        # print(self.agentStartPosints)
        #在这个时候我们要对控制表进行更新
        # i = 0
        # for item in self.agentStartPosints[0]:
        #
        #     a,b = find(self.allPoints,item)
        #     agent1PathPoints[i].append((a,b))
        #
        #     gezi[a][b]["team"] = 0
        #     gezi[a][b]["member"] = self.agentStartPosints[0].index(item)
        #     gezi[a][b]["whoIn"].append(0)
        #     i = i +1
        #     agent1AllAgentNowPoints.append((a,b))
        #     # print(gezi)
        # i = 0
        # for item in self.agentStartPosints[1]:
        #
        #     a,b = find(self.allPoints,item)
        #     agent2PathPoints[i].append((a, b))
        #     gezi[a][b]["team"] = 1
        #     gezi[a][b]["member"] = self.agentStartPosints[1].index(item)
        #     gezi[a][b]["whoIn"].append(1)
        #
        #     i = i+1
        #     agent1AllAgentNowPoints.append((a, b))

        self.drawAlllByFive()



        pass
    def move(self,action,start_time,newDone):#两组agent共用的
        #在这个函数里我们需要根据得到的action来调整五个变量的值
        # print(newDone,"这是nowdone")

        if newDone:
            clear()


        # agent1LastPathPoints[0] = agent1PathPoints[0][:]
        # agent1LastPathPoints[1] = agent1PathPoints[1][:]
        # agent2LastPathPoints[0] = agent2PathPoints[0][:]
        # agent2LastPathPoints[1] = agent2PathPoints[1][:]
        # print(agent1PathPoints,"这是智能体1的所有点"
        #                        "")
        agentReward = [0,0]
        stateP = getPs(self.screen)
        lastPoint = agent1AllAgentNowPoints
        for i in range(len(action[0])):

            sum= (lastPoint[i][0]+ action[0][i][0],lastPoint[i][1]+ action[0][i][1])  # 使用zip方法进行连接
            if (sum[0] > 84):
                sum = (84, sum[1])
            if (sum[0] < 0):
                sum = (0, sum[1])
            if (sum[1] > 44):
                sum = (sum[0], 44)
            if (sum[1] < 0):
                sum = (sum[0], 0)
            #检测时候路经自己走过的点  全是agent1的
            if sum in agent1PathPoints[i]:
                # print("在这里")
                mypoint = agent1PathPoints[i][:agent1PathPoints[i].index(sum)+1]
                agent1AllAgentNowPoints[i] = sum
                agent1PathPoints[i] = mypoint
            else :
                agent1AllAgentNowPoints[i] = sum
                agent1PathPoints[i].append(lastPoint[i])
            #杀敌检测
            for  item in range(len(agent2PathPoints)):
                if sum in agent2PathPoints[item] :
                    agent2PathPoints[item] = []
                    agent2AllAgentNowPoints[item] = random.choice(agent2PublicPoints)
                    agentReward[0] = agentReward[0] + 1
                    agentReward[1] = agentReward[1] - 1
            #是否到达公共区域检测  如果到达 则进行闭操作
            if sum in agent1PublicPoints:
                # print(agent1PathPoints[i])
                diyige = [i[0] for i in agent1PathPoints[i]]#获取路径中每一列最大数
                dierge = [i[1] for i in agent1PathPoints[i]]
                pub1TempPoint = []
                for item in range(min(diyige),max(diyige)+1):
                    for k in range(min(dierge),max(dierge)+1):
                        pub1TempPoint.append((item,k))
                agent1PublicPoints.extend(pub1TempPoint)
                agent1PathPoints[i] = []
                agentReward[0] = agentReward[0] + 1
                # agentReward[1] = agentReward[1] - 1
            # print(agent1PublicPoints) 公共点位打印
        extenR1 = getRewardByDis(0)
        extenR2 = getRewardByDis(1)





        lastPoint = agent2AllAgentNowPoints
        for i in range(len(action[1])):

            sum= (lastPoint[i][0]+ action[1][i][0],lastPoint[i][1]+ action[1][i][1])  # 使用zip方法进行连接
            if(sum[0]>84):
                sum = (84,sum[1])
            if(sum[0]<0):
                sum = (0, sum[1])
            if (sum[1] > 44):
                sum = (sum[0], 44)
            if (sum[1] < 0):
                sum = (sum[0], 0)
            if sum in agent2PathPoints[i]:
                # print("在这里")
                mypoint = agent2PathPoints[i][:agent2PathPoints[i].index(sum) + 1]
                agent2AllAgentNowPoints[i] = sum
                agent2PathPoints[i] = mypoint
            else:
                agent2AllAgentNowPoints[i] = sum
                agent2PathPoints[i].append(lastPoint[i])
            # 杀敌检测
            for item in range(len(agent2PathPoints)):
                if sum in agent1PathPoints[item]:
                    agent1PathPoints[item] = []
                    agent1AllAgentNowPoints[item] = random.choice(agent1PublicPoints)
                    agentReward[0] = agentReward[0] - 1
                    agentReward[1] = agentReward[1] + 1
            # 是否到达公共区域检测  如果到达 则进行闭操作
            if sum in agent2PublicPoints:
                # print(agent2PathPoints[i])
                diyige = [i[0] for i in agent2PathPoints[i]]  # 获取路径中每一列最大数
                dierge = [i[1] for i in agent2PathPoints[i]]
                pub1TempPoint = []
                if diyige==[] or dierge==[]:
                    pass
                else :
                    for item in range(min(diyige), max(diyige)+1):
                        for k in range(min(dierge), max(dierge)+1):
                            pub1TempPoint.append((item, k))
                    agent2PublicPoints.extend(pub1TempPoint)
                    agent2PathPoints[i] = []
                    # agentReward[0] = agentReward[0] - 1
                    agentReward[1] = agentReward[1] + 4
            # print(agent2PublicPoints)

        self.drawAlllByFive()
        import time
        time.sleep(0.1)
        stateN = getPs(self.screen)
        done = getTime(start_time)

        import easygui
        # agentReward[0] = GuiY(agentReward[0] + extenR1)#把杀敌检测 形成公共区域的检测 每一步的检测放在一起
        # agentReward[1] = GuiY(agentReward[1] + extenR1)
        agentReward[0] = agentReward[0] + extenR1#把杀敌检测 形成公共区域的检测 每一步的检测放在一起
        agentReward[1] = agentReward[1] + extenR1
        if agentReward[0]>20:
            agentReward[0]=20
        if agentReward[0]<-20:
            agentReward[0]=-20
        if agentReward[1] > 20:
            agentReward[1] = 20
        if agentReward[1] < -20:
            agentReward[1] = -20
        if done:

            if len(agent1PublicPoints)>len(agent2PublicPoints):
                agentReward[0] = 20
                agentReward[1] = -20
                easygui.msgbox("队1赢了", "胜负")
            elif len(agent1PublicPoints) < len(agent2PublicPoints):
                agentReward[1] = 20
                agentReward[0] = -20
                easygui.msgbox("队2赢了", "胜负")
            else:

                easygui.msgbox("平局","平局")


        # for i in range(len(agentReward)):
        #     if agentReward[i]>20:
        #         agentReward[i] = 20
        #     if agentReward[i]<-20:
        #         agentReward=-20


        return stateP,action,agentReward,stateN,done





    def getNowS(self):
        stateN = getPs(self.screen)
        return stateN
    def drawAll(self):#根据gezi画整个屏幕

        DrowBackground(self.screen)
        import time
        # time.sleep(1)
        # print(gezi)
        for row in range(len(gezi)):
            for col in range(len(gezi[row])):
                # print("row","col",row,col)
                if gezi[row][col]["team"]!=-2:
                    pygame.draw.rect(self.screen, TeamColor[gezi[row][col]["team"]], self.getRectByList((col,row)), 0, border_radius=1)

                    if len(gezi[row][col]["whoIn"])!=0:
                        for i in gezi[row][col]["whoIn"]:
                            self.screen.blit(agentR[i],self.getRectByList((col,row)))
                else:
                    pygame.draw.rect(self.screen, BackgroundColor, self.getRectByList((col,row)), 0, border_radius=1)


        DrawLine(self.screen)
    def drawAlllByFive(self):
        DrowBackground(self.screen)
        #画公共区域
        for i in agent1PublicPoints:

            pygame.draw.rect(self.screen, TeamColor[0], self.allPoints[i[0]][i[1]], 0, border_radius=1)
        for i in agent2PublicPoints:
            pygame.draw.rect(self.screen, TeamColor[1], self.allPoints[i[0]][i[1]], 0, border_radius=1)
        #画每个智能体的路线
        for j in agent1PathPoints:
            for i in j :
                pygame.draw.rect(self.screen, TeamColor[0], self.allPoints[i[0]][i[1]], 0, border_radius=1)

        for j in agent2PathPoints:
            for i in j:
                pygame.draw.rect(self.screen, TeamColor[1], self.allPoints[i[0]][i[1]], 0, border_radius=1)
        #画每个智能体所在位置
        for  i in agent1AllAgentNowPoints:
            self.screen.blit(agentR[0], self.allPoints[i[0]][i[1]])
        for  i in agent2AllAgentNowPoints:
            self.screen.blit(agentR[1], self.allPoints[i[0]][i[1]])
        pygame.display.flip()
    def getRectByList(self,indexList):#85 45
        return self.allPoints[indexList[0]][indexList[1]]


def getObsInif():
   return   (agent1PathPoints,agent2PathPoints,agent1PublicPoints,agent2PublicPoints,agent1AllAgentNowPoints,agent2AllAgentNowPoints)


# 计算智能体队伍 走的距离获得奖励的情况
def getRewardByDis(team):

    midDisLen = 10#是奖励值递减的分界线 具体见 计算公式里面的
    if team==0:
        len1 = []
        dis1 = []
        # 计算 每个智能体现在走过的点 但是没有添加到pub里面的长度 以及此刻位置距离
        for item in agent1PathPoints:
            if len(item) == 0:  # 防止智能体的长度为0
                len1.append(0)
                dis1.append(0)
            else:
                len1.append(len(item))
                dis1.append(getItemToPubDis(item[0], agent1PublicPoints))
            # 计算每一个智能体到 pub的距离
        # 现在 当前的 智能体的长度 和距离都计算出来了 我么开始计算 奖励了
        rewardAll = []
        for i in range(len(len1)):
            if len1[i] + dis1[i] <= midDisLen:
                rewardAll.append(len1[i] + dis1[i])
            else:
                rewardAll.append(-len1[i] - dis1[i])

        #print("这是计算出来的最后所有的奖励值", rewardAll)
        sum = 0
        for i in rewardAll:
            sum = sum + i

            # 进行归一化到 -10-10
        # from utils.utils import GuiY
        # reward = GuiY(sum, -10, 10)
        return sum
    if team==1:
        len1 = []
        dis1 = []
        # 计算 每个智能体现在走过的点 但是没有添加到pub里面的长度 以及此刻位置距离
        for item in agent2PathPoints:
            if len(item) == 0:  # 防止智能体的长度为0
                len1.append(0)
                dis1.append(0)
            else:
                len1.append(len(item))
                dis1.append(getItemToPubDis(item[0], agent2PublicPoints))
            # 计算每一个智能体到 pub的距离
        # 现在 当前的 智能体的长度 和距离都计算出来了 那么开始计算 奖励了
        rewardAll = []
        for i in range(len(len1)):
            if len1[i] + dis1[i] <= midDisLen:
                rewardAll.append(len1[i] + dis1[i])
            else:
                rewardAll.append(-len1[i] - dis1[i]+midDisLen-4)

        #print("这是计算出来的最后所有的奖励值", rewardAll)
        sum = 0
        for i in rewardAll:
            sum = sum + i

            # 进行归一化到 -10-10
        # from utils.utils import GuiY
        # reward = GuiY(sum, -10, 10)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print(sum)
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        return sum

        #计算 每个智能体到public 的距离  使用欧式距离


    # if team==0:
    #     #先计算当前点距离public的距离
    #     for i in  range(len(agent1PathPoints)):
    #         pass






#计算一个智能体到自家公共范围的距离
def getItemToPubDis(item,publicPoints):
    minV = 1000
    for i in publicPoints:
        dis=np.sqrt(np.square(i[0]-item[0])+np.square(i[1]-item[1]))
        if dis <minV:
            minV = dis
    #print("这是计算出来的minV",minV)
    return minV
