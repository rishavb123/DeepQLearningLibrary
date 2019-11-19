import tensorflow as tf
import numpy as np

print("TensorFlow version: {}".format(tf.__version__))
print("Eager execution: {}".format(tf.executing_eagerly()))

x = np.array([
    [100, 105.4, 108.3, 111.1, 113, 114.7],
    [11, 11.8, 12.3, 12.8, 13.1, 13.6],
    [55, 56.3, 57, 58, 59.5, 60.4]
])

y = np.array([4000, 4200.34, 4700, 5300, 5800, 6400])


class Model(object):
    def __init__(self, x, y):
        # Initialize variable to (5.0, 0.0)
        # In practice, these should be initialized to random values.
        self.W = tf.Variable(tf.random.normal((len(x), len(x[0]))))
        self.b = tf.Variable(tf.random.normal((len(y),)))

    def __call__(self, x):
        return self.W * x + self.b


def loss(predicted_y, desired_y):
    return tf.reduce_sum(tf.square(predicted_y - desired_y))

optimizer = tf.optimizers.Adam(0.1)
# noinspection PyPep8Naming
def train(model, inputs, outputs):
    with tf.GradientTape() as t:
        current_loss = loss(model(inputs), outputs)
    grads = t.gradient(current_loss, [model.W, model.b])
    optimizer.apply_gradients(zip(grads,[model.W, model.b]))
    print(current_loss)


model = Model(x, y)

for i in range(10000):
    # print(model.b.numpy())
    train(model,x,y)