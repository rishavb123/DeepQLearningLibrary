import numpy as np
import gym

# env = gym.make('BipedalWalker-v3')
env = gym.make('LunarLander-v2')
# env = gym.make('CarRacing-v0')
# env = gym.make('CartPole-v1')
# env = gym.make('Berzerk-v0')
# env = gym.make('Pendulum-v0')

env.reset()
# print(env.action_space.n, len(env.reset()), env.reset().shape)
for _ in range(1000):
    env.render()
    act = env.action_space.sample()
    obs, reward, done, info = env.step(act) # take a random action
    print("Obs:", obs, "\tReward:", reward, "\tAction:", act, "\tDone:", done)
    if done:
        env.reset()

env.close()