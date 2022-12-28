from pathlib import Path
import os

def cantidad_recetas(path_inicial):
    contador_recetas=0
    for archivo_txt in path_inicial.glob('**/*.txt'):
        contador_recetas += 1
    return contador_recetas

def mostrar_opciones():
    opcion_elegida=0
    print('[1] - leer receta')
    print('[2] - crear receta')
    print('[3] - crear categoria')
    print('[4] - eliminar receta')
    print('[5] - eliminar categoria')
    print('[6] - finalizar programa')
    opcion_elegida = input('Elije una de las 6 opciones: ')
    while opcion_elegida not in ('123456'):
        opcion_elegida = input('Solo puedes elegir  numeros del 1 al 6: ')
    return opcion_elegida

def elige_categoria():
    os.chdir(directorio_recetas)
    count=1
    lista_categoria=[]
    for categoria in os.listdir():
        print(f'Categoria [{count}] - {categoria}')
        lista_categoria.append(categoria)
        count +=1
    categoria_elegida = input('Elige una de las categorias: ')
    lista_conteo=list(range(1, count))
    string_conteo=''.join(map(str,lista_conteo))
    while categoria_elegida not in string_conteo:
        categoria_elegida = input('Solo puedes elegir el numero de las categorias disponibles arriba: ')
    return str(lista_categoria[int(categoria_elegida)-1])

def elige_receta(categoria_receta):
    os.chdir(directorio_recetas / categoria_receta)
    count=1
    lista_recetas=[]
    for receta in os.listdir():
        print(f'receta [{count}] - {receta}')
        lista_recetas.append(receta)
        count +=1
    if lista_recetas==[]:
        input('No hay recetas, cualquier tecla para continuar')
        return 0
    else:
        receta_elegida = input('Elige una de las recetas: ')
        lista_conteo=list(range(1, count))
        string_conteo=''.join(map(str,lista_conteo))
        while receta_elegida not in string_conteo:
            receta_elegida = input('Solo puedes elegir el numero de las categorias disponibles arriba: ')
        return str(lista_recetas[int(receta_elegida)-1])

def crea_receta(categoria_receta):
    os.chdir(directorio_recetas / categoria_receta)
    nombre_nueva_receta=input('Ingresa el nombre de la nueva receta: ')
    texto_receta=input('Ingresa la receta nueva: ')
    archivo_receta=open(nombre_nueva_receta+'.txt','w')
    archivo_receta.write(texto_receta)
    archivo_receta.close()
    print('Receta creada con exito')

def leer_receta(categoria_receta,receta_leer):
    os.chdir(directorio_recetas / categoria_receta)
    archivo=open(receta_leer)
    print(archivo.read())

def crea_categoria():
    categoria_nueva = input('Ingresa el nombre de la nueva categoria: ')
    Path.mkdir(directorio_recetas / categoria_nueva)
    input('Categoria creada exitosamente, pulsa cualquier tecla para continuar')

def elimina_receta(categoria,receta):
    Path.unlink(directorio_recetas / categoria / receta)
    input('Has eliminado la receta exitosamente!, cualquier tecla para continuar')

def elimina_categoria(categoria):
    Path.rmdir(directorio_recetas /categoria)
    input('Categoria eliminada exitosamente, pulsa cualquier tecla para continuar')


opcion=0
directorio_recetas = Path(Path.home(),'Recetas')
print("Bienvenido al administrador de recetas")

print("********************************************")

print("Las recetas estan en "+str(directorio_recetas))

print(f'En total hay {cantidad_recetas(directorio_recetas)} recetas')
print("********************************************")

opcion = int(mostrar_opciones())
while opcion!=6:
    if opcion == 1:
        print('Has elegido leer receta, ahora elige una categoria')
        categoria_elegida=elige_categoria()
        print('has elegido la categoria: '+categoria_elegida)
        receta_elegida=elige_receta(categoria_elegida)
        if receta_elegida != 0:
            print('has elegido la receta: ' + receta_elegida)
            leer_receta(categoria_elegida, receta_elegida)
            input('Ingresa cualquier tecla para volver al menu principal')
        opcion = int(mostrar_opciones())
    elif opcion == 2:
        print('Has elegido crear receta')
        categoria_elegida=elige_categoria()
        print('has elegido la categoria: '+categoria_elegida)
        crea_receta(categoria_elegida)
        input('Ingresa cualquier tecla para volver al menu principal')
        opcion = int(mostrar_opciones())
    elif opcion == 3:
        print('Has elegido crear categoria')
        crea_categoria()
        opcion = int(mostrar_opciones())
    elif opcion == 4:
        print('Has elegido eliminar receta')
        categoria_elegida=elige_categoria()
        print('has elegido la categoria: '+categoria_elegida)
        receta_elegida=elige_receta(categoria_elegida)
        if receta_elegida != 0:
            print('has elegido la receta: ' + receta_elegida)
            elimina_receta(categoria_elegida, receta_elegida)
        opcion = int(mostrar_opciones())
    elif opcion == 5:
        print('Has elegido eliminar categoria')
        categoria_elegida = elige_categoria()
        print('has elegido eliminar la categoria: '+categoria_elegida)
        elimina_categoria(categoria_elegida)
        opcion = int(mostrar_opciones())

print('Has elegido finalizar programa')