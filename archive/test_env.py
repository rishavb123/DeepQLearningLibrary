class TestEnv:

    def __init__(self):
        self.x = 0
        self.dx = 10

    def reset(self):
        self.x = 0

    def step(self, action):
        self.x += 1 if action[0] > 0 else -1
        self.x += 1 if action[1] > 0 else -1
        self.dx += 1 if self.x > self.dx else -1
        done = False
        if self.dx == self.x:
            done = True
        return (get_state(), -100 if done else 1, done, None)

    def get_state(self):
        return [self.x, self.dx]

    def render(self):
        print("\rCurrent State:", get_state(), end='')

    def close(self):
        pass