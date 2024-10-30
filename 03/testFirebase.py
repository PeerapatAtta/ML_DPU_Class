# from firebase import firebase

# firebase = firebase.FirebaseApplication('https://we674-ml-f62d5-default-rtdb.firebaseio.com/', None)
# data =  { 'Name': 'Peerapat',
#           'Surname': 'Atta',
#           'Gender': 'Male',
#           'Image' : 'images/off.jpg'
#           }
# result = firebase.post('/check-in',data)
# print(result)

import firebase_admin
from firebase_admin import credentials, db

# ตั้งค่า Credential เพื่อเชื่อมต่อ Firebase
cred = credentials.Certificate("key/serviceAccountKey.json")  # ใส่ path ของไฟล์ serviceAccountKey.json
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://we674-ml-f62d5-default-rtdb.firebaseio.com/'  # URL ของ Firebase Database
})

# ข้อมูลที่ต้องการส่งไปยัง Firebase
data = {
    'Name': 'Peerapat',
    'Surname': 'Atta',
    'Gender': 'Male',
    'Image': 'images/off.jpg'
}

# ส่งข้อมูลไปยัง Firebase Realtime Database
ref = db.reference('/check-in')
result = ref.push(data)
print("Data pushed to Firebase:", result.key)