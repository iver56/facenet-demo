import numpy as np
from keras.preprocessing import image
from keras_vggface.vggface import VGGFace
from keras_vggface import utils

from helpers import base64_png_image_to_pillow_image


class Classifier:
    DESIRED_DIMENSIONS = (224, 224)

    def __init__(self):
        self.model = VGGFace(model='resnet50')

    def predict(self, base64_png):
        # Convert base64 to Pillow image instance
        that_image = base64_png_image_to_pillow_image(base64_png)

        # Resize image
        that_image.thumbnail(self.DESIRED_DIMENSIONS)

        # Remove alpha channel
        that_image = that_image.convert('RGB')

        #that_image = image.load_img('./image/ajb.jpg', target_size=(224, 224))
        # Convert the PIL image to a numpy array
        x = image.img_to_array(that_image)
        x = np.expand_dims(x, axis=0)
        x = utils.preprocess_input(x, version=2)  # version=2 is valid for resnet50
        predictions = self.model.predict(x)
        decoded_predictions = utils.decode_predictions(predictions)

        return decoded_predictions
