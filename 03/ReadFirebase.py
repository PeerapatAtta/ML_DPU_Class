# import json
# import requests
# import numpy as np

# from firebase import firebase

# firebase = firebase.FirebaseApplication('https://we674-ml-f62d5-default-rtdb.firebaseio.com/', None)
# result = firebase.get('/testpython/', '')
# for person in result:
#     jsn = requests.get('https://we674-ml-f62d5-default-rtdb.firebaseio.com/testpython.json')
#     data = jsn.json()
#     print(data[person]['Name'])
#     print(data[person]['Surname'])
#     print(data[person]['Gender'])
#     print(data[person]['Image'])

import firebase_admin
from firebase_admin import credentials, db

# ตั้งค่า Firebase Admin SDK
cred = credentials.Certificate("key/serviceAccountKey.json")  # แทนที่ path นี้ด้วย path ของไฟล์ serviceAccountKey.json
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://we674-ml-f62d5-default-rtdb.firebaseio.com/'  # ใส่ URL ของ Firebase Database ของคุณ
})

# ดึงข้อมูลจาก Firebase Realtime Database
ref = db.reference('/testpython')
result = ref.get()

# แสดงผลข้อมูล
for person in result:
    print("Name:", result[person].get('Name'))
    print("Surname:", result[person].get('Surname'))
    print("Gender:", result[person].get('Gender'))
    print("Image:", result[person].get('Image'))
    print("-" * 30)
