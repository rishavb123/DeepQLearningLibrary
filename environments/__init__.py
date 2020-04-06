class Environment:

    def render(self):
        print("Using default render. Make sure to override this method!")

    def step(self, action):
        print("Using default step. Make sure to override this method!")
        return [], 0, False, None

    def reset(self):
        print("Using default reset. Make sure to override this method!")
        return []

    def random_action(self):
        print("Using default random_action. Make sure to override this method!")
        return 0

    def num_of_actions(self):
        print("Using default num_of_actions. Make sure to override this method!")
        return 0

    def len_of_state(self):
        print("Using default len_of_state. Make sure to override this method!")
        return 0

    def close(self):
        print("Using default close. Make sure to override this method!")

    def get_state(self):
        print("Using default get_state. Make sure to override this method!")
        return []