import cv2
import os
import numpy as np
import pandas as pd
from datetime import datetime


def load_training_data():

    data_dir = "database"

    faces = []
    labels = []
    for i in os.listdir(data_dir):
        img_path = os.path.join(data_dir, i)
        image = cv2.imread(img_path)
        # faces.append(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces.append(gray)
        label = int(i.split('.')[0])
        labels.append(label)
    return faces, np.array(labels)


def train_model(faces, labels):

    recognizer = cv2.face.LBPHFaceRecognizer.create()
    recognizer.train(faces, labels)
    recognizer.write('lbph_face_model.yml')
    return recognizer


def predict(recognizer, face):

    id_, conf = recognizer.predict(face)
    if conf > 90:
        return id_


def get_name(id_):

    data = pd.read_csv("records.csv")
    all_words = data.to_dict(orient='records')
    # print(all_words)
    name = None
    for i in all_words:
        if i['rollno'] == id_:
            print(i['rollno'])
            name = i['name']
            # print(name)
            now = datetime.now()

            current_time = now.strftime("%H:%M")
            # if data.loc[data['rollno'] == id_, 'present'] == 'P':
            data.loc[data['rollno'] == id_, 'present'] = 'P'
            data.loc[data['rollno'] == id_, 'time'] = current_time
            data.to_csv("records.csv", index=False)


    # print(all_words)
    print(name)

    return name
