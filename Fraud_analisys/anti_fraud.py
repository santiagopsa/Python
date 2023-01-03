from cv2 import cv2
import face_recognition as fr
import time

def picture_taker():
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Read camera image
    success, image = capture.read()
    if not success:
        print('Not able to capture')
    else:

        # Convert photo to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


        try:
            face_location = fr.face_locations(image)[0]
            print(fr.face_locations(image))

        except:
            print('No hay una Cara, por favor vuelve a intentarlo')
            exit()

       #see if there is more than one face
        if len(fr.face_locations(image))>1:
            multiple_faces=True
        else:
            multiple_faces=False

        decodified_face = fr.face_encodings(image)[0]

        return image,face_location,decodified_face,multiple_faces



# Take control picture of student
image_control,location_control,decodified_control_face,multi_face=picture_taker()
cv2.rectangle(image_control,
              (location_control[3], location_control[0]),
              (location_control[1], location_control[2]),
              (0, 255, 0),
              2)

cv2.imshow('Foto Control', image_control)

# Keep image
cv2.waitKey(3000)

# Start time for test
start_timer=time.time()

#reference point for next time
end_timer=time.time()
time_difference=end_timer-start_timer


# set a time for the test
while time_difference<30:
    end_timer = time.time()
    # See elapsed time
    time_difference = round(end_timer - start_timer,0)
    # Take pictures after 10,20 and 25 seconds
    if time_difference == 10 or time_difference == 20 or time_difference == 25:
        new_pic,new_loc,new_dec,new_multi_face= picture_taker()
        #See if there are multiple faces
        while new_multi_face ==True:
            print('Hay mas de una persona, solo puede haber una persona en la prueba')
            new_pic, new_loc, new_dec, new_multi_face = picture_taker()

        cv2.imshow('Foto en prueba', new_pic)
        cv2.waitKey(3000)

        # face comparison
        caras_iguales = fr.compare_faces([decodified_control_face], new_dec,0.6)
        print(caras_iguales)
        distance = round(float(fr.face_distance([decodified_control_face], new_dec)), 2)
        print(distance)

        if caras_iguales == [True]:
           print('son iguales')
        else:
            print('no son iguales')







# difference distance
'''distance = round(float(fr.face_distance([decodified_faceA], decodified_faceB)), 2)
print(distance)'''

# print distance in square
'''cv2.putText(foto_control1, f'La distancia es {str(distance)} y las caras {caras}',
            (lugar_cara_B[3], lugar_cara_B[0]),
            cv2.FONT_HERSHEY_TRIPLEX,
            0.5,
            (0, 0, 255))'''

# Show images
'''
cv2.imshow('Foto Santi', foto_control2)


'''
