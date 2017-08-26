# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# import sys
# import numpy as np
# import tensorflow as tf
# import cv2
# import tensorflow.python.platform
# from types import *
# from dlfunc import *

# CLASSES_NUM = 3
# IMAGE_SIZE_PX = 120
# IMAGE_PIXELS = IMAGE_SIZE_PX*IMAGE_SIZE_PX*3

# flags = tf.app.flags
# FLAGS = flags.FLAGS
# flags.DEFINE_string('readmodels', 'models/model.ckpt', 'File name of model data')

# if __name__ == '__main__':
#     test_image = []
#     for i in range(1, len(sys.argv)):
#         img = cv2.imread(sys.argv[i])
#         print(img)
#         height, width, channels = img.shape
#         if height >= IMAGE_SIZE_PX and width >= IMAGE_SIZE_PX:
#             img = img[0:IMAGE_SIZE_PX, 0:IMAGE_SIZE_PX] # cv2.resize(img, (IMAGE_SIZE_PX, IMAGE_SIZE_PX))
#         img = cv2.resize(img, (IMAGE_SIZE_PX, IMAGE_SIZE_PX))
#         test_image.append(img.flatten().astype(np.float32)/255.0)
#     test_image = np.asarray(test_image)

#     images_placeholder = tf.placeholder("float", shape=(None, IMAGE_PIXELS))
#     labels_placeholder = tf.placeholder("float", shape=(None, CLASSES_NUM))
#     keep_prob = tf.placeholder("float")

#     logits = inference(images_placeholder, keep_prob)
#     sess = tf.InteractiveSession()

#     saver = tf.train.Saver(tf.global_variables_initializer())
#     sess.run(tf.global_variables_initializer())
#     saver.restore(sess,FLAGS.readmodels)

#     for i in range(len(test_image)):
#         pr = logits.eval(feed_dict={
#             images_placeholder: [test_image[i]],
#             keep_prob: 1.0 })[0]
#         pred = np.argmax(pr)
#         print(pr)
#         print(pred)
#     print("finish")
