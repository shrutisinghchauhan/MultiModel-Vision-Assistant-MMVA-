import os
import numpy as np
from PIL import Image

MODEL_PATH = 'models/vgg16.h5'
_model = None  # loaded lazily so the app still starts if vgg16.h5 is missing


def _load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            return None
        import tensorflow as tf
        _model = tf.keras.models.load_model(MODEL_PATH)
    return _model


def get_high_confidence_class(predictions, threshold=0.9):
    class_index = np.argmax(predictions)
    if predictions[0][class_index] >= threshold:
        return class_index
    return None


def predict(image):
    model = _load_model()
    if model is None:
        return None
    img = image.convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return model.predict(img_array)


def reverse_encoding(high_confidence_class):
    mapping = {
        0: "NORMAL LUNG CHEST CASE",
        1: "BACTERIAL LUNG CHEST CASE",
        2: "VIRAL LUNG CHEST CASE",
    }
    return mapping.get(high_confidence_class, "NOTHING")


def predictive_label(image):
    val = predict(image)
    if val is None:
        return "NOTHING"
    high_confidence_class = get_high_confidence_class(val, threshold=0.9)
    return reverse_encoding(high_confidence_class)
