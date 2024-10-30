import face_recognition
from PIL import Image

image = face_recognition.load_image_file("images/a.jpg")
face_location = face_recognition.face_locations(image)

print(face_location)
print(f"numbers of face: {len(face_location)}")

for f in face_location: 
    top, right, bottom, left = f

    face_img = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_img)
    pil_image.show()