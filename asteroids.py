import pygame, sys, os, random, math
from pygame.locals import *

pygame.init()
fps=pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#GLOABLAS
WIDTH = 800
HEIGHT = 600
time = 0

#declaracion de canvas
window = pygame.display.set_mode((WIDTH, HEIGHT),0,32)
pygame.display.set_caption('Asteroids')

#carga de imagenes
bg = pygame.image.load(os.path.join('images','bg.jpg'))
debris = pygame.image.load(os.path.join('images','debris2_brown.png'))
nave = pygame.image.load(os.path.join('images','nave.png'))
nave_movimiento = pygame.image.load(os.path.join('images','nave_movimiento.png'))
asteroide = pygame.image.load(os.path.join('images','asteroide.png'))
disparo = pygame.image.load(os.path.join('images','disparo.png'))

#generar sonidos

#misil sonido
sonido_misil = pygame.mixer.Sound(os.path.join('sounds','misil.ogg'))
sonido_misil.set_volume(1)

#propulsor sonido
sonido_propulsor = pygame.mixer.Sound(os.path.join('sounds','propulsor.ogg'))
sonido_propulsor.set_volume(1)

#sonido de aceleracion
sonido_explosion = pygame.mixer.Sound(os.path.join('sounds','explosion.ogg'))
sonido_explosion.set_volume(1)

#juego
pygame.mixer.music.load(os.path.join('sounds','juego.ogg'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()

#nave
nave_x = WIDTH/2 - 50
nave_y = HEIGHT/2 - 50
angulo_nave = 0
nave_rotando = False
direccion_nave = 0
velocidad_nave = 0
nave_acelerando = False

#asteroides
asteroide_x = [] #random.randint(0, WIDTH)
asteroide_y = [] #random.randint(0, HEIGHT)
angulo_asteroide = []
velocidad_asteroide = 2
no_asteriodes = 5

#balas
bala_x = []
bala_y = []
angulo_bala = []
no_balas = 0

#estado del juego
puntuacion = 0
perdiste = False

for i in range(0,no_asteriodes):
    asteroide_x.append(random.randint(0, WIDTH))
    asteroide_y.append(random.randint(0, HEIGHT))
    angulo_asteroide.append(random.randint(0, 365))

def rotar_centro(image,angle):
    """Rotar nave manteniendo su posicion actual"""
    origin_rect = image.get_rect()
    rotar_imagen = pygame.transform.rotate(image,angle)
    rotar_rect = origin_rect.copy()
    rotar_rect.center = rotar_imagen.get_rect().center
    rotar_imagen = rotar_imagen.subsurface(rotar_rect).copy()
    return rotar_imagen


    

#funcion para crear canvas
def draw(canvas):
    global time
    global nave_acelerando
    global bala_x, bala_y
    canvas.fill(BLACK)
    canvas.blit(bg,(0,0))
    canvas.blit(debris,(time*.3,0))
    canvas.blit(debris,(time*.3-WIDTH,0))
    #canvas.blit(disparo,(bala_x,bala_y))
    time = time + 0.5
    
    #generar disparos
    for i in range(0, no_balas):
        canvas.blit(disparo, (bala_x[i], bala_y[i]))
    
    #generar asteroides
    for i in range(0,no_asteriodes):
        canvas.blit(rotar_centro(asteroide,time), (asteroide_x[i],asteroide_y[i]))
    if nave_acelerando: 
        canvas.blit(rotar_centro(nave_movimiento,angulo_nave), (nave_x,nave_y))
    else:
        canvas.blit(rotar_centro(nave,angulo_nave), (nave_x,nave_y))
        
    #mostrar puntuacion
    myfont1 = pygame.font.SysFont("momic Sans MS",40)
    label1 = myfont1.render("Puntuacion: " + str(puntuacion), 1, (255, 255, 0))
    canvas.blit(label1, (50, 20))
    
    if perdiste:
        myfont2 = pygame.font.SysFont("Comic Sans MS",80)
        label2 = myfont2.render("GAME OVER", 1, (255,255,255))
        canvas.blit(label2, (WIDTH/2 - 150, HEIGHT/2 - 40))
        
  
# (0,0)
# (width,0)
# (0, height)
# (width, height)
#funcion para direccionar

def handle_input():
    global angulo_nave, nave_rotando, direccion_nave
    global nave_x, nave_y, velocidad_nave, nave_acelerando
    global bala_x, bala_y, angulo_bala,no_balas
    global sonido_propulsor, sonido_misil
    for event in pygame.event.get():
        if event.type== QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                nave_rotando = True
                direccion_nave = 0
            elif event.key == K_RIGHT:
                nave_rotando = True
                direccion_nave = 1
            elif event.key == K_UP:
                nave_acelerando = True
                velocidad_nave = 10
                sonido_propulsor.play()
            elif event.key == K_SPACE:
                bala_x.append( nave_x + 50 )
                bala_y.append( nave_y + 50 )
                angulo_bala.append( angulo_nave )
                no_balas = no_balas +1
                sonido_misil.play()
        elif event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                nave_rotando = False
            else:
                nave_acelerando = False
                sonido_propulsor.stop()
    if nave_rotando:
        if direccion_nave == 0:
            angulo_nave = angulo_nave + 10
        elif direccion_nave == 1:
            angulo_nave = angulo_nave - 10
    if nave_acelerando or velocidad_nave > 0:
        nave_x = (nave_x + math.cos(math.radians(angulo_nave)) * velocidad_nave)
        nave_y = (nave_y + -math.sin(math.radians(angulo_nave)) * velocidad_nave)
        if nave_acelerando == False:
            velocidad_nave = velocidad_nave - 0.5
    #print(angulo_nave)

#actualizar_pantalla
def actualizar_pantalla():
    pygame.display.update()
    fps.tick(60)
    
def es_colision(enemigoX, enemigoY, proyectilX, proyectilY, dist):
    distancia = math.sqrt( math.pow(enemigoX - proyectilX, 2) + ( math.pow(enemigoY - proyectilY, 2)))
    if distancia < dist:
        return True
    else: 
        return False

#logica_del_juego
def logica_del_juego():
    
    global bala_x, bala_y, angulo_bala, no_balas
    global asteroide_x, asteroide_y
    global sonido_explosion
    global puntuacion
    global perdiste
    
    
    for i in range(0,no_balas):
        bala_x[i] = (bala_x[i] + math.cos(math.radians(angulo_bala[i])) * 10)
        bala_y[i] = (bala_y[i] + -math.sin(math.radians(angulo_bala[i])) * 10)
    
    for i in range(0,no_asteriodes):
        asteroide_x[i] = (asteroide_x[i] + math.cos(math.radians(angulo_asteroide[i])) * velocidad_asteroide) #cambiar 0 por velocidad_asteroide
        asteroide_y[i] = (asteroide_y[i] + -math.sin(math.radians(angulo_asteroide[i])) * velocidad_asteroide) #cambiar 0 por velocidad_asteroide
        #Retornar ateroides al mapa cuando estos salen del canvas
        if asteroide_y[i] < 0:
            asteroide_y[i] = HEIGHT
        if asteroide_y[i] > HEIGHT:
            asteroide_y[i] = 0
        if asteroide_x[i] < 0:
            asteroide_x[i] = WIDTH
        if asteroide_x[i] > WIDTH:
            asteroide_x[i] = 0
        
        #coliciones de asteroides con naves
        if es_colision(nave_x, nave_y,asteroide_x[i],asteroide_y[i],27):
            perdiste = True
    for i in range(0, no_balas):
        for j in range(0, no_asteriodes):
            if es_colision(bala_x[i],bala_y[i],asteroide_x[j],asteroide_y[j],50):
                asteroide_x[j] = (random.randint(0,WIDTH))
                asteroide_y[j] = (random.randint(0,HEIGHT))
                angulo_asteroide[j] = (random.randint(0,365))
                sonido_explosion.play()
                puntuacion += 1

#game loop
while True:
    draw(window)
    handle_input()
    logica_del_juego()
    actualizar_pantalla()