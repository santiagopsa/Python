from random import choice

# Definimos una lista de palabras para jugar
lista_palabras=['arbol','aguacate','computador','arracacha','marinero','camara','estadio','francia','colombia']
oportunidades=6

# funcion para elegir aleatoriamente una palabra de la lista
def palabra_aleatoria(lista_opciones):
    return choice(lista_opciones)

def indices_palabra(letra_usuario,palabra_rand):
    conteo_indice=0
    lista_indices=[]
    for letra in palabra_rand:
        if letra == letra_usuario:
            lista_indices.append(conteo_indice)
        conteo_indice += 1
    return lista_indices


# Elegimos una palabra para iniciar el juego
palabra_elegida = palabra_aleatoria(lista_palabras)
palabra_lista = list(palabra_elegida)
pista_lista=['-']*len(palabra_elegida)
pista = ''.join(pista_lista)

print(f'Bienvenido a Ahorado, estoy pensando una palabra, tienes {str(oportunidades)} oportunidades de adivinar')
print('\nTe deseo suerte, vamos a empezar')
print(pista)
while(oportunidades>0):
    letra_elegida=input('Ingresa una letra: ')
    if indices_palabra(letra_elegida,palabra_elegida) == []:
        oportunidades -= 1
        print(f'tienes {oportunidades} oportunidades')
    for indice in indices_palabra(letra_elegida,palabra_elegida):
        pista_lista[indice]=str(letra_elegida)
    print(''.join(pista_lista))
    if palabra_lista==pista_lista:
        print('Felicitacionces, has ganado')
        break


