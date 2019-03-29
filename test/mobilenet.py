from keras.applications.mobilenet_v2 import MobileNetV2
from keras.preprocessing import image
from keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
import time

model = MobileNetV2(weights='imagenet')

img_path = 'photo.jpg'

for _ in range(10):
    start = time.time()

    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)

    end = time.time()
    print('Predicted:', decode_predictions(preds, top=3)[0])
    print('Time: %f s' % (end - start))
