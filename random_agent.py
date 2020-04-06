import numpy as np
import gym

from environments.gym import GymEnvironment
from environments.flappy_bird import FlappyBird

# env = GymEnvironment(gym.make('BipedalWalker-v2'))
env = FlappyBird()

for _ in range(1000):
    env.render()
    act = env.random_action()
    obs, reward, done, info = env.step(act) # take a random action
    print("Obs:", obs, "\tReward:", reward, "\tAction:", act, "\tDone:", done)
    if done:
        env.reset()

env.close()