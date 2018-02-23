import os
import time

import numpy as np
from PIL import Image
from sklearn.externals import joblib

from helpers import load_image_references
from settings import VGGFACE2_TRAIN_PATH

if __name__ == '__main__':
    image_references = load_image_references()

    for celebrity_images in image_references:
        folder_name = celebrity_images[0][0]
        image_resolutions = []

        load_images_start_time = time.time()

        for image_reference in celebrity_images:
            file_name = image_reference[1]
            file_path = os.path.join(VGGFACE2_TRAIN_PATH, folder_name, file_name)
            that_image = Image.open(file_path)
            image_resolutions.append(that_image.size)  # width, height

        image_resolutions = np.array(image_resolutions)
        print("Loaded {} images from {} in {:.2f} seconds".format(
            len(image_resolutions), folder_name, time.time() - load_images_start_time)
        )

        resolutions_file_path = os.path.join(VGGFACE2_TRAIN_PATH, folder_name, 'resolutions.pkl')
        joblib.dump(image_resolutions, resolutions_file_path, compress=True)
