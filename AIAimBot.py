import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import cv2
import os

# Defining data paths
train_data_dir = 'path/to/your/training/data'
validation_data_dir = 'path/to/your/validation/data'

# Image dimensions
img_width, img_height = 64, 64

# Parameters
batch_size = 32
epochs = 10

# Data generators
train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

validation_generator = validation_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='binary')

# Build the model
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_width, img_height, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // batch_size)

# Save the model
model.save('red_circle_detector.h5')
Step 4: Detect and Click Red Circles
Once the model is trained, you can use it to detect red circles in real-time and simulate a mouse click:

python
Copy
import cv2
import numpy as np
import tensorflow as tf
import pyautogui

# Load trained model
model = tf.keras.models.load_model('red_circle_detector.h5')

# Function to preprocess the image
def preprocess_image(image):
    image = cv2.resize(image, (64, 64))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# Capture video from webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    processed_frame = preprocess_image(frame)

    # Predict
    prediction = model.predict(processed_frame)
    if prediction > 0.5:  # Assuming 1 is red circle and 0 is not
        print("Red circle detected!")
        # Get the center of the red circle
        center = (frame.shape[1] // 2, frame.shape[0] // 2)
        pyautogui.click(center[0], center[1])  # Simulate mouse click

    # Display the frame
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()