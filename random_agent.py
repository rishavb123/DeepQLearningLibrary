import numpy as np
# import gym

# from environments.gym import GymEnvironment
# from environments.flappy_bird import FlappyBird
from environments.coin_collector import CoinCollector

# env = GymEnvironment(gym.make('BipedalWalker-v2'))
# env = FlappyBird()
env = CoinCollector()

for _ in range(5000):
    env.render()
    act = env.random_action()
    obs, reward, done, info = env.step(act) # take a random action
    print("Obs:", obs, "\tReward:", reward, "\tAction:", act, "\tDone:", done)
    if done:
        env.reset()

env.close()