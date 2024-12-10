import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math


class Basura:
    # def __init__(self, dim, vel, textures, txtIndex,Id,posX,posZ,oX,oY,oZ,rotation,W,H,D):
    def __init__(self, dim=None, vel=1, textures=None, txtIndex=0, Id=-1, posX=0, posZ=0, oX=0, oY=0, oZ=0, rotation=0, W=1, H=1, D=1):

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
        #changing the order because of opengl is different
        self.W_H_D = [W,H,D]

        # Inicializar las coordenadas (x,y,z) del cubo en el tablero
        # almacenandolas en el vector Position
        # ...
        # Se inicializa un vector de direccion aleatorio
        self.ordered_W_H_D = [W,H,D]

        tempW_H_D = [W,H,D]

        self.W_H_D = [W,D,H]

        if self.rotationType == 0:
            self.ordered_W_H_D = [self.W_H_D[0],self.W_H_D[1],self.W_H_D[2]]
        elif self.rotationType == 1:
            self.ordered_W_H_D = [self.W_H_D[1],self.W_H_D[0],self.W_H_D[2]]
        elif self.rotationType == 2:
            self.ordered_W_H_D = [self.W_H_D[1],self.W_H_D[2],self.W_H_D[0]]
        elif self.rotationType == 3:
            self.ordered_W_H_D = [self.W_H_D[2],self.W_H_D[1],self.W_H_D[0]]
        elif self.rotationType == 4:
            self.ordered_W_H_D = [self.W_H_D[2],self.W_H_D[0],self.W_H_D[1]]
        elif self.rotationType == 5:
            self.ordered_W_H_D = [self.W_H_D[0],self.W_H_D[2],self.W_H_D[1]]

        self.ordered_W_H_D = [self.ordered_W_H_D[0],self.ordered_W_H_D[2],self.ordered_W_H_D[1]]

        self.W_H_D = tempW_H_D







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
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        # glScaled(2, 2, 2)
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

    def draw_ordenada(self):
    #Se muevea a la posicion ordenada
        glPushMatrix()
        glTranslatef(self.orderedPosition[0], self.orderedPosition[1], self.orderedPosition[2])
        self.Position = [0,0,0]
        self.W_H_D = self.ordered_W_H_D

        self.draw()
        glPopMatrix()


