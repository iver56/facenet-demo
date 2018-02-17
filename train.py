from keras.engine import Model
from keras.layers import Flatten, Dense
from keras_vggface.vggface import VGGFace

# custom parameters
num_classes = 2

vgg_model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3))
last_layer = vgg_model.get_layer('avg_pool').output
x = Flatten(name='flatten')(last_layer)
out = Dense(num_classes, activation='softmax', name='classifier')(x)
custom_vgg_model = Model(vgg_model.input, out)
