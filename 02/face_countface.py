import face_recognition

image = face_recognition.load_image_file("images/a.jpg")
face_location = face_recognition.face_locations(image)

print(face_location)
print(f"numbers of face: {len(face_location)}")