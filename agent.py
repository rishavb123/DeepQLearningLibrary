import numpy as np
import tensorflow as tf

from replay_buffer import ReplayBuffer
from dqn import DQN

class Agent:
    def __init__(self, alpha, gamma, num_of_actions, epsilon, batch_size, input_dims, random_action_func=None, layers=[], epsilon_decay=0.996, copy_period=1, epsilon_min=0.01, mem_size=1000000, model_file='dqn_model.h5'):
        self.action_space = [i for i in range(num_of_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size
        self.model_file = model_file
        self.random_action_func = random_action_func if random_action_func != None else lambda:np.random.choice(self.action_space)
        self.copy_period = copy_period

        self.memory = ReplayBuffer(mem_size, input_dims, num_of_actions, discrete=True)
        self.dqn = DQN(num_of_actions, input_dims, [256, 256], learning_rate=alpha, orig_layers=layers)
        self.target_dqn = DQN(num_of_actions, input_dims, [256, 256], learning_rate=alpha, orig_layers=layers, model=self.dqn.get_model())
        self.learn_counter = 0

    def remember(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, state):
        state = state[np.newaxis, :]
        action = self.random_action_func() if np.random.random() < self.epsilon else np.argmax(self.dqn.get_model().predict(state))
        return action

    def learn(self):
        self.learn_counter += 1
        if self.memory.mem_counter < self.batch_size:
            return
        state, action, reward, new_state, done = self.memory.sample_buffer(self.batch_size)

        action_values = np.array(self.action_space, dtype=np.int8)
        action_indicies = np.dot(action, action_values)

        q_eval = self.target_dqn.get_model().predict(state)
        q_next = self.target_dqn.get_model().predict(new_state)

        q_target = q_eval.copy()

        batch_index = np.arange(self.batch_size, dtype=np.int32)

        q_target[batch_index, action_indicies] = reward + self.gamma * np.max(q_next, axis=1) * done
        
        self.dqn.get_model().fit(state, q_target, verbose=0)

        self.epsilon = self.epsilon * self.epsilon_decay if self.epsilon > self.epsilon_min else self.epsilon_min

        if self.learn_counter % self.copy_period == 0:
            self.target_dqn.copy_from(self.dqn)

    def save_model(self):
        self.dqn.save_model(self.model_file)

    def load_model(self, model_file=None):
        if model_file == None or model_file == "":
            model_file = self.model_file
        self.dqn.load_model(model_file)