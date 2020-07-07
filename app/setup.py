import json
import os

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np

checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

print(tf.__version__)
trainingData= json.loads(open("trainingData.json","r").read())
trainingAnswers= json.loads(open("trainingAnswers.json","r").read())
# testingData= json.loads(open("testingData.json","r").read())
# testingAnswers= json.loads(open("testingAnswers.json","r").read())
model = keras.Sequential([
    keras.layers.Dense(13),
    keras.layers.Dense(128, activation='relu'),
    # keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(16)
])
print(len(trainingAnswers))
model.compile(optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])
# cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
#                                                  save_weights_only=True,
#                                                  verbose=1)
model.fit(trainingData, 
          trainingAnswers,  
          epochs=50)
        #   validation_data=(testingData,testingAnswers),
        #   callbacks=[cp_callback])

# test_loss, test_acc = model.evaluate(testingData,  testingAnswers, verbose=2)

# print('\nTest accuracy:', test_acc)

model.save('saved_model/nextgen_1') 
