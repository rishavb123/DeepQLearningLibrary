import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.backend as K
import numpy as np

m = 1000
n = 1
X = np.random.randn(m, n).astype(np.float32)
y = (3 + 0 * np.random.randn(m)).astype(np.float32)

def create_model():
    a_input = keras.layers.Input(shape=(n,), dtype=np.float32)
    a = K.expand_dims(a_input, axis=2)
    q = keras.layers.Conv1D(1, 1)(a)
    q = - tf.math.square(q) # this breaks things, but only when using tf.function
    model = keras.models.Model(inputs=a_input, outputs=q)
    return model

model = create_model()
model.predict(X)

class Trainer():
    def __init__(self, epochs=10):
        self.epochs = epochs
        self.model = create_model()
        self.optimizer = tf.optimizers.Adam()
        self.step = 0
    def train(self, X, y, epochs=10):
        X = tf.convert_to_tensor(X, dtype=tf.float32)
        y = tf.convert_to_tensor(y, dtype=tf.float32)
        for epoch in range(epochs):
            l = self._train_one_step(X, y)
        return l
    @tf.function
    def _train_one_step(self, X, y):
        with tf.GradientTape() as tape:
            yp = self.model(X)
            loss = tf.reduce_mean(tf.math.square(y - yp))
        gradients = tape.gradient(loss, self.model.trainable_variables)
        l = self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        d = dict(loss=loss)
        tf.print(yp[0], loss)
        self.step += 1

trainer = Trainer()
l = trainer.train(X, y, epochs=100)