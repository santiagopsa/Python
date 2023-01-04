from cv2 import cv2
import face_recognition as fr
import time


face_control=False
def picture_taker():
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    faces=True
    # Read camera image
    success, unfiltered_image = capture.read()

    if not success:
        print('Not able to capture')
    else:

        # Convert photo to RGB
        image = cv2.cvtColor(unfiltered_image, cv2.COLOR_BGR2RGB)


        try:
            face_location = fr.face_locations(image)
            decodified_face = fr.face_encodings(image)[0]

        except:
            print('No hay una Cara, por favor vuelve a intentarlo')
            picture_show(unfiltered_image)
            faces=False
            multiple_faces=False
            decodified_face=0
            return unfiltered_image,decodified_face,multiple_faces, faces

       #see if there is more than one face
        if len(face_location)>1:
            multiple_faces=True
        else:
            multiple_faces=False



        for face in face_location:
            cv2.rectangle(unfiltered_image,
                          (face[3], face[0]),
                          (face[1], face[2]),
                          (0, 255, 0),
                          2)


        return unfiltered_image,decodified_face,multiple_faces,faces

def picture_show(imagen_mostrar):
    cv2.imshow('Foto Id', imagen_mostrar)

    # Keep image
    cv2.waitKey(3000)

def instructions():
    print('*' * 20 + '\n')
    print('Bienvenido a la prueba de Arquitecto de software')
    print('Esta prueba tiene unos requisitos altos de seguiridad, por lo tanto requerimos autorización a tu webcam\n')
    print('*' * 20 + '\n')
    print('Aquí las reglas para presentar la prueba:\n')
    print('1. Debes autorizar el uso de tu webcam antes de iniciar')
    print('2. Asegurate de contar con suficiente iluminación para poder reconocerte durante toda la prueba')
    print('3. Esta prueba no se debe presentar en un dispositivo móvil')
    print('4. Solo puede haber una persona presentando la prueba')
    print('5. No puedes abrir otras ventanas o usar material de apoyo externo')
    print('*' * 100 + '\n')
    agree=input('¿Estás de acuerdo con estas condiciones? S/N:')
    if agree.lower() != 's':
        print('Prueba terminada')
        exit()


#Instructions for the test
instructions()

# Take control picture of student
while face_control == False:
    print('Tomando imagen de control........')
    print('*' * 20 + '\n')
    image_control,decodified_control_face,multi_face,face_control=picture_taker()
    print('Presentando imagen de control')
    print('*' * 20 + '\n')
    picture_show(image_control)

# Start time for test
start_timer=time.time()

#reference point for next time
end_timer=time.time()
time_difference=end_timer-start_timer

print('Inicialdo el test, se tomaran imagenes cada 10 segundos y se compararán con la imagen de control')
print('*' * 20 + '\n')
print('*' * 20 + '\n')
contador_tomas=1
# set a time for the test
while time_difference<60:
    end_timer = time.time()
    # See elapsed time
    time_difference = round(end_timer - start_timer,0)
    # Take pictures after 10,20 and 25 seconds
    if time_difference == 10 or time_difference == 20 or time_difference == 30 or time_difference == 40 or time_difference == 50:
        print('\n' + ('*' * 20))
        print(f'Toma #{str(contador_tomas)}')
        print(('*' * 20))
        new_pic,new_dec,new_multi_face,nueva_cara= picture_taker()
        contador_tomas += 1


        #See if there are multiple faces
        if new_multi_face ==True:
            print('Hay mas de una persona, solo puede haber una persona en la prueba')

        # face comparison
        if nueva_cara == True:
            caras_iguales = fr.compare_faces([decodified_control_face], new_dec,0.6)
            print(caras_iguales)
            distance = round(float(fr.face_distance([decodified_control_face], new_dec)), 2)
            print(distance)
            picture_show(new_pic)
            if caras_iguales == [True]:
                print('La cara control y la nueva cara SI SON iguales')
            else:
                print('La cara control y la nueva cara NO SON iguales')
        else:
            print('No se ve una cara en la imagen')



