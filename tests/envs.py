import numpy as np
import gym

# env = gym.make('BipedalWalker-v3')
# env = gym.make('LunarLander-v2')
# env = gym.make('CarRacing-v0')
# env = gym.make('CartPole-v1')
env = gym.make('Berzerk-v0')

env.reset()
print(env.action_space.n, len(env.reset()), env.reset().shape)
shape = env.reset().shape
x = (shape[0], shape[1], shape[2], )
print(len(x))
# for _ in range(10000):
#     env.render()
#     env.step(env.action_space.sample()) # take a random action

env.close()