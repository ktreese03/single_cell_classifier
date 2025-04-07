import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import pyreadr
import os
from joblib import load


# Load the pre-trained model(s) for predicting the stage closest to the target dataset 
print(f"Loading model...")
model = load_model('modelAdult.keras')
# model = load_model('modelP48.keras')
# model = load_model('modelP24.keras')
print(f"Model shape: {model.input_shape}")


# Load average expression values of the training set, for the stage closest to the target dataset
print(f"Loading average expression values...")
mean = np.load('meanAdult.npy')
# mean = np.load("meanP48.npy)
# mean = np.load("meanP24.npy)


# Import target dataset (see Readme.txt for requirements). These lines are required if you are importing the RDS file. Use the function "pyreadr.read_r" to read the file.
print(f"Loading target dataset...")
result = pyreadr.read_r('../target_expressionMatrix.rds')
Target = result[None]
Target = Target.T
print(f"Target dataset shape: {Target.shape}")


# mean-center
Target -= mean


# You can alternatively center with the mean of your own dataset. This could provide additional domain adaptation but should only be used if your dataset originates from whole optic lobes, i.e. not a subset achieved by FACS etc.
# meanTarget = Target.mean(axis=0)
# Target -= meanTarget


# Load the encoder
print(f"Loading encoder...")
encoder = load('Encoder_multinet.joblib')
print(f"Encoder classes: {encoder.classes_}")


# Load the encoder
print(f"Loading encoder...")
encoder = load('Encoder_multinet.joblib')
print(f"Encoder classes: {encoder.classes_}")


# Function to make prediction
def predict_with_confidence(model, x, no_classes, n_iter=500):
    prediction = model.predict(x)
    softmax = np.amax(prediction, axis=1)
    classes = np.argmax(prediction, axis=1)

    @tf.function
    def f(x):
        return model(x, training=True)

    bootstrap = np.zeros((n_iter,) + (x.shape[0], no_classes))
    for i in range(n_iter):
        bootstrap[i, :, :] = f(x).numpy()

    BSmax = np.argmax(bootstrap, axis=2)
    confidence = np.sum(BSmax == classes, axis=0) / BSmax.shape[0]
    return classes, softmax, confidence


# If you are classifying a large dataset on a machine with limited memory, use this alternative function instead
# def predict_with_confidence(model, x, no_classes, n_iter=100):
#     prediction = model.predict(x)
#     softmax = np.amax(prediction, axis=1)
#     classes = np.argmax(prediction, axis=1)
    
#     @tf.function
#     def f(x):
#         return model(x, training=True)
    
#     bootstrap = np.zeros((n_iter, x.shape[0], no_classes))
#     for i in range(n_iter):
#         bootstrap[i, :, :] = f(x).numpy()
#     BSmax1 = np.argmax(bootstrap, axis=2)    
    
#     bootstrap = np.zeros((n_iter, x.shape[0], no_classes))
#     for i in range(n_iter):
#         bootstrap[i, :, :] = f(x).numpy()
#     BSmax2 = np.argmax(bootstrap, axis=2) 
    
#     bootstrap = np.zeros((n_iter, x.shape[0], no_classes))
#     for i in range(n_iter):
#         bootstrap[i, :, :] = f(x).numpy()
#     BSmax3 = np.argmax(bootstrap, axis=2) 
    
#     bootstrap = np.zeros((n_iter, x.shape[0], no_classes))
#     for i in range(n_iter):
#         bootstrap[i, :, :] = f(x).numpy()
#     BSmax4 = np.argmax(bootstrap, axis=2) 
    
#     bootstrap = np.zeros((n_iter, x.shape[0], no_classes))
#     for i in range(n_iter):
#         bootstrap[i, :, :] = f(x).numpy()
#     BSmax5 = np.argmax(bootstrap, axis=2) 
    
#     BSmax = np.concatenate((BSmax1, BSmax2, BSmax3, BSmax4, BSmax5), axis=0)
#     confidence = np.sum(BSmax == classes, axis=0) / BSmax.shape[0]
#     return classes, softmax, confidence


# Predict using the new dataset
print("Making predictions with confidence estimation...")
prediction, softmax, confidence = predict_with_confidence(model, Target, 259)


# Transform predictions back to clusters using the inverse encoder
preds = encoder.inverse_transform(prediction)


# Quick check of confidences
sample_indices = np.random.choice(len(preds), 10, replace=False)
print("Sample Predicted Clusters:", preds[sample_indices])
print("Sample Confidence Scores:", confidence[sample_indices])


# Combine clusters and confidence scores into a single array
combined_array = np.vstack((preds, confidence)).T


# Save the combined array to a text file in the specified directory
print(f"Saving predictions and confidence scores...")
np.savetxt('Predictions_and_Confidences.txt', X=combined_array, delimiter=',', fmt='%s,%.6f', header='Cluster,Confidence', comments='')


# Plot and save confidence scatter plot
plt.figure(figsize=(20,10))
plt.scatter(preds, confidence, alpha=0.1)
plt.xlabel("Class")
plt.ylabel("Confidence")
plt.savefig(os.path.expanduser('TargetDataset_Confidences.png'))
plt.show()


# Optional: Plot and save softmax vs confidence scatter plot
# plt.figure(figsize=(10,10))
# plt.scatter(softmax, confidence, alpha=0.1)
# plt.xlabel("Softmax")
# plt.ylabel("Confidence")
# plt.savefig(os.path.join(directory_path, 'SoftmaxVSConfidence.png'))
# plt.show()
