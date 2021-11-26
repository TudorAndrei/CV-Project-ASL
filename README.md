# ASL Project

## Description

ASL project is an educational software, intended for individuals learning American Sign Language, that will allow them to master the basic spelling and will facilitate the communication, as well as the integration, of deaf people.

## Idea

Learning ASL allows you to communicate with a wide range of hearing, hard of hearing, and deaf human beings—including those from hospitals, schools/colleges, courts, governmental agencies, community activities, and local, county, state legislatures.

## The goal

The main goal of the ASL project is to improve the quality of communication for hearing people with deaf or hard of hearing individuals, by helping learners to practice and to develop fluency in Sign Language.

## Architecture

![alt text](static/images/system_design.png?raw=true)

## Install the required packages

### Conda version (Highly Recommended)
```bash
conda env create -f environment.yml
```
### Pip version
```
pip install -f requirement.txt

```

##  Download the repositories and launch the web application

Make sure the yolo repository is cloned,  otherwise the model cannot be configured.

```
git clone https://github.com/TudorAndrei/CV-Project-ASL.git
cd CV-Project-ASL
git clone https://github.com/TudorAndrei/yolov5 yolo
FLASK_APP=app.py flask run
```

## Bibliography
![Yolov5 Implementation](https://github.com/ultralytics/yolov5)
![Object Detection Dataset Augmentation](https://github.com/insigh1/Interactive_ABCs_with_American_Sign_Language_using_Yolov5/blob/master/01_image_processing_and_data_augmentation.ipynb)
![ASL Alphabet Dataset](https://public.roboflow.com/object-detection/american-sign-language-letters/1)
![Camera App with Flask and OpenCV](https://towardsdatascience.com/camera-app-with-flask-and-opencv-bd147f6c0eec)

