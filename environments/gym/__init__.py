from .. import Environment

class GymEnvironment(Environment):

    def __init__(self, gym_env):
        self.gym_env = gym_env
        self.state = self.gym_env.reset()
        self.state_len = len(self.state)

    def step(self, action):
        temp = self.gym_env.step(action)
        self.state = temp[0]
        return temp

    def reset(self):
        self.state = self.gym_env.reset()
        return self.state

    def random_action(self):
        return self.gym_env.action_space.sample()

    def num_of_actions(self):
        return self.gym_env.action_space.n

    def len_of_state(self):
        return self.state_len

    def render(self):
        return self.gym_env.render()

    def close(self):
        self.gym_env.close()

    def get_state(self):
        return self.state