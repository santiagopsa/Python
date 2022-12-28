import numeros

print('Bienvenido a la farmacia "Pasele Ud" por favor elija una de las secciones para pedir un turno')
lista_secciones=['Pefumeria','Farmacia','Cosmeticos']
terminar=0
turno1=numeros.generador_turnos()
turno2=numeros.generador_turnos()
turno3=numeros.generador_turnos()

while terminar !='t':
    contador=0
    for eleccion in lista_secciones:
        print(f'[{contador+1}] - para {eleccion}')
        contador += 1
    seleccion=int(input('Por favor increse la seccion para la cual necesita el turno: '))
    if seleccion == 1:
        turnos_decorados=numeros.deco_turno(numeros.turno_categoria)
        turnos_decorados(next(turno1),'P')
    elif seleccion == 2:
        turnos_decorados=numeros.deco_turno(numeros.turno_categoria)
        turnos_decorados(next(turno2),'F')
    elif seleccion == 3:
        turnos_decorados=numeros.deco_turno(numeros.turno_categoria)
        turnos_decorados(next(turno3),'C')
    else:
        print('Opcion invalida')
    terminar=input('Operacion terminada, presione cualquier tecla para pedir otro turno o "t" para terminar: ')
