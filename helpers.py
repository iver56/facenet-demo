import base64
import io
import os

import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.utils.data_utils import get_file
from keras_vggface import utils
from keras_vggface.utils import V2_LABELS_PATH, VGGFACE_DIR
from resizeimage.resizeimage import resize_cover
from sklearn.externals import joblib

import settings


def load_feature_descriptors(folder_name):
    return joblib.load(os.path.join(settings.VGGFACE2_TRAIN_PATH, folder_name, 'feature_vectors.pkl'))


def load_image_resolutions(folder_name):
    return joblib.load(os.path.join(settings.VGGFACE2_TRAIN_PATH, folder_name, 'resolutions.pkl'))


def load_image_from_disk(file_path):
    that_image = Image.open(file_path)

    # Resize image
    that_image = resize_cover(that_image, settings.DESIRED_DIMENSIONS, validate=False)

    # Remove alpha channel
    that_image = that_image.convert('RGB')

    # Convert the PIL image to a numpy array
    x = img_to_array(that_image)
    x = np.expand_dims(x, axis=0)
    x = utils.preprocess_input(x, version=2)  # version=2 is valid for resnet50
    return x[0]


def base64_png_image_to_pillow_image(base64_string):
    img_data = base64.b64decode(str(base64_string))  # Decode base64
    image = Image.open(io.BytesIO(img_data))  # Decode the PNG data
    return image


def load_image_references():
    folder_filename_tuples = []  # a list with ordered lists of (folder, filename) tuples

    train_list_file_path = os.path.join(settings.VGGFACE2_META_PATH, 'train_list.txt')
    with open(train_list_file_path, 'r') as text_file:
        lines = text_file.readlines()
    lines = [line.strip() for line in lines]

    current_folder = None
    for line in lines:
        folder, filename = line.split('/')
        if current_folder != folder:
            folder_filename_tuples.append([])

        current_folder = folder
        folder_filename_tuples[-1].append((folder, filename))

    assert len(folder_filename_tuples) == 8631
    return folder_filename_tuples


def load_labels():
    file_path = get_file('rcmalli_vggface_labels_v2.npy', V2_LABELS_PATH, cache_subdir=VGGFACE_DIR)
    labels = np.load(file_path)
    labels = [label.replace('_', ' ').strip() for label in labels]
    return labels
