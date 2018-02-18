import numpy as np
from keras.preprocessing import image
from keras.utils.data_utils import get_file
from keras_vggface import utils
from keras_vggface.utils import V2_LABELS_PATH, VGGFACE_DIR
from keras_vggface.vggface import VGGFace

from helpers import base64_png_image_to_pillow_image


class Classifier:
    DESIRED_DIMENSIONS = (224, 224)

    def __init__(self):
        self.model = VGGFace(model='resnet50')
        file_path = get_file('rcmalli_vggface_labels_v2.npy', V2_LABELS_PATH, cache_subdir=VGGFACE_DIR)
        self.labels = np.load(file_path)

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
        decoded_predictions = self.decode_predictions(predictions)
        decoded_prediction = decoded_predictions[0]

        return decoded_prediction

    def decode_predictions(self, predictions, top=5):
        results = []
        for prediction in predictions:
            top_indices = prediction.argsort()[-top:][::-1]
            result = [[self.labels[i], prediction[i]] for i in top_indices]
            result.sort(key=lambda x: x[1], reverse=True)
            results.append(result)
        return results
