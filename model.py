from keras.models import Model
from keras.layers import Input, Flatten, Dropout, Lambda
from keras.layers import Dense, Conv2D

HEIGHT = 66
WEIGHT = 200


def MyModel():
    inputs = Input(shape=(HEIGHT, WEIGHT, 3))

    # Normalize
    x = Lambda(lambda x: x / 127.5 - 1.0, )(inputs)

    x = Conv2D(24, (5, 5), strides=(2, 2), activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Conv2D(36, (5, 5), strides=(2, 2), activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Conv2D(48, (5, 5), strides=(2, 2), activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Conv2D(64, (3, 3), strides=(1, 1), activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Conv2D(64, (3, 3), strides=(1, 1), activation='relu')(x)
    x = Dropout(0.2)(x)

    x = Flatten()(x)

    x = Dense(100, activation='relu')(x)
    x = Dropout(0.5)(x)

    x = Dense(50, activation='relu')(x)
    x = Dropout(0.5)(x)

    x = Dense(10, activation='relu')(x)

    outputs = Dense(1)(x)

    model = Model(inputs=inputs, outputs=outputs)
    model.summary()
    return model
