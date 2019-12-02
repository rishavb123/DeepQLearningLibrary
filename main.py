import gym
import os
import sys
from gym import wrappers
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from dqn import DQN
from savgol_filter import savgol_filter

def play_episode(env, model, target_model, eps, gamma, copy_period, n, training=True):
    observation = env.reset()
    done = False
    totalreward = 0
    iters = 0
    while not done and iters < 500:

        if not training:
            env.render()
        print("\r\tEpisode:", format(n, '03d'), "Iteration:", format(iters, '04d'), end="")

        action = model.sample_action(observation, eps)
        prev_observation = observation
        observation, reward, done, info = env.step(action)
        
        totalreward += reward
        if done:
            reward -= 200

        if training:
            model.add_experience(prev_observation, action, reward, observation, done)
            model.train(target_model)

            if iters % copy_period == 0:
                target_model.copy_from(model)

        iters += 1
    print("\r", end="")
    return totalreward

def main():
    env = gym.make('CartPole-v0')
    gamma = 0.99
    copy_period = 50

    D = len(env.observation_space.sample())
    K = env.action_space.n
    sizes = [200, 200]
    
    model = DQN(D, K, sizes, gamma)
    tmodel = DQN(D, K, sizes, gamma)

    if 'monitor' in sys.argv:
        filename = os.path.basename(__file__).split('.')[0]
        monitor_dir = "./" + filename + '_' + str(datetime.now())
        env = wrappers.Monitor(env, monitor_dir)

    N = 500
    totalrewards = np.empty(N)

    for n in range(N):
        eps = 1.0 / np.sqrt(n+1)
        totalreward = play_episode(env, model, tmodel, eps, gamma, copy_period, n)
        totalrewards[n] = totalreward
        if n % 10 == 0:
            print("Episode:", n, "Total Reward:", totalreward, "Epsilon:", eps, "Avg Reward (last 10):", totalrewards[max(0, n-10):(n+1)].mean(), "Avg Reward (last 100):", totalrewards[max(0, n-100):(n+1)].mean())

    print("Avg Reward for Last 10 Episodes:", str(totalrewards[-10:].mean()) + ";", "Avg Reward for Last 100 Episodes:", totalrewards[-100:].mean())
    print("total rewards:", totalrewards.sum())

    plt.plot(totalrewards)
    plt.plot(savgol_filter(totalrewards, 30, 4))
    plt.title("Rewards")
    plt.show()

    input("Now lets watch it play a game: ")
    print(play_episode(env, model, tmodel, 0, gamma, copy_period, N, training=False))

if __name__ == '__main__':
    main()