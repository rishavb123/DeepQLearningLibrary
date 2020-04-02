import tensorflow as tf

class DQN:
    def __init__(self, num_of_actions, input_dims, hidden_layers, activation='relu', learning_rate=0.001):
        layers = []
        first = True
        for dim in hidden_layers:
            if first:
                layers.push(tf.keras.layers.Dense(dim, inputs_shape=(input_dims), activation=activation))
            else:
                layers.push(tf.keras.layers.Dense(dim, activation=activation))
        layers.push(tf.keras.layers.Dense(num_of_actions))
        self.model = tf.keras.Sequential(layers)

        self.model.compile(opimizer=tf.keras.optimizers.Adam(learning_rate), loss='mse')

    def get_model(self):
        return self.model