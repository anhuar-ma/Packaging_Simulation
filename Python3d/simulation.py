import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import random
# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Lifter import Lifter
from Basura import Basura

#Necesario para Julia
import requests

URL_BASE = "http://localhost:8000"
r = requests.post(URL_BASE+ "/simulations", allow_redirects=False)
datos = r.json()
# datos se vuelve una lista con los datos de nuestros robots
LOCATION = datos["Location"]
print("--------------------------")
print(LOCATION)
print("--------------------------")



screen_width = 500
screen_height = 500
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=1800.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
EYE_X=200.0
EYE_Y=150.0
EYE_Z=200.0
CENTER_X=0
CENTER_Y=0
CENTER_Z=0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 200


#lifters
lifters = []
cantidad_robots = 0
cantidad_cajas =0
cantidad_estante = 0
escala = 2



for i in range(len(datos["agents"])):
    if datos["agents"][i]["type"] == "Robot":
        cantidad_robots += 1
    elif datos["agents"][i]["type"] == "Box":
        cantidad_cajas += 1
    else:
        cantidad_estante += 1


basuras = []
nbasuras = 10

# Variables para el control del observador
theta = 0.0
radius = 300

# Arreglo para el manejo de texturas
textures = []
filenames = ["img1.bmp","wheel.jpg", "walle.jpg","basura.bmp"]

def Axis():
    glShadeModel(GL_FLAT)
    glLineWidth(3.0)
    #X axis in red
    glColor3f(1.0,0.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(X_MIN,0.0,0.0)
    glVertex3f(X_MAX,0.0,0.0)
    glEnd()
    #Y axis in green
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,Y_MIN,0.0)
    glVertex3f(0.0,Y_MAX,0.0)
    glEnd()
    #Z axis in blue
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0,0.0,Z_MIN)
    glVertex3f(0.0,0.0,Z_MAX)
    glEnd()
    glLineWidth(1.0)

def Texturas(filepath):
    textures.append(glGenTextures(1))
    id = len(textures) - 1
    glBindTexture(GL_TEXTURE_2D, textures[id])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    image = pygame.image.load(filepath).convert()
    w, h = image.get_rect().size
    image_data = pygame.image.tostring(image, "RGBA")
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
    glGenerateMipmap(GL_TEXTURE_2D)

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL: cubos")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    for i in filenames:
        Texturas(i)

    for i in range(cantidad_robots):
        lifters.append(Lifter(DimBoard, 0.7, textures,0,0))

    #Creacion de basuras
    i = 0

for i in range(len(datos["agents"])):
    if datos["agents"][i]["type"] == "Box":
        box = datos["agents"][i]
        basuras.append(Basura(
            DimBoard,1,textures,3,
            box["id"],
            escala * box["pos"][0],
            escala * box["pos"][1],
            escala * box["ordered_position"][0],
            escala * box["ordered_position"][1],
            escala * box["ordered_position"][2],
            box["rotation"],
            box["dimension"][0],
            box["dimension"][1],
            box["dimension"][2]
            ))

#primera caja para sacar
anterior =datos["queue_front"]

def planoText():
    # activate textures
    glColor(0.0, 1, 0)
    #glEnable(GL_TEXTURE_2D)
    # front face
    #glBindTexture(GL_TEXTURE_2D, textures[0])  # Use the first texture
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-DimBoard, 0, -DimBoard)

    glTexCoord2f(0.0, 1.0)
    glVertex3d(-DimBoard, 0, DimBoard)

    glTexCoord2f(1.0, 1.0)
    glVertex3d(DimBoard, 0, DimBoard)

    glTexCoord2f(1.0, 0.0)
    glVertex3d(DimBoard, 0, -DimBoard)

    glEnd()
    # glDisable(GL_TEXTURE_2D)

def checkCollisions():
    for c in lifters:
        for b in basuras:
            distance = math.sqrt(math.pow((b.Position[0] - c.Position[0]), 2) + math.pow((b.Position[2] - c.Position[2]), 2))
            if distance <= c.radiusCol:
                if c.status == 0 and b.alive:
                    b.alive = False
                    c.status = 1
                #print("Colision detectada")

