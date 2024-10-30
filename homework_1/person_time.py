import cv2
import face_recognition
import firebase_admin
from firebase_admin import credentials, db
import datetime
import numpy as np

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

# ตัวแปรเพื่อติดตามสถานะ Check-in/Check-out
check_status = {name: None for name in person_face_names}
last_seen = {name: None for name in person_face_names}
absent_time = 5  # กำหนดระยะเวลา (วินาที) ที่ต้องไม่พบใบหน้าในเฟรมเพื่อสลับสถานะใหม่

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
        current_time = datetime.datetime.now()

        for dc in data_encodings:
            matches = face_recognition.compare_faces(person_face_encodings, dc)
            name = "UNKNOWN"
            if True in matches:
                first_match_index = matches.index(True)
                name = person_face_names[first_match_index]

                # เงื่อนไขที่ 1: Check-in หากไม่มีสถานะเดิม
                if check_status[name] is None:
                    check_in_out_ref = db.reference(f'/check_in_out/{name}')
                    check_in_out_ref.push({
                        'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'Check-in'
                    })
                    print(f"{name} has checked in at {current_time}")
                    check_status[name] = 'Check-in'
                
                # เงื่อนไขที่ 2: สลับสถานะหากไม่พบใบหน้าอย่างน้อย 5 วินาทีและพบอีกครั้ง
                elif last_seen[name] is not None:
                    time_diff = (current_time - last_seen[name]).total_seconds()
                    if time_diff >= absent_time:
                        # สลับสถานะ
                        new_status = 'Check-out' if check_status[name] == 'Check-in' else 'Check-in'
                        check_in_out_ref = db.reference(f'/check_in_out/{name}')
                        check_in_out_ref.push({
                            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                            'status': new_status
                        })
                        print(f"{name} has {new_status.lower()}ed at {current_time}")
                        check_status[name] = new_status  # อัปเดตสถานะใหม่หลังสลับสถานะ

                # บันทึกเวลาล่าสุดที่พบใบหน้า
                last_seen[name] = current_time

            data_names.append(name)

    frameProcess = not frameProcess

    # แสดงผลในหน้าจอ
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
