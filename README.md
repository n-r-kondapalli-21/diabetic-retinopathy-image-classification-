# A Hybrid CNN Model for Diabetic Retinopathy Classification

## Overview

This project implements a system for the automatic classification of Diabetic Retinopathy (DR) from fundus images. It utilizes a hybrid approach combining a Generative Adversarial Network (GAN) to generate synthetic retinal images and a Convolutional Neural Network (CNN) to classify the severity of DR.

The application provides a graphical user interface (GUI) built with Tkinter to interact with the models.

## Features

-   **Image Generation**: A Deep Convolutional GAN (DCGAN) is used to generate realistic 32x32 fundus images.
-   **DR Classification**: A CNN model classifies the generated images into five stages of diabetic retinopathy:
    1.  No DR
    2.  Mild
    3.  Moderate
    4.  Severe
    5.  Proliferative DR
-   **Graphical User Interface**: An interactive GUI to load models, generate images, and view predictions.

## How It Works

The workflow is divided into two main parts:

1.  **GAN for Image Synthesis**: The GAN is trained on a dataset of fundus images to learn the underlying data distribution. The generator part of the GAN can then produce new, synthetic fundus images from random noise vectors. In this project, the GAN is used to augment the dataset and provide a stream of images for classification.

2.  **CNN for Classification**: A standard CNN is trained on a labeled dataset of fundus images, where each image is assigned a severity grade. This trained model takes an image as input and outputs the predicted DR stage.

The main application uses a pre-trained GAN generator to create images and then feeds them to the pre-trained CNN for classification.

## Directory Structure

```
.
├── dataset/              # Contains the training images sorted into subfolders by class (0-4)
├── model/                # Contains pre-trained models (GAN generator, CNN classifier)
├── img/                  # Directory for saving generated images
├── main.py               # Main application file with the Tkinter GUI
├── TrainModel.py         # Script to train the CNN classification model
├── GANModel.py           # Script to define and train the GAN model
├── GeneratePredict.py    # Script for generating images and making predictions (likely for testing)
├── retina.py             # (purpose to be clarified)
├── requirements.txt      # Project dependencies
└── README.md
```

## System Requirements

-   Python 3.7
-   TensorFlow 1.14.0
-   Keras 2.3.1
-   OpenCV

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install the dependencies:**
    The project contains two requirement files. `req.txt` seems more accurate.
    ```bash
    pip install -r req.txt
    ```
    Note: Some packages might have installation issues on newer systems. `tensorflow==1.14.0` requires a compatible version of Python (like 3.7) and other system libraries. You might also need to install `imutils`:
    ```bash
    pip install imutils
    ```

## How to Run

To start the application, run the `retina.py` script:

```bash
python main.py
```

This will open the GUI. From there, you can:
1.  **Load GAN Model**: Loads the pre-trained GAN generator.
2.  **Load Prediction Model**: Loads the pre-trained CNN classifier.
3.  **Generate GAN Image & Predict Severity**: Generates a batch of synthetic images and classifies each one, displaying the image with its predicted DR severity.

## File Descriptions

-   `main.py`: The main entry point of the application. It runs the Tkinter GUI.
-   `TrainModel.py`: Handles the loading of the dataset and the training of the CNN classifier. It saves the model as `train.h5` and `train.json`.
-   `GANModel.py`: Defines the DCGAN architecture (generator and discriminator) and handles the training process. It saves generator models periodically during training.
-   `GeneratePredict.py`: A script used for development and testing. It loads a GAN model, generates images, and uses the classification model to predict their severity.
-   `retina.py`: Its purpose is not immediately clear from the context, might be a helper script or part of an older version.
-   `dataset/`: This directory should contain the image dataset, with subdirectories named `0`, `1`, `2`, `3`, `4` corresponding to the DR severity classes.
-   `model/`: This directory stores the pre-trained model files. `generator_model_080.h5` is used by default in the application. `train.h5` and `train.json` contain the classification model. 