def display():
    response = requests.get(URL_BASE + LOCATION)
    datos = response.json()

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    print(datos)
    print("-------------------------")
    # Se dibujan los robots
    index = 0
    for i in range(cantidad_robots):
        posX = datos["agents"][i]["pos"][0] * escala
        posZ = datos["agents"][i]["pos"][1] * escala
        angle = datos["agents"][i]["looking_at"]
        status = datos["agents"][i]["state"]
        platformHeight = datos["agents"][i]["platformHeight"]
        lifters[index].update(posX, posZ, angle, status, platformHeight)
        lifters[index].draw()
        index += 1
    index = 0
    print("Cantidad de basuras: ", len(datos["agents"]) - (cantidad_robots))

    # for i in range(cantidad_robots, len(datos["agents"]) - cantidad_robots):
    #     posX = datos["agents"][i]["pos"][0] * escala
    #     posZ = datos["agents"][i]["pos"][1] * escala
    #     print(i)
    #     print("Posicion de la basura: ", posX, posZ)
    #     # basuras[index].update(posX, posZ)
    #     basuras[index].draw()
    #     index += 1

    global basuras
    global anterior

    for box in basuras:
        box.draw()
        if(anterior !=datos["queue_front"] and anterior != -1):
            # Assuming basuras is a list of objects with a parameter 'id'
            basuras = [box2 for box2 in basuras if box2.id != anterior]
        anterior = datos["queue_front"]




    # Se dibuja el incinerador
    glColor3f(1.0, 0.5, 0.0)  # Color: Naranja
    square_size = 20.0  # Tamaño

    half_size = square_size / 2.0
    glBegin(GL_QUADS)
    glVertex3d(-half_size, 0.5, -half_size)
    glVertex3d(-half_size, 0.5, half_size)
    glVertex3d(half_size, 0.5, half_size)
    glVertex3d(half_size, 0.5, -half_size)
    glEnd()

    #Se dibujan basuras
    # for obj in basuras:
        # obj.draw()
        #obj.update()
    #Axis()

    #Se dibuja el plano gris
    planoText()
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()

    # Draw the walls bounding the plane
    wall_height = 50.0  # Adjust the wall height as needed

    glColor3f(0.8, 0.8, 0.8)  # Light gray color for walls

    # Draw the left wall
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(-DimBoard, wall_height, DimBoard)
    glVertex3d(-DimBoard, wall_height, -DimBoard)
    glEnd()

    # Draw the right wall
    glBegin(GL_QUADS)
    glVertex3d(DimBoard, 0, -DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, wall_height, DimBoard)
    glVertex3d(DimBoard, wall_height, -DimBoard)
    glEnd()

    # Draw the front wall
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, wall_height, DimBoard)
    glVertex3d(-DimBoard, wall_height, DimBoard)
    glEnd()

    # Draw the back wall
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glVertex3d(DimBoard, wall_height, -DimBoard)
    glVertex3d(-DimBoard, wall_height, -DimBoard)
    glEnd()

    checkCollisions()

def lookAt():
    glLoadIdentity()
    rad = theta * math.pi / 180
    newX = EYE_X * math.cos(rad) + EYE_Z * math.sin(rad)
    newZ = -EYE_X * math.sin(rad) + EYE_Z * math.cos(rad)
    gluLookAt(newX,EYE_Y,newZ,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

done = False
Init()
while not done:
    keys = pygame.key.get_pressed()  # Checking pressed keys
    if keys[pygame.K_RIGHT]:
        if theta > 359.0:
            theta = 0
        else:
            theta += 1.0
        lookAt()
    if keys[pygame.K_LEFT]:
        if theta < 1.0:
            theta = 360.0
        else:
            theta -= 1.0
        lookAt()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        if event.type == pygame.QUIT:
            done = True
    display()

    display()
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()