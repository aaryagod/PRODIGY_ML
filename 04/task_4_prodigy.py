# -*- coding: utf-8 -*-
"""Task 4 prodigy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1m2ZzfOX1Us3Wz9-X4wf2WmswBR8UPtcj

Task 3 Prodigy

By Aarya Godbole

ML Track
"""

# STEP 1: Upload kaggle.json
from google.colab import files
files.upload()  # Upload your kaggle.json here

# STEP 2: Set up Kaggle API and download dataset
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json
!kaggle datasets download -d gti-upm/leapgestrecog

# STEP 3: Unzip dataset
import zipfile
with zipfile.ZipFile("leapgestrecog.zip", 'r') as zip_ref:
    zip_ref.extractall("leapGestRecog")

print("✅ Dataset extracted.")

# STEP 4: Import libraries
import os
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# STEP 5: Prepare data
img_width, img_height = 64, 64
batch_size = 32
data_dir = '/content/leapGestRecog/leapGestRecog'

train_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

train_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    subset='training',
    color_mode='grayscale'
)

val_generator = train_datagen.flow_from_directory(
    data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation',
    color_mode='grayscale'
)

# STEP 6: Build CNN model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 1)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dropout(0.5),
    Dense(128, activation='relu'),
    Dense(train_generator.num_classes, activation='softmax')
])

# STEP 7: Compile and train model
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

epochs = 15
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=epochs
)

# STEP 8: Plot accuracy and loss
plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Model Accuracy')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.legend()
plt.show()

# STEP 9: Save model
model.save('hand_gesture_cnn_model.h5')
print("✅ Model saved as hand_gesture_cnn_model.h5")

