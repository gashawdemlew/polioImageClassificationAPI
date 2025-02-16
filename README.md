# Polio-Virus Prediction Model

## Description

This repository provides the codebase to test a deployed model for **polio-virus prediction** (Polio vs Non-Polio). The model is trained using **image processing** and **computer vision technologies**, specifically image classification approaches. The dataset includes MRI images collected from various hospitals in Ethiopia.

---

## Process of Model Development

The model was developed using the following steps:

1. **Image Collection and Preprocessing**:
   - MRI images were collected from hospitals.
   - Preprocessing steps included cleaning, resizing, and normalizing the images for training.

2. **Image Labeling and Augmentation**:
   - Images were labeled as either **Polio** or **Non-Polio**.
   - Data augmentation techniques were applied to improve dataset variability, including:
     - Resizing
     - Rotation
     - Adjusting contrast and brightness
     - Other transformations.

3. **Model Training**:
   - The model was trained using state-of-the-art image classification pre-trained models, including:
     - **Vision Transformers (ViT)**
     - **ResNet** (Residual Networks)
     - **MobileNet**
     - **VGG16** and **VGG19**

4. **Testing and Evaluation**:
   - The model achieved an **F-score of 93%**, showing strong performance in distinguishing Polio from Non-Polio cases.

5. **Model Deployment**:
   - The trained model was deployed on:
     - **On-premise servers**
     - **Cloud platforms** (paid or free options like Hugging Face).

---

## How to Use This Repository

Follow the steps below to use this repository to test the deployed model:

### 1. Clone the Repository

Clone the repository to your local machine using the following command:

```bash
git clone https://github.com/gashawdemlew/polioImageClassificationAPI.git
cd polioImageClassificationAPI
```

---

### 2. Install Required Python Packages

Ensure you have Python installed. Then, install the necessary dependencies from the requirements.txt file:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Run the app.py file on your local machine:
```bash
python main.py
```



## Deployment
The deployed model is available on Hugging Face. You can directly test the model online or integrate it into your application.

### Deployed Model Link: Hugging Face Model [Link](https://huggingface.co/spaces/gashudemman/polioImageClassification)
If you prefer to deploy the model yourself, you can use the following platforms:

1. On-Premise Server: Use Docker or other tools to host the model locally.
2. Cloud Platforms:
    - Paid platforms like AWS, GCP (Google Cloud), or Azure.
    - Free platforms like Hugging Face Spaces.

---

## Features
- Polio-Virus Detection:
        - Classifies MRI images into Polio or Non-Polio categories.
- Image Processing:
        - Preprocesses and augments MRI images for improved accuracy.
- Image Classification:
        - Leverages pre-trained models like Vision Transformers (ViT), ResNet, MobileNet, VGG16, and VGG19.
- Cloud Integration:
        - Model is deployable on cloud platforms for easy accessibility.
    
---

## Technologies Used
- Python: The primary programming language.
- Computer Vision: Techniques for image processing and object detection.
Image Classification Models:
    - Vision Transformers (ViT)
    - ResNet (Residual Networks)
    - MobileNet
    - VGG16 and VGG19
- Annotation Tools:
        - Roboflow
        - Labelme
- Deployment: Hugging Face, on-premise servers, or cloud platforms.

---

## License
This project is licensed under the MIT License.


---

## Contact
For questions or support, feel free to reach out:

    - Email: gashudemman@gmail.com
    - LinkedIn: https://www.linkedin.com/in/gashaw-demlew-b35865150/