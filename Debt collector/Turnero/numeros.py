def generador_turnos():
    x=0
    while True:
        x += 1
        yield x

def deco_turno(funcion):
    def decoracion(turno,categoria):
        print('Su turno es')
        funcion(turno,categoria)
        print('Gracias por aguardar')
    return decoracion


def turno_categoria(turno,categoria):
    print(f'{categoria}-{turno}')