import tensorflow as tf

import numpy as np
import copy
# import io
import random
import os
import tensorflow.keras as keras
from utils.utils import GuiY


UP = [0,-1]
DOWN = [0,1]
LEFT = [-1,0]
RIGHT= [1,0]
allAction = [UP,DOWN,LEFT,RIGHT]
maxAction = 2**(len(allAction))
myAction = [[[0, 1], [-1, 0]], [[-1, 0], [-1, 0]], [[-1, 0], [0, -1]], [[-1, 0], [1, 0]], [[1, 0], [0, 1]], [[0, -1], [1, 0]], [[1, 0], [-1, 0]], [[1, 0], [0, -1]], [[0, -1], [-1, 0]], [[1, 0], [1, 0]], [[0, 1], [0, -1]], [[0, 1], [1, 0]], [[0, 1], [0, 1]], [[0, -1], [0, 1]], [[0, -1], [0, -1]], [[-1, 0], [0, 1]]]


# for i in allAction:
#     for j in allAction:
#         myAction.append([i,j])
# print("]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
# print(myAction)
# print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[")
# print(maxAction)


class DQNAgent():
    def __init__(self):

        # 经验池
        self.memory = []
        self.gamma = 0.9  # decay rate 奖励衰减
        self.lossM = []

        # 控制训练的随机干涉
        self.epsilon = 1 # 随机干涉阈值 该值会随着训练减少 减少这个可以去掉 增加探索能力
        self.epsilon_decay = .85  # 每次随机衰减0.005
        self.epsilon_min = 0.1  # 随机值干涉的最小值

        self.learning_rate = 0.0001  # 学习率
        self._build_model()
        self.shuaijian = 0.8

    # 创建模型  输入4种状态，预测0/1两种行为分别带来到 奖励值
    def _build_model(self):
        model = tf.keras.Sequential()
        #输入是一张图 输出是16个组合动作
        model.add(tf.keras.layers.Conv2D(2, (3, 3), activation='relu', padding="SAME", input_shape=(720, 1360, 3)))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        model.add(tf.keras.layers.Conv2D(2, (3, 3), activation='relu'))
        model.add(tf.keras.layers.MaxPooling2D((2, 2)))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(300, activation='relu'))
        model.add(tf.keras.layers.Dropout(0.5))
        model.add(tf.keras.layers.Dense(100, activation='relu'))
        model.add(tf.keras.layers.Dropout(0.7))
        model.add(tf.keras.layers.Dense(16, activation='linear'))

        # model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
        model.summary()  # 显示模型的架构
        # model.add(tf.keras.layers.Flatten(input_shape=(1360, 720,))
        # model.add(tf.keras.layers.Dense(128, activation='tanh'))
        # model.add(tf.keras.layers.Dense(128, activation='tanh'))
        # model.add(tf.keras.layers.Dense(128, activation='tanh'))
        # model.add(tf.keras.layers.Dense(16, activation='linear'))
        # 这里虽然输出2，但第二个完全没用上

        model.compile(loss='mse', optimizer=tf.keras.optimizers.RMSprop(lr=self.learning_rate))
        self.model = model



    def save_exp(self, _state, _action, _reward, _next_state, _done):

        self.memory.append((_state, _action, _reward, _next_state, _done))

    # 经验池重放  根据尺寸获取  #  这里是训练数据的地方
    def train_exp(self, batch_size):
        # 确保每批返回的数量不会超出memory实际的存量，防止错误
        batches = min(batch_size, len(self.memory))
        # 从len(self.memory）中随机选出batches个数
        batches = np.random.choice(len(self.memory), batches)

        for i in batches:
            # 从经验数组中 取出相对的参数 状态，行为，奖励，即将发生的状态，结束状态
            _state, _action, _reward, _next_state, _done = self.memory[i]
            # print(_state.shape,"=========================这是state")
            _state = np.expand_dims(_state,axis=0)
            # 获取当前 奖励
            y_reward = _reward
            # 如果不是结束的状态，取得未来的折扣奖励
            # if not _done:
            #     # _target = 经验池.奖励 + gamma衰退值 * (model根据_next_state预测的结果)[0]中最大（对比所有操作中，最大值）
            #     # 根据_next_state  预测取得  当前的回报 + 未来的回报 * 折扣因子（gama）
            #     y_reward = _reward + self.gamma * np.amax(self.model.predict(_next_state)[0])
            #     # print('y_action', y_action)  # 1.5389154434204102

            # 获取，根据当前状态推断的 行为 input 4,output 2
            # _y = self.model.predict(_state)
            #_y的转化
            _y = get_y(y_reward,_action)
            # print("####################predict _y##############################")
            # print(_y)
            # print("#################################################")
            # print(_y,"这是yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
            # print(_action, y_reward, _y[0][_action], '_y', _y)  # [[0.08838317 0.16991007]]
            # 更新 将 某行为预测的 回报，分配到相应到 行为中  （_action = 1/0）
            # _y[0][_action] = y_reward
            # 训练  x： 4 当前状态  _y[0]：2
            jk = self.model.fit(_state, _y, epochs=1, verbose=0)
            # print("jkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjk")
            self.lossM.append(jk.history["loss"][0])
            # print("jkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjkjk")
        # 随着训练的继续，每次被随机值干涉的几率减少 * epsilon_decay倍数(0.001)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    # 输入状态，返回应该采取的动作。随机干涉会随着时间的推进，越来越少。
    def act(self, _state):  # 返回回报最大的奖励值，或 随机数

        # 随着训练的增加，渐渐减少随机
        # print(self.epsilon,"===========这是随机率")
        if np.random.rand() <= 0.4:
            # print("random ")
            # print('000000000',self.env.action_space.sample())
            return [random.choice([UP,DOWN,LEFT,RIGHT]),random.choice([UP,DOWN,LEFT,RIGHT])]
        else:
            # 使用预测值    返回，回报最大到最大的那个
            # print(_state.shape, "=====================================")
            _state = np.expand_dims(_state, axis=0)
            act_values = self.model.predict(_state)
            #for advio always return 0 i need de fushu
            tempF = False
            for i in act_values[0]:
                if i<0:
                    tempF = True
                    break
            if tempF:
                for i in range(len(act_values[0])):
                    act_values[0][i] = act_values+random.randint(1,10)


            return myAction[list(act_values[0]).index(max(list(act_values[0])))]  # returns action


def get_y(y_reward,action_):
    temp = []
    # maxY = list(y[0]).index(max(list(y[0])))
    # print(maxY,"这是maxY")
    action_index = myAction.index(action_)
    # print(action_index,"这是动作的标号")

    for i in range(maxAction):
        j = 0
        # if i ==maxY:
        #     j = random.uniform(0.4,0.8)
        temp.append(j)
    temp[action_index] = y_reward
    # print("================this is a guide value team11111111111======================\n")
    # print(temp)
    # print("===========================================================\n")
    return np.array([temp])


