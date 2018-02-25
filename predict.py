import time

import numpy as np
from keras.engine import Model
from keras.preprocessing import image
from keras_vggface import utils
from keras_vggface.vggface import VGGFace
from sklearn.neighbors import KNeighborsClassifier
from helpers import base64_png_image_to_pillow_image, load_image_references, load_labels, load_feature_descriptors, \
    load_image_resolutions
from settings import DESIRED_DIMENSIONS
from sklearn.neighbors import NearestNeighbors

class Classifier:
    def __init__(self):
        self.model = VGGFace(model='resnet50')

        feature_layer_name = 'flatten_1'
        feature_layer = self.model.get_layer(feature_layer_name)  # 2048-dimensional feature vector
        self.feature_descriptor_model = Model(self.model.input, feature_layer.output)

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
        feature_vectors = self.feature_descriptor_model.predict(x)
        print("Prediction execution time: {0:.2f} seconds".format(time.time() - run_start_time))
        prediction = predictions[0]
        decoded_prediction = self.decode_prediction(prediction, feature_vectors)

        return decoded_prediction

    def decode_prediction(self, prediction, feature_vectors, top=5):
        top_indices = list(prediction.argsort()[-top:][::-1])

        celebrities = []
        for i in top_indices:
            image_references = self.images_references[i]
            closest_image_reference, distance = self.get_closest_celebrity_image(image_references, feature_vectors)
            closest_image_url = '/celebrities/{}/{}'.format(*closest_image_reference)
            celebrity = {
                'name': self.labels[i],
                'score': float(prediction[i]),
                'closest_image_distance': distance,
                'closest_image': closest_image_url
            }
            celebrities.append(celebrity)
        celebrities.sort(key=lambda x: x['closest_image_distance'])
        return celebrities

    def get_closest_celebrity_image(self, image_references, input_feature_vectors):
        folder_name = image_references[0][0]
        feature_vectors = load_feature_descriptors(folder_name)
        image_resolutions = load_image_resolutions(folder_name)
        nearest_neighbours_model = NearestNeighbors(n_neighbors=8, algorithm='brute').fit(feature_vectors)
        vector_distances, neighbour_indexes = nearest_neighbours_model.kneighbors(input_feature_vectors)
        neighbour_distances_for_first_input = vector_distances[0]
        neighbour_indexes_for_first_input = neighbour_indexes[0]

        fallback_distance = None
        fallback_index = None
        highest_min_resolution = 1
        best_index = None
        best_distance = None
        for i in range(len(neighbour_distances_for_first_input)):
            index = neighbour_indexes_for_first_input[i]
            resolution = image_resolutions[index]  # (width, height) tuple
            min_dimension = min(resolution)
            # filter out images with very low resolution
            if min_dimension < 250:
                if min_dimension > highest_min_resolution:
                    highest_min_resolution = min_dimension
                    fallback_index = index
                    fallback_distance = neighbour_distances_for_first_input[i]
                continue
            best_index = index
            best_distance = neighbour_distances_for_first_input[i]
            break

        # In case all proposed images were low-res, pick the one with the highest resolution
        if best_index is None:
            best_index = fallback_index
            best_distance = fallback_distance

        return image_references[best_index], best_distance
