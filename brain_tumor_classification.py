# -*- coding: utf-8 -*-
"""Brain_Tumor_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q03820rTAM_Eol-qZgfFlGcd40DP3-ag
"""

import os
import numpy as np
import cv2
from PIL import Image
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt

from google.colab import drive
drive.mount('/content/drive')

tf.test.gpu_device_name()

data_generator = ImageDataGenerator(
    rescale=1./255,
    rotation_range=10,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    zoom_range=0.2
)

train_folder = "/content/drive/MyDrive/All__Datasets/brain tumor/Training"
batch_size = 32

train_data = data_generator.flow_from_directory(
    train_folder,
    target_size=(224, 224),
    batch_size=batch_size,
    class_mode='categorical',
    color_mode='grayscale'
)

import matplotlib.pyplot as plt
import os
train_dir = "/content/drive/MyDrive/All__Datasets/brain tumor/Training"
valid_extensions=('.jpg', '.png', '.jpeg')

categories = ["glioma", "meningioma", "notumor", "pituitary"]

plt.figure(figsize=(10, 6))
for i, category in enumerate(categories):
    folder_path = os.path.join(train_dir, category)
    image_path = os.path.join(folder_path, os.listdir(folder_path)[0])
    if not image_path.lower().endswith(valid_extensions):
        continue
    img = plt.imread(image_path)
    plt.subplot(2, 2, i+1)
    plt.imshow(img)
    plt.title(category)
    plt.axis("off")
plt.tight_layout()
plt.show()

model = models.Sequential()
model.add(layers.Conv2D(16, (3, 3), activation='relu', input_shape=(224, 224, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(4, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(train_data, epochs=20)

history.history.keys()

import matplotlib.pyplot as plt

plt.plot(history.history['accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train'],loc='upper left')
plt.show()

import matplotlib.pyplot as plt

plt.plot(history.history['loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train'],loc='upper right')
plt.show()

model.save('/content/drive/MyDrive/saved models/brain_tumor_2.h5')

from tensorflow.keras.models import load_model
loaded_model = load_model('/content/drive/MyDrive/saved models/brain_tumor_2.h5')

test_image_path = '/content/drive/MyDrive/All__Datasets/brain tumor/Testing/pituitary/Te-pi_0294.jpg'
test_image = cv2.imread(test_image_path, cv2.IMREAD_GRAYSCALE)
test_image = cv2.resize(test_image, (224, 224))
test_image = np.expand_dims(test_image, axis=-1)
test_image = np.expand_dims(test_image, axis=0)
test_image = test_image / 255.0

prediction = loaded_model.predict(test_image)
predicted_class_index = np.argmax(prediction)
class_names = train_data.class_indices
predicted_class = [key for key, value in class_names.items() if value == predicted_class_index][0]

plt.imshow(test_image.squeeze(), cmap='gray')
plt.title(f"Prediction: {predicted_class}")
plt.axis('off')
plt.show()





















