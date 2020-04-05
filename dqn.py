import tensorflow as tf

class DQN:
    def __init__(self, num_of_actions, input_dims, hidden_layers, activation='relu', learning_rate=0.001):
        layers = []
        first = True
        for dim in hidden_layers:
            if first:
                layers.append(tf.keras.layers.Dense(dim, input_shape=(input_dims, ), activation=activation))
            else:
                layers.append(tf.keras.layers.Dense(dim, activation=activation))
        layers.append(tf.keras.layers.Dense(num_of_actions))
        self.model = tf.keras.Sequential(layers)

        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate), loss='mse')

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model

    def load_model(self, model_file):
        self.model.load_weights(model_file)

    def save_model(self, model_file):
        self.model.save_weights(model_file)