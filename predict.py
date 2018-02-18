import numpy as np
from keras.preprocessing import image
from keras_vggface.vggface import VGGFace
from keras_vggface import utils

model = VGGFace(model='resnet50')

img = image.load_img('./image/ajb.jpg', target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = utils.preprocess_input(x, version=2)  # version=2 is valid for resnet50
preds = model.predict(x)
print('Predicted:', utils.decode_predictions(preds))
