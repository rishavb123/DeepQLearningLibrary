import gym
import os
import sys
from gym import wrappers
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

from dqn import DQN
from savgol_filter import savgol_filter

def play_episode(env, model, target_model, eps, gamma, copy_period, n, max_steps=500, training=True):
    observation = env.reset()
    done = False
    totalreward = 0
    iters = 0

    env._max_episode_steps = max_steps + 1

    while not done and iters < max_steps:


        action = model.sample_action(observation, eps)
        prev_observation = observation
        observation, reward, done, info = env.step(action)
        
        totalreward += reward
        if done:
            reward -= 200

        if not training:
            env.render()
        else:
            print("\r\tEpisode:", format(n, '03d'), "Iteration:", format(iters, '04d'), 'Reward:', "{:7.2f}".format(reward), 'Total Reward:', "{:7.2f}".format(totalreward), 'Observation', observation, 'Action:', action, end="")

        if training:
            model.add_experience(prev_observation, action, reward, observation, done)
            model.train(target_model)

            if iters % copy_period == 0:
                target_model.copy_from(model)

        iters += 1
    env.close()
    print("\r" + " "*100, end="")
    return totalreward

def play_model(env, model, tmodel, gamma, copy_period):
    ans = 'y'
    while ans == 'y':
        ans = input("Would you like to watch the model play a game? (Y/n): ").lower()
        print("Total Reward:", play_episode(env, model, tmodel, 0, gamma, copy_period, -1, max_steps=5000, training=False))

def main():
    # env = gym.make('CartPole-v0')
    # gamma = 0.99
    # copy_period = 10
    # print_period = 5
    # N = 100

    # D = len(env.observation_space.sample()) if not isinstance(env.observation_space.sample(), int) else 1
    # K = env.action_space.n
    # sizes = [50, 50]

    from test_env import TestEnv
    env = TestEnv()
    gamma = 0.99
    copy_period = 5
    print_period = 5
    N = 30

    D = 2
    K = 2
    sizes = [10, 10]
    
    model = DQN(D, K, sizes, gamma)
    tmodel = DQN(D, K, sizes, gamma)

    play_model(env, model, tmodel, gamma, copy_period)

    if 'monitor' in sys.argv:
        filename = os.path.basename(__file__).split('.')[0]
        monitor_dir = "./" + filename + '_' + str(datetime.now())
        env = wrappers.Monitor(env, monitor_dir)

    totalrewards = np.empty(N)

    for n in range(N):
        eps = 1.0 / np.sqrt(n+1)
        totalreward = play_episode(env, model, tmodel, eps, gamma, copy_period, n)
        totalrewards[n] = totalreward
        if n % print_period == 0:
            print("Episode:", n, "Total Reward:", totalreward, "Epsilon:", eps, "Avg Reward (last " + str(print_period) + "):", totalrewards[max(0, n-print_period):(n+1)].mean())

    print("Avg Reward (last " + str(print_period) + "):", str(totalrewards[-print_period:].mean()) + ";")
    print("total rewards:", totalrewards.sum())

    plt.plot(totalrewards)
    plt.plot(savgol_filter(totalrewards, 30, 4))
    plt.title("Rewards")
    plt.show()

    play_model(env, model, tmodel, gamma, copy_period)

if __name__ == '__main__':
    main()