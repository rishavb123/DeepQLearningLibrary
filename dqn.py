import numpy as np
import tensorflow as tf

class DenseLayer:

    def __init__(self, M1, M2, f=tf.nn.tanh, use_bias=True):
        self.W = tf.Variable(np.random.random([M1, M2]).astype(np.float32))
        self.params = [self.W]
        self.use_bias = use_bias
        if use_bias:
            self.b = tf.Variable(np.zeros(M2).astype(np.float32))
            self.params.append(self.b)
        self.f = f

    def forward(self, X):
        return self.f(tf.matmul(X, self.W) + self.b if self.use_bias else tf.matmul(X, self.W))

class DQN:
    def __init__(self, D, K, hidden_layer_sizes, gamma, max_experience=10000, min_experience=100, batch_size=32):
        self.K = K
        self.layers = []
        M1 = D
        for M2 in hidden_layer_sizes:
            self.layers.append(DenseLayer(M1, M2))
            M1 = M2

        self.layers.append(DenseLayer(M1, K, f=lambda x: x))
        self.params = []
        for layer in self.layers:
            self.params += layer.params

        self.experience = []
        self.max_experience = max_experience
        self.min_experience = min_experience
        self.batch_size = batch_size
        self.gamma = gamma

        self.optimizer = tf.optimizers.Adam()

    def copy_from(self, other):
        for p, q in zip(self.params, other.params):
            p.assign(q)

    def predict(self, X):
        Z = np.atleast_2d(X).astype(np.float32)
        for layer in self.layers:
            Z = layer.forward(Z)
        return Z

    def train(self, target_network):
        if len(self.experience) < self.min_experience:
            return
        idx = np.random.choice(len(self.experience), size=self.batch_size, replace=False)
        states = [self.experience[i]['s'] for i in idx]
        actions = [self.experience[i]['a'] for i in idx]
        rewards = [self.experience[i]['r'] for i in idx]
        next_states = [self.experience[i]['s2'] for i in idx]
        dones = [self.experience[i]['done'] for i in idx]
        next_Q = np.max(target_network.predict(next_states), axis=1)
        targets = [r + self.gamma*next_q if not done else r for r, next_q, done in zip(rewards, next_Q, dones)]
        self.backprop(states, targets, actions)

    def loss(self, G, selected_action_values):
        return tf.reduce_sum(tf.square(G - selected_action_values))

    def backprop(self, X, G, actions, N=100):
        for _ in range(N):
            with tf.GradientTape() as t:
                Y_hat = self.predict(X)
                selected_action_values = tf.reduce_sum(Y_hat * tf.one_hot(actions, self.K, dtype='float32'), 1)
                current_loss = self.loss(G, selected_action_values)
            grads = t.gradient(current_loss, self.params)
            self.optimizer.apply_gradients(zip(grads, self.params))

    def add_experience(self, s, a, r, s2, done):
        if (len(self.experience)) >= self.max_experience:
            self.experience.pop(0)
        self.experience.append({'s': s, 'a': a, 'r': r, 's2': s2, 'done': done})

    def sample_action(self, x, eps):
        if np.random.random() < eps:
            return np.random.choice(self.K)
        else:
            return np.argmax(self.predict(x)[0])