import tensorflow as tf
import numpy as np

class DQN:
    def __init__(self, num_of_actions, input_dims, hidden_layers, activation='relu', learning_rate=0.001, orig_layers=[], model=None):
        if model == None:
            layers = orig_layers
            first = len(layers) == 0
            for dim in hidden_layers:
                if first:
                    layers.append(tf.keras.layers.Dense(dim, input_shape=(input_dims, ), activation=activation))
                else:
                    layers.append(tf.keras.layers.Dense(dim, activation=activation))
            layers.append(tf.keras.layers.Dense(num_of_actions))
            self.model = tf.keras.Sequential(layers)
            self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate), loss='mse')
        else:
            self.model = tf.keras.models.clone_model(model)
            self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate), loss='mse')
            self.model.set_weights(model.get_weights())

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model

    def load_model(self, model_file):
        self.model.load_weights(model_file)

    def save_model(self, model_file):
        self.model.save_weights(model_file)

    def copy_from(self, dqn):
        self.model.set_weights(dqn.get_model().get_weights())