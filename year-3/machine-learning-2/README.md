# Urban Sound Classification with Deep Learning

## About the Project

This project was developed for the *Machine Learning II* course and focused on the implementation and evaluation of Deep Learning models for **urban sound classification** using the **UrbanSound8K** dataset.

The main objective was to classify environmental audio clips into 10 different sound categories, including car horns, dog barks, drilling, sirens, street music, and gunshots.

Two Deep Learning approaches were implemented and compared:

- **Multilayer Perceptron (MLP)**
- **Convolutional Neural Network (CNN)**

The project included:
- Audio preprocessing and normalization
- Feature extraction
- Data augmentation
- Model training and optimization
- Performance evaluation using 10-fold cross-validation
- Adversarial robustness analysis using DeepFool

---

# Project Structure

The repository contains three notebooks that should be executed in the following order:

## Notebook 1 — Data Preparation and Preprocessing
This notebook performs:
- Dataset analysis and class distribution inspection
- Data augmentation for minority classes
- Audio normalization and preprocessing
- Uniformization of sample rate and duration
- Feature extraction for Deep Learning models

Main preprocessing techniques:
- Time Stretching
- Pitch Shifting
- Noise Injection
- Temporal Shifting
- MFCC extraction
- Mel Spectrogram generation
- Chroma and spectral feature extraction

The preprocessing pipeline ensures that all audio samples have consistent dimensions and are suitable for model training.

---

## Notebook 2 — MLP Classifier
Implementation and training of a **Multilayer Perceptron (MLP)** model for urban sound classification.

Features used:
- MFCCs
- Delta and Delta-Delta coefficients
- Chroma features
- Spectral features
- Mel Spectrogram statistics
- Tonnetz features

Main techniques:
- Batch Normalization
- Dropout Regularization
- Random Search hyperparameter tuning
- Early stopping

The notebook also includes:
- Performance evaluation
- Accuracy analysis across folds
- Confusion matrix generation
- DeepFool adversarial robustness evaluation

---

## Notebook 3 — CNN Classifier
Implementation and training of a **2D Convolutional Neural Network (CNN)** for audio classification.

Input representations tested:
- MFCCs
- Mel Spectrograms

Main techniques:
- Conv2D architectures
- Batch Normalization
- MaxPooling
- Global Average Pooling
- Dropout
- Data Augmentation
- Early Stopping
- ReduceLROnPlateau

Several architectures and training strategies were evaluated to improve model performance.

The best results were achieved using:
- Mel Spectrogram inputs
- Data Augmentation
- EarlyStopping with patience = 10

---

# Results

## MLP
- Average Accuracy: **65.37%**
- Standard Deviation: **4.08%**

## CNN
Best-performing model:
- Average Accuracy: **76.18%**
- Standard Deviation: **3.36%**

The CNN model significantly outperformed the MLP approach, particularly when using Mel Spectrogram representations combined with data augmentation strategies.

---

# Dataset

This project uses the **UrbanSound8K** dataset:
- 8732 labeled urban sound excerpts
- 10 environmental sound classes
- Audio clips with duration ≤ 4 seconds

Dataset link:
https://urbansounddataset.weebly.com/urbansound8k.html

---

# Technologies and Libraries

- Python
- TensorFlow / Keras
- NumPy
- Pandas
- Librosa
- Scikit-learn
- Matplotlib

---

# Execution Order

Run the notebooks in the following order:

1. Notebook 1 — Data Preparation and Preprocessing  
2. Notebook 2 — MLP  
3. Notebook 3 — CNN  

This order is required to ensure that all processed data and extracted features are available for the training notebooks.

---

# Authors

- Ana Matilde Ferreira
- Maria Leonor Carvalho

---

# Course Information

- Course: Machine Learning II
- Degree: FCUP
- Professor: Francesco Renna
