import os

import time

import numpy as np
from keras.engine import Model
from keras_vggface.vggface import VGGFace
from sklearn.externals import joblib

from helpers import load_image_references, load_image_from_disk
from settings import VGGFACE2_TRAIN_PATH

if __name__ == '__main__':
    layer_name = 'flatten_1'
    vgg_model = VGGFace(model='resnet50')
    out = vgg_model.get_layer(layer_name).output  # 2048-dimensional feature vector
    feature_descriptor_model = Model(vgg_model.input, out)

    image_references = load_image_references()

    for celebrity_images in image_references:
        folder_name = celebrity_images[0][0]
        images = []

        load_images_start_time = time.time()

        for image_reference in celebrity_images:
            file_name = image_reference[1]
            file_path = os.path.join(VGGFACE2_TRAIN_PATH, folder_name, file_name)
            that_image = load_image_from_disk(file_path)
            images.append(that_image)
        images = np.array(images)
        print("Loaded and preprocessed {} images from {} in {:.2f} seconds".format(
            len(images), folder_name, time.time() - load_images_start_time)
        )
        predict_images_start_time = time.time()
        feature_vectors = feature_descriptor_model.predict(images)
        print("Feed forward in {:.2f} seconds".format(time.time() - predict_images_start_time))

        # Save disk space by quantizing the numbers to 16-bit floats
        feature_vectors = np.float16(feature_vectors)

        feature_file_path = os.path.join(VGGFACE2_TRAIN_PATH, folder_name, 'feature_vectors.pkl')
        joblib.dump(feature_vectors, feature_file_path, compress=True)
