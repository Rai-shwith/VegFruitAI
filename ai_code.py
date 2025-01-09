import tensorflow as tf
import numpy as np
from keras._tf_keras.keras.models import Sequential
from keras._tf_keras.keras import layers,losses
from keras._tf_keras.keras.utils import image_dataset_from_directory, load_img, img_to_array
from fastapi.middleware.cors import CORSMiddleware
import os

current_dir = os.getcwd()
# Paths to datasets and image
DATA_TRAIN_PATH = os.path.join(current_dir,"Fruits_Vegetables","train")
DATA_VALIDATION_PATH = os.path.join(current_dir,"Fruits_Vegetables","validation")
DATA_TEST_PATH = os.path.join(current_dir,"Fruits_Vegetables","test")
epoch_size = 25

image_width = 180
image_height = 180

data_train = image_dataset_from_directory(
    DATA_TRAIN_PATH,
    shuffle=True,
    image_size=(image_width,image_height),
    batch_size=32,
    validation_split=False
)
data_cat = data_train.class_names

data_val = image_dataset_from_directory(
    DATA_VALIDATION_PATH,
    shuffle=True,
    image_size=(image_width,image_height),
    batch_size=32,
    validation_split=False
)

data_test = image_dataset_from_directory(
    DATA_TEST_PATH,
    shuffle=True,
    image_size=(image_width,image_height),
    batch_size=32,
    validation_split=False
)

model = Sequential([
    layers.Rescaling(1/255),
    layers.Conv2D(16,3,padding="same",activation="relu"),
    layers.MaxPooling2D(),
    layers.Conv2D(32,3,padding="same",activation="relu"),
    layers.MaxPooling2D(),
    layers.Conv2D(64,3,padding="same",activation="relu"),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dropout(0.2),
    layers.Dense(128),
    layers.Dense(len(data_cat))
])

model.compile("adam",loss=losses.SparseCategoricalCrossentropy(from_logits=True),metrics=["accuracy"])

# Print model summary
model.summary()

history = model.fit(data_train,validation_data=data_val,epochs=epoch_size)

# Save the model
model.save("fruits_vegetables_model.keras")  # Save the model
print("Model saved successfully!")
