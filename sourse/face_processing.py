import dlib
import numpy as np
import tensorflow as tf

root_path = "Beauty_Makeup_Transfer/"
landmarks_checkpoint_path = root_path + "models/shape_predictor_5_face_landmarks.dat"
meta_graph_path = root_path + "models/model.meta"
checkpoint_path = root_path + "models"

def align_faces(img_path):
  # Read Image
  img = dlib.load_rgb_image(img_path)

  # Face Detection
  detector = dlib.get_frontal_face_detector()

  # Landmark Detection
  sp = dlib.shape_predictor(landmarks_checkpoint_path)
  dets = detector(img,1)
  objs = dlib.full_object_detections()

  for detection in dets:
    s = sp(img, detection)
    objs.append(s)

  faces = dlib.get_face_chips(img, objs, size=256, padding=0.35)

  return faces[0]

def preprocess(img):
  return img.astype(np.float32) / 127.5 -1           #0 ~ 255 -> -1 ~ 1

def postprocess(img):
  return ((img+1.)*127.5).astype(np.uint8)           #-1 ~ 1 -> 0 ~ 255

def apply_beautygan_filter(origin_img_path, style_img_path):
  tf.compat.v1.disable_eager_execution()
  with tf.compat.v1.Session() as sess:
    sess.run(tf.compat.v1.global_variables_initializer())

  sess = tf.compat.v1.Session()
  saver = tf.compat.v1.train.import_meta_graph(meta_graph_path)
  saver.restore(sess, tf.train.latest_checkpoint(checkpoint_path))
  graph = tf.compat.v1.get_default_graph()

  X = graph.get_tensor_by_name('X:0') #source
  Y = graph.get_tensor_by_name('Y:0') #reference
  Xs = graph.get_tensor_by_name('generator/xs:0') #output

  origin_img = align_faces(origin_img_path)

  style_img = align_faces(style_img_path)

  X_img = preprocess(origin_img)
  X_img = np.expand_dims(X_img,axis=0)

  Y_img = preprocess(style_img)
  Y_img = np.expand_dims(Y_img,axis=0)

  output = sess.run(Xs, feed_dict={
    X: X_img,
    Y: Y_img
  })

  output_img = postprocess(output[0])

  return output_img