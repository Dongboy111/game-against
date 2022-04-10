UP = [0,-1]
DOWN = [0,1]
LEFT = [-1,0]
RIGHT= [1,0]


import tensorflow as tf

class DQN:
    def __init__(self,model,gamma=0.9,learnging_rate=0.01):
        self.model = model.model
        self.target_model = model.target_model
        self.gamma = gamma
        self.lr = learnging_rate

        self.model.optimizer = tf.optimizers.Adam(learning_rate=self.lr)
        self.model.loss_func = tf.losses.MeanSquaredError()
        self.global_step = 0
        self.update_target_steps = 200

    def predict(self, obs):
        """ 使用self.model的value网络来获取 [Q(s,a1),Q(s,a2),...]
        """
        return self.predict1(obs)

    def _train_step(self,action,features,labels):
        """ 训练步骤
        """
        with tf.GradientTape() as tape:
            # 计算 Q(s,a) 与 target_Q的均方差，得到loss
            predictions = self.model(features,training=True)
            enum_action = list(enumerate(action))
            pred_action_value = tf.gather_nd(predictions,indices=enum_action)
            loss = self.model.loss_func(labels,pred_action_value)
        gradients = tape.gradient(loss,self.model.trainable_variables)
        self.model.optimizer.apply_gradients(zip(gradients,self.model.trainable_variables))
        # self.model.train_loss.update_state(loss)
    def _train_model(self,action,features,labels,epochs=1):
        """ 训练模型
        """
        for epoch in tf.range(1,epochs+1):
            self._train_step(action,features,labels)

    def learn(self,obs,action,reward,next_obs,terminal):
        """ 使用DQN算法更新self.model的value网络
        """
        # 每隔200个training steps同步一次model和target_model的参数
        if self.global_step % self.update_target_steps == 0:
            self.replace_target()
        # 从target_model中获取 max Q' 的值，用于计算target_Q
        next_pred_value = self.target_model.predict(next_obs)
        best_v = tf.reduce_max(next_pred_value,axis=1)
        terminal = tf.cast(terminal,dtype=tf.float32)
        target = reward + self.gamma * (1.0 - terminal) * best_v

        # 训练模型
        self._train_model(action,obs,target,epochs=1)
        self.global_step += 1

    def replace_target(self):
        '''预测模型权重更新到target模型权重'''
        self.target_model.get_layer(name='l1').set_weights(self.model.get_layer(name='l1').get_weights())
        self.target_model.get_layer(name='l2').set_weights(self.model.get_layer(name='l2').get_weights())
        self.target_model.get_layer(name='l3').set_weights(self.model.get_layer(name='l3').get_weights())























    def predict1(self):

            import random
            return [random.choice(all),random.choice(all)]