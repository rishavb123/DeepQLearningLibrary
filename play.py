import gym

from agent import Agent

if __name__ == '__main__':
    env = gym.make('LunarLander-v2')
    agent = Agent(gamma=0.99, epsilon=0, alpha=0.0005, input_dims=8, n_actions=4, mem_size=1000000, batch_size=64, epsilon_dec=1, epsilon_min=0)

    agent.load_model(input('Name the file the AI should save its brain? ') + '.h5')

    while input('Would you like to watch the AI play another game (Y/N): ').lower() == 'y':
        done = False
        score = 0
        observation = env.reset()

        while not done:
            action = agent.choose_action(observation)
            observation, reward, done, info = env.step(action)
            score += reward
            env.render()

        print("Score was", score)