
# Implementacja obsługi ładowania i predykcji modelu

from keras.models import model_from_json
from keras.models import load_model
import cv2
import numpy as np

from PyQt6.QtGui import QImage

# load and evaluate a saved model
from numpy import loadtxt
from keras.models import load_model

def qimage_to_array(image: QImage):
    """
    Funkcja konwertująca obiekt QImage do numpy array
    """
    image = image.convertToFormat(QImage.Format.Format_Grayscale8)
    ptr = image.bits()
    ptr.setsize(image.sizeInBytes())
    numpy_array = np.array(ptr).reshape(image.height(), image.width(), 1)

    # wykorzystanie bibloteki OpenCV do wyświetlenia obrazu po konwersji
    #cv2.imshow('Check if the function works!', numpy_array)
    return numpy_array
    

def predict(image: QImage, model):
    """
    Funkcja wykorzystująca załadowany model sieci neuronowej do predykcji znaku na obrazie 

    Należy dodać w niej odpowiedni kod do obsługi załadowanego modelu
    """
    numpy_array = qimage_to_array(image)

    # wykorzystanie bibloteki OpenCV do zmiany wielkości obrazu do wielkości obrazów używanych w zbiorze MNIST
    numpy_array = cv2.resize(numpy_array, (28,28))

    # wykorzystanie bibloteki OpenCV do wyświetlenia obrazu po konwersji
    #cv2.imshow('Check if the function works!!', numpy_array)

    predictions = model.predict(numpy_array.reshape((1, 28, 28, 1)))

    # classes = ["0","1","2","3","4","5","6","7","8","9"]

    # print(np.argmax(predictions, axis=1))

    return np.argmax(predictions, axis=1)[0]

def get_model():
    """
    Funkcja wczytująca nauczony model sieci neuronowej 

    Należy dodać w niej odpowiedni kod do wczytywania na modelu oraz wag
    """
    # load model
    model = load_model('modelX.h5')

    # summarize model
    model.summary()
    return model 