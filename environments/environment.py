class Environment:

    def render(self):
        pass

    def step(self, action):
        return [], 0, False, None

    def reset(self):
        return []

    def random_action(self):
        return 0

    def num_of_actions(self):
        return 0

    def len_of_state(self):
        return 0
