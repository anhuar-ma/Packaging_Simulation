import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math


class Basura:
    def __init__(self, dim, vel, textures, txtIndex,Id,posX,posZ,oX,oY,oZ,rotation,W,H,D):

       #id de la caja de julia
        self.id = Id

        #id del robot que la var a llevar
        self.robotID = 0

        # Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [1,1,1,1,1,-1,1,-1,-1,1,-1,1,-1,1,1,-1,1,-1,-1,-1,-1,-1,-1,1,]

        self.elementArray = [0,1,2,3,0,3,7,4,0,4,5,1,6,2,1,5,6,5,4,7,6,7,3,2,]

        self.vertexColors = [1,1,1,1,0,0,1,1,0,0,1,0,0,0,1,1,0,1,0,0,0,0,1,1,]

        self.dim = dim
        # Se inicializa una posicion aleatoria en el tablero
        self.Position = [posX, 0, posZ]

        self.orderedPosition = [oX, oY, oZ]
        self.rotationType = rotation
        #width, height, depth
        self.W_H_D = [W,H,D]

        # Inicializar las coordenadas (x,y,z) del cubo en el tablero
        # almacenandolas en el vector Position
        # ...
        # Se inicializa un vector de direccion aleatorio
        dirX = random.randint(-10, 10) or 1
        dirZ = random.randint(-1, 1) or 1
        magnitude = math.sqrt(dirX * dirX + dirZ * dirZ) * vel
        self.Direction = [dirX / magnitude, 0, dirZ / magnitude]
        # El vector aleatorio debe de estar sobre el plano XZ (la altura en Y debe ser fija)
        # Se normaliza el vector de direccion
        # ...
        # Se cambia la maginitud del vector direccion con la variable vel
        # ...

        #Arreglo de texturas
        self.textures = textures

        #Index de la textura a utilizar
        self.txtIndex = txtIndex

        #Control variable for drawing
        self.alive = True

    def update(self,posX,posZ):
        # Se debe de calcular la posible nueva posicion del cubo a partir de su
        # posicion acutual (Position) y el vector de direccion (Direction)
        # ...
        return
        # self.Position = [posX, 0, posZ]
        # Se debe verificar que el objeto cubo, con su nueva posible direccion
        # no se salga del plano actual (DimBoard)
        # ...

    def draw(self):
        if self.alive:
            glPushMatrix()
            glTranslatef(self.Position[0], self.Position[1], self.Position[2])
            glScaled(2, 2, 2)
            glColor3f(1.0, 1.0, 1.0)

            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textures[self.txtIndex])

            glBegin(GL_QUADS)

            W = self.W_H_D[0]
            H = self.W_H_D[1]
            D = self.W_H_D[2]

            # Front face, we use Width and Depth
            glTexCoord2f(0.0, 0.0)
            glVertex3d(0, 0, 0)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(W, 0, 0)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(W, 0, D)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(0, 0, D)

            # Back face use Width and Depth , but now with Height
            glTexCoord2f(0.0, 0.0)
            glVertex3d(0, H, 0)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(W, H, 0)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(W, H, D)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(0, H, D)

            # Left face (use Height and Depth)
            glTexCoord2f(0.0, 0.0)
            glVertex3d(0,0, 0)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(0, H, 0)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(0, H, D)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(0, 0, D)

            # Right face (use Height and Depth) but now with Width
            glTexCoord2f(0.0, 0.0)
            glVertex3d(W,0, 0)
            glTexCoord2f(1.0, 0.0)
            glVertex3d(W, H, 0)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(W, H, D)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(W, 0, D)

            # Top face (use Width and Height)
            glTexCoord2f(0.0, 0.0)
            glVertex3d(0, 0, 0)
            glTexCoord2f(0.0, 0.0)
            glVertex3d(W, 0, 0)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(W, H, 0)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(0, H, 0)

            # Bottom face (use Width and Height) but now with Depth
            glTexCoord2f(0.0, 0.0)
            glVertex3d(0, 0, D)
            glTexCoord2f(0.0, 0.0)
            glVertex3d(W, 0, D)
            glTexCoord2f(1.0, 1.0)
            glVertex3d(W, H, D)
            glTexCoord2f(0.0, 1.0)
            glVertex3d(0, H, D)



            glEnd()
            glDisable(GL_TEXTURE_2D)

            glPopMatrix()