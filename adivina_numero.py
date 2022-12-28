from random import randint

print('Hola, este juego te permitira adivinar un numero del 1 al 100\n\n')
nombre=input('Para empezar escribe tu nombre: ')

print(f'un gusto {nombre}, he pensado un numero del 1 al 100, Cual crees que es?')
numero_aleatorio = randint(1,100)
acierto = False
for intento in range(1,8):
    valor_intento = int(input('Cual cree que es el numero que pense: '))
    if valor_intento < 1 or valor_intento > 100:
        print('El numero no esta permitido')
    elif valor_intento < numero_aleatorio:
        print('El numero que elegiste es menor al que pense')
    elif valor_intento > numero_aleatorio:
        print('El numero que elegiste es mayor al que pense')
    else:
        print('Felicitaciones!, acertaste, el numero es '+str(valor_intento))
        print(f'acertaste despues de {intento} intentos')
        acierto = True
        break

if not acierto:
    print('Lo siento, no encontraste el numero, vuelve a intentarlo mas tarde')