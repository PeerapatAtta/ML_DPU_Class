import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials, db
import json
import numpy as np
import requests

# ตั้งค่า Firebase Admin SDK
cred = credentials.Certificate("key/serviceAccountKey.json")  # แทนที่ path นี้ด้วย path ของไฟล์ serviceAccountKey.json
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://we674-ml-f62d5-default-rtdb.firebaseio.com/'
})

# โหลดข้อมูลจาก Firebase
person_face_encodings = []
person_face_names = []

ref = db.reference('/testpython')
result = ref.get()
for person in result:
    data = result[person]

    # โหลดภาพจากไฟล์ที่กำหนดในฐานข้อมูล
    database_image = face_recognition.load_image_file(data['Image'])
    data_base_encoding = face_recognition.face_encodings(database_image)[0]
    person_face_names.append(data['Name'])
    person_face_encodings.append(data_base_encoding)

# ตั้งค่ากล้องและการตรวจจับใบหน้า
videoCapture = cv2.VideoCapture(0)
data_locations = []
data_encodings = []
data_names = []
frameProcess = True

while True:
    ret, frame = videoCapture.read()
    resizing = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_resizing = np.ascontiguousarray(resizing[:, :, ::-1])
    if frameProcess:
        data_locations = face_recognition.face_locations(rgb_resizing)
        data_encodings = face_recognition.face_encodings(rgb_resizing, data_locations)
        data_names = []
        for dc in data_encodings:
            matches = face_recognition.compare_faces(person_face_encodings, dc)
            name = "UNKNOWN"
            if True in matches:
                first_match_index = matches.index(True)
                name = person_face_names[first_match_index]
            data_names.append(name)
    frameProcess = not frameProcess
    for (top, right, bottom, left), name in zip(data_locations, data_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (26, 174, 10), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (26, 174, 10), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    cv2.imshow('Video', frame)
    
    if cv2.waitKey(25) == 13:
        break

videoCapture.release()
cv2.destroyAllWindows()
