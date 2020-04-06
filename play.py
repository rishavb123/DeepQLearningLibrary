import gym

from agent import Agent
from environments.gym import GymEnvironment

if __name__ == '__main__':
    env = GymEnvironment(gym.make('CartPole-v1'))
    agent = Agent(
        gamma=0.99,
        epsilon=0,
        alpha=0.0005, 
        input_dims=env.len_of_state(),
        num_of_actions=env.num_of_actions(), 
        mem_size=1000000, 
        batch_size=64, 
        epsilon_decay=0.999, 
        epsilon_min=0.01
    )

    agent.load_model("./models/" + input("What file should the AI load in a brain from a file? ") + '.h5')

    while input('Would you like to watch the AI play another game (Y/N): ')[0].lower() == 'y':
        done = False
        score = 0
        observation = env.reset()

        while not done:
            action = agent.choose_action(observation)
            observation, reward, done, info = env.step(action)
            score += reward
            env.render()

        env.close()

        print("Score was", score)