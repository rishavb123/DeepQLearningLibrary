import tensorflow as tf
import numpy as np
import gym
import matplotlib.pyplot as plt

from agent import Agent
from savgol_filter import savgol_filter

from environments.gym.gym_environment import GymEnvironment

if __name__ == '__main__':
    env = GymEnvironment(gym.make('LunarLander-v2'))
    n_games = int(input('How many games should the AI train on? '))
    agent = Agent(
        gamma=0.99,
        epsilon=1,
        alpha=0.0005, 
        input_dims=env.len_of_state(),
        num_of_actions=env.num_of_actions(), 
        mem_size=1000000, 
        batch_size=64, 
        epsilon_decay=0.999, 
        epsilon_min=0.01,
        model_file="./models/" + input('Name the file the AI should save its brain? ') + '.h5'
    )

    brain_file = input("What file should the AI load in a brain from a file? ")
    if brain_file != "" and brain_file.lower() != "none":
        agent.load_model("./models/" + brain_file + ".h5")

    scores = []

    for i in range(1, n_games + 1):
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
            # if i % 20 == 1:
            #     env.render()

        scores.append(score)

        avg_score = np.mean(scores[max(0, i - 100): i + 1])
        print('Episode ', i, 'Score %.2f' % score, 'Average Score %.2f' % avg_score)

        if i % 10 == 0:
            agent.save_model()

        if len(scores) > 10 and scores[-3] == 500 and scores[-2] == 500 and scores[-1] == 500:
            break

    agent.save_model()

    plt.plot(scores, label='Scores Over Iterations')
    plt.plot(savgol_filter(scores, n_games / 2, 4), label='Savgol Filter Smoothing')
    plt.legend()
    plt.savefig("./graphs/" + agent.model_file.split("/")[2][:-3] + '-scores.png')
    plt.show()