from .. import environment

class GymEnvironment(environment.Environment):

    def __init__(self, gym_env):
        self.gym_env = gym_env
        self.state_len = len(self.gym_env.reset())

    def step(self, action):
        return self.gym_env.step(action)

    def reset(self):
        return self.gym_env.reset()

    def random_action(self):
        return self.gym_env.action_space.sample()

    def num_of_actions(self):
        return self.gym_env.action_space.n

    def len_of_state(self):
        return self.state_len
