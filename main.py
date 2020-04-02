import tensorflow as tf
import numpy as np
import gym
import matplotlib.pyplot as plt

from agent import Agent
from savgol_filter import savgol_filter

if __name__ == '__main__':
    env = gym.make('CartPole-v1')
    n_games = int(input('How many games should the AI train on? '))
    agent = Agent(
        gamma=0.99,
        epsilon=1.0,
        alpha=0.0005, 
        input_dims=len(env.reset()), 
        num_of_actions=env.action_space.n, 
        mem_size=1000000, 
        batch_size=64, 
        epsilon_decay=0.999, 
        epsilon_min=0.01,
        model_file=input('Name the file the AI should save its brain? ') + '.h5'
    )

    brain_file = input("What file should the AI load in a brain from a file? ")
    if brain_file != "" and brain_file.lower() != "none":
        agent.load_model(brain_file)

    scores = []

    for i in range(n_games):
        done = False
        score = 0
        observation = env.reset()

        while not done:
            action = agent.choose_action(observation)
            next_observation, reward, done, info = env.step(action)
            score += reward
            agent.remember(observation, action, reward, next_observation, done)
            observation = next_observation
            agent.learn()

        scores.append(score)

        avg_score = np.mean(scores[max(0, i - 100): i + 1])
        print('Episode ', i, 'Score %.2f' % score, 'Average Score %.2f' % avg_score)

        if i % 10 == 0 and i > 0:
            agent.save_model()

        plt.plot(scores)
        plt.plot(savgol_filter(scores, 30, 4))
        plt.savefig(agent.model_file[:-3] + '-scores.png')
        plt.show()