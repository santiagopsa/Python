from cv2 import cv2
import face_recognition as fr

#load images
foto_control1 = fr.load_image_file('caro1.jpeg')
foto_control2 = fr.load_image_file('santi.jpeg')

# convert to RGB
foto_control1 = cv2.cvtColor(foto_control1,cv2.COLOR_BGR2RGB)
foto_control2 = cv2.cvtColor(foto_control2,cv2.COLOR_BGR2RGB)

# find control face
lugar_cara_A = fr.face_locations(foto_control1)[0]
decodified_faceA = fr.face_encodings(foto_control1)[0]

lugar_cara_B = fr.face_locations(foto_control2)[0]
decodified_faceB = fr.face_encodings(foto_control2)[0]

# show rectangle on face
cv2.rectangle(foto_control1,
              (lugar_cara_A[3],lugar_cara_A[0]),
              (lugar_cara_A[1],lugar_cara_A[2]),
               (0,255,0),
               2)

cv2.rectangle(foto_control2,
              (lugar_cara_B[3],lugar_cara_B[0]),
              (lugar_cara_B[1],lugar_cara_B[2]),
               (0,255,0),
               2)

# face comparison
caras_iguales= fr.compare_faces([decodified_faceA],decodified_faceB)
if caras_iguales == True:
    caras= 'son iguales'
else:
    caras= 'no son iguales'

# difference distance
distance= round(float(fr.face_distance([decodified_faceA],decodified_faceB)),2)
print(distance)

#print distance in square
cv2.putText(foto_control1,f'La distancia es {str(distance)} y las caras {caras}',
            (lugar_cara_B[3],lugar_cara_B[0]),
            cv2.FONT_HERSHEY_TRIPLEX,
            0.5,
            (0,0,255))

# Show images
cv2.imshow('Foto Caro',foto_control1)
cv2.imshow('Foto Santi',foto_control2)

# take image from webcam
capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Read camera image
success, image=capture.read()

if not success:
    print('Not able to capture')
else:
    #Recognize captured face
    face_captured= fr.face_locations(image)

    # codify captured face
    face_captured_codified = fr.face_encodings(image,face_captured)

    



# Keep images
cv2.waitKey()