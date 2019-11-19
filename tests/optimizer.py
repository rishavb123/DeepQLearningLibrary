import tensorflow as tf
import numpy as np

X = tf.Variable([0.2, -0.3])

optimizer = tf.optimizers.Adam()
for _ in range(10000):
    optimizer.minimize(lambda: sum(tf.square(X)), [X])
print(X)
