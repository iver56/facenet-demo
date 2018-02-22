import time

import numpy as np
from keras.preprocessing import image
from keras_vggface import utils
from keras_vggface.vggface import VGGFace

from helpers import base64_png_image_to_pillow_image, load_image_references, load_labels
from settings import DESIRED_DIMENSIONS


class Classifier:
    def __init__(self):
        self.model = VGGFace(model='resnet50')
        self.model.summary()
        self.labels = load_labels()
        self.images_references = load_image_references()

    def predict(self, base64_png):
        # Convert base64 to Pillow image instance
        that_image = base64_png_image_to_pillow_image(base64_png)

        # Resize image
        that_image.thumbnail(DESIRED_DIMENSIONS)

        # Remove alpha channel
        that_image = that_image.convert('RGB')

        # Convert the PIL image to a numpy array
        x = image.img_to_array(that_image)
        x = np.expand_dims(x, axis=0)
        x = utils.preprocess_input(x, version=2)  # version=2 is valid for resnet50
        run_start_time = time.time()
        predictions = self.model.predict(x)
        print("Prediction execution time: {0:.2f} seconds".format(time.time() - run_start_time))
        prediction = predictions[0]
        decoded_prediction = self.decode_prediction(prediction)

        return decoded_prediction

    def decode_prediction(self, prediction, top=3):
        top_indices = list(prediction.argsort()[-top:][::-1])

        celebrities = [
            {
                'name': self.labels[i],
                'score': float(prediction[i]),
                'image_references': self.images_references[i]
            }
            for i in top_indices
        ]
        celebrities.sort(key=lambda x: x['score'], reverse=True)
        return celebrities
