import cv2
import face_recognition

video_path = 'videos/WIN_20220925_13_54_04_Pro.mp4'
cap = cv2.VideoCapture(video_path)
face_locations = []

while True:
    ret, frame = cap.read()
    if not ret:
        print(f"Error: ไม่สามารถอ่านเฟรมจากวิดีโอ {video_path}")
        break

    rgb_frame = frame[:, :, ::-1]
    face_locations = face_recognition.face_locations(rgb_frame)
    for top, right, bottom, left in face_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 4)

    frame = cv2.resize(frame, (600, 340))      
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()