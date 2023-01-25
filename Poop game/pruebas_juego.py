import pygame
from random import randint
from pygame import mixer

game_over=False
salida=False
iniciado=True
cuentagotas = 0
#Inicializa el juego
pygame.init()

#Define la pantalla y la resulucion
pantalla = pygame.display.set_mode((800,600))

#Se pone el titulo de la ventana
pygame.display.set_caption('Invacion Espacial')

#Se pone el icono de la ventana
icono = pygame.image.load('space-gun.png')
pygame.display.set_icon(icono)

#Definicion de la imagen del jugador
img_protagonista = pygame.image.load('poop.png')
muevoj_x=20
muevoj_y=520

#Definicion del puntaje
puntaje=0
fuente= pygame.font.Font('freesansbold.ttf',32)
texto_x=10
texto_y=10

#cargando musica
mixer.music.load('mario.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)


#funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f'Corazones ganados: {puntaje}', True, (255,255,255))
    pantalla.blit(texto,(x,y))


#Definicion de la imagen del enemigo


#Definicion listas variables de Enemigo
img_enemigo=[]
muevoe_x=[]
muevoe_y=[]
e_x_incremeto=[]
e_y_incremento=[]
numero_enemigos=8

#Definicion variables de Enemigo
correr_x=0
for e in range(numero_enemigos):
    img_enemigo.append(pygame.image.load('enemy.png'))
    muevoe_x.append(42+correr_x)
    muevoe_y.append(42)
    e_x_incremeto.append(0.1)
    e_y_incremento.append(60)
    correr_x += 90

#Definicion de la imagen de la bala
img_bala = pygame.image.load('bala.png')
muevob_x=0
muevob_y=520
b_x_incremeto=0
b_y_incremento=0.5
bala_visible=False

#Funcion del jugador
def jugador(x,y):
    pantalla.blit(img_protagonista,(x,y))

#Funcion del enemigo
def enemigo(x,y,nu):
    pantalla.blit(img_enemigo[nu], (x, y))

def bala(x,y):
    global bala_visible
    bala_visible=True
    pantalla.blit(img_bala, (x+16, y+10))

def detectar_colision(x1,x2,y1,y2):
    distancia = ((x2-x1)**2 + (y2-y1)**2)**0.5
    if 30 >= distancia:
        sonido_bala = mixer.Sound('muerto.mp3')
        sonido_bala.play()
        sonido_bala.set_volume(0.2)
        return True
    else:
        return False

while True:
    pantalla.fill((0, 73, 112))
    # movimiento del enemigo va automatico
    jugador(muevoj_x, muevoj_y)
    mostrar_puntaje(texto_x, texto_y)
    for n in range(numero_enemigos):
        enemigo(muevoe_x[n], muevoe_y[n],n)
        muevoe_x[n] += e_x_incremeto[n]
        impacto_bala = detectar_colision(muevob_x, muevoe_x[n], muevob_y, muevoe_y[n])
        # Restriccion movimiento enemigo
        if muevoe_x[n] <= 20:
            e_x_incremeto[n] = 0.1
            muevoe_y[n] += e_y_incremento[n]
        elif muevoe_x[n] >= 730:
            e_x_incremeto[n] = -0.1
            muevoe_y[n] += e_y_incremento[n]
        if impacto_bala:
            bala_visible=False
            muevob_y=500
            puntaje += 100
            muevoe_x[n] = randint(0,700)
            muevoe_y[n] = randint(50,300)

        if muevoe_y[n] > 500:
            print(muevoe_y)
            for k in range(numero_enemigos):
                muevoe_y[k]=-10000
                muevoj_y=10000
            game_over=True
            break

    for evento in pygame.event.get():
        #movimiento del jugador va con el mouse
        muevoj_x=pygame.mouse.get_pos()[0]
        if evento.type == pygame.MOUSEBUTTONUP:
            sonido_bala=mixer.Sound('disparo.mp3')
            sonido_bala.play()
            sonido_bala.set_volume(0.2)
            if bala_visible==False:
                muevob_x = pygame.mouse.get_pos()[0]
                bala(muevob_x,muevob_y)
        if evento.type == pygame.QUIT:
            pygame.quit()

        #Restriccion movimiento jugador
        if muevoj_x <= 20:
            muevoj_x=20
        elif muevoj_x >= 730:
            muevoj_x=730

    #Si game Over

    if game_over:
        bala_visible = False
        texto = fuente.render(f'Juego terminado', True, (255, 255, 255))
        pantalla.blit(texto, (30, 250))
        mixer.music.fadeout(1000)
        if cuentagotas==0:
            print(cuentagotas)
            game = mixer.Sound('gameover.mp3')
            game.set_volume(0.1)
            game.play()
            cuentagotas += 1

    if muevob_y <=0:
        muevob_y = 500
        bala_visible = False

    if bala_visible:
        bala(muevob_x,muevob_y)
        muevob_y -= b_y_incremento

    pygame.display.update()
