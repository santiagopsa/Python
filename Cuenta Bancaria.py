from random import randint

class Persona:
    def __init__(self, nombre, apellido):
        self.nombre=nombre
        self.apellido=apellido

class Cliente(Persona):
    def __init__(self, nombre, apellido, numero_cuenta, balance):
        super().__init__(nombre,apellido)
        self.numero_cuenta=numero_cuenta
        self.balance=balance
    def imprimir(self):
        print(f'Hola {self.nombre} {self.apellido} identificad@ con numero de cuenta {self.numero_cuenta}, tu saldo es {self.balance}')
    def depositar(self,valor_deposito):
        self.balance=valor_deposito+self.balance
        print(f'el valor depositado es {valor_deposito} y tu balance es {self.balance}')
    def retirar(self,valor_retiro):
        self.balance=self.balance-valor_retiro
        print(f'el valor retirado es {valor_retiro} y tu balance es {self.balance}')

def crear_cliente():
    nombre = input('Ingresa el nombre del cliente: ')
    apellido = input('Ingresa el apellido del cliente: ')
    numero_cuenta = randint(10956366,20956366)
    balance_inicial = int(input('ingresa el balance inicial: '))
    return Cliente(nombre,apellido,numero_cuenta,balance_inicial)

def inicio():
    cliente_1=crear_cliente()
    cliente_1.imprimir()
    codigo=True
    contador=1
    for opcion in ['Depositar','Retirar','Salir']:
        print(f'[{contador}] - {opcion}')
        contador += 1
    while codigo:
        seleccion = int(input('Ingresa una de las opciones de arriba: '))
        if seleccion == 1:
            deposito = int(input('ingresa el valor a depositar: '))
            cliente_1.depositar(deposito)
        elif seleccion == 2:
            balance_actual = cliente_1.balance
            retiro = int(input('ingresa el valor a retirar: '))
            if balance_actual < retiro:
                print('No tienes saldo suficiente')
            else:
                cliente_1.retirar(retiro)
        elif seleccion == 3:
            break
        else:
            print('has ingresado una opción invalida')

inicio()


