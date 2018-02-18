from keras.engine import Model
from keras.layers import Flatten, Dense
from keras_vggface.vggface import VGGFace

# custom parameters
num_classes = 2

vgg_model = VGGFace(model='resnet50', include_top=True, input_shape=(224, 224, 3))
