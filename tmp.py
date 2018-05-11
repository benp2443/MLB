import tensorflow as tf
hello = tf.constant('fuck you Ben.')
sess = tf.Session()
print(sess.run(hello))
