import pygame
from pygame.locals import *
from Cubo import Cubo

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

from Basura import Basura


class Lifter:
    def __init__(self, dim, vel, textures,posX,posZ,id):
        self.dim = dim
        # Se inicializa una posicion aleatoria en el tablero
        # self.Position = [random.randint(-dim, dim), 6, random.randint(-dim, dim)]
        self.Position = [posX, 6, posZ]
        # Inicializar las coordenadas (x,y,z) del cubo en el tablero
        # almacenandolas en el vector Position

        # Se inicializa un vector de direccion aleatorio
        dirX = random.randint(-10, 10) or 1
        dirZ = random.randint(-1, 1) or 1
        magnitude = math.sqrt(dirX**2 + dirZ**2)
        self.Direction = [(dirX / magnitude), 0, (dirZ / magnitude)]
        self.angle = 0
        self.vel = vel
        # El vector aleatorio debe de estar sobre el plano XZ (la altura en Y debe ser fija)
        # Se normaliza el vector de direccion

        # Arreglo de texturas
        self.textures = textures

        # Control variables for platform movement
        #Tarda 150 iteraciones en subir o bajar
        self.platformHeight = -1.5
        self.platformUp = False
        self.platformDown = False

        #Control variable for collisions
        self.radiusCol = 5

        #Control variables for animations
        self.status = 0
        self.trashID = -1
        #0 = searching
        #1 = lifting
        #2 = delivering
        #3 = dropping
        #4 = returning
        #Un objecto de la clase Basura que se recibe cuando se recoje
        self.basura = None

        #id del lifter de julia
        self.id = id

        #id de la caja que lleva
        self.box_id = -1

    def search(self):
        # Change direction to random
        dirX = random.randint(-10, 10) or 1
        dirZ = random.randint(-1, 1) or 1
        magnitude = math.sqrt(dirX**2 + dirZ**2)
        self.Direction = [(dirX / magnitude), 0, (dirZ / magnitude)]

    def targetCenter(self):
        # Set direction to center
        dirX = -self.Position[0]
        dirZ = -self.Position[2]
        magnitude = math.sqrt(dirX**2 + dirZ**2)
        self.Direction = [(dirX / magnitude), 0, (dirZ / magnitude)]

    #Se actualizan las variables del objeto segun julia
    def update(self,posX,posZ,angle,status,platformHeight,box_id):
        #Se esta recogiendo la caja
        self.Position = [posX, 6, posZ]
        self.angle = angle
        self.status = status
        self.platformHeight = platformHeight * 0.01
        self.box_id = box_id


    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glRotatef(self.angle + 180 , 0, 1, 0)
        glScaled(5, 5, 5)
        glColor3f(1.0, 1.0, 1.0)
        # front face
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures[2])
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(1, 1, 1)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(1, 1, -1)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(1, -1, -1)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(1, -1, 1)

        # 2nd face
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-2, 1, 1)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(1, 1, 1)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(1, -1, 1)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-2, -1, 1)

        # 3rd face
        glTexCoord2f(0.0, 0.0)
        glVertex3d(-2, 1, -1)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2, 1, 1)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-2, -1, 1)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(-2, -1, -1)

        # 4th face
        glTexCoord2f(0.0, 0.0)
        glVertex3d(1, 1, -1)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2, 1, -1)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-2, -1, -1)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(1, -1, -1)

        # top
        glTexCoord2f(0.0, 0.0)
        glVertex3d(1, 1, 1)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(-2, 1, 1)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(-2, 1, -1)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(1, 1, -1)
        glEnd()

        # Head

        glPushMatrix()
        glTranslatef(0, 1.5, 0)
        glScaled(0.8, 0.8, 0.8)
        glColor3f(1.0, 1.0, 1.0)
        head = Cubo(self.textures, 0)
        head.draw()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

        # Wheels
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures[1])
        glPushMatrix()
        glTranslatef(-1.2, -1, 1)
        glScaled(0.3, 0.3, 0.3)
        glColor3f(1.0, 1.0, 1.0)
        wheel = Cubo(self.textures, 0)
        wheel.draw()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.5, -1, 1)
        glScaled(0.3, 0.3, 0.3)
        wheel = Cubo(self.textures, 0)
        wheel.draw()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.5, -1, -1)
        glScaled(0.3, 0.3, 0.3)
        wheel = Cubo(self.textures, 0)
        wheel.draw()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-1.2, -1, -1)
        glScaled(0.3, 0.3, 0.3)
        wheel = Cubo(self.textures, 0)
        wheel.draw()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

        # Lifter
        glPushMatrix()
        if self.status == 2 or self.status == 3 or self.status == 4:
            self.drawTrash()
        glColor3f(0.0, 0.0, 0.0)
        glTranslatef(0, self.platformHeight, 0)  # Up and down
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3d(1, 1, 1)
        glTexCoord2f(0.0, 1.0)
        glVertex3d(1, 1, -1)
        glTexCoord2f(1.0, 1.0)
        glVertex3d(3, 1, -1)
        glTexCoord2f(1.0, 0.0)
        glVertex3d(3, 1, 1)
        glEnd()
        glPopMatrix()
        glPopMatrix()


    def getTrash(self,basura):
        self.basura = basura


    def drawTrash(self):
        glPushMatrix()
        glTranslatef(2, (self.platformHeight + 1.5), 0)
        glScaled(0.2, 0.2, 0.2)
        glColor3f(1.0, 1.0, 1.0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.textures[3])

        # glBegin(GL_QUADS)
        if self.basura != None:
            print("O"*1000)
            self.basura.draw()

        # glEnd()
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()