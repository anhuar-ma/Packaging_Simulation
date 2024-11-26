import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Basura import Basura

import random
import math


class Contenedor:
    def __init__(self, posX,posZ,W,H,D):

        #id del robot que la var a llevar
        self.robotID = 0

        # Se inicializa las coordenadas de los vertices del cubo
        self.vertexCoords = [1,1,1,1,1,-1,1,-1,-1,1,-1,1,-1,1,1,-1,1,-1,-1,-1,-1,-1,-1,1,]

        self.elementArray = [0,1,2,3,0,3,7,4,0,4,5,1,6,2,1,5,6,5,4,7,6,7,3,2,]

        self.vertexColors = [1,1,1,1,0,0,1,1,0,0,1,0,0,0,1,1,0,1,0,0,0,0,1,1,]

        # Se inicializa una posicion aleatoria en el tablero
        self.Position = [posX, 0, posZ]

        #width, height, depth
        self.W_H_D = [W,H,D]

        #array de cajas en el contenedor
        self.cajas = []

        # Inicializar las coordenadas (x,y,z) del cubo en el tablero
        # almacenandolas en el vector Position
        # ...
        # Se inicializa un vector de direccion aleatorio
        # El vector aleatorio debe de estar sobre el plano XZ (la altura en Y debe ser fija)
        # Se normaliza el vector de direccion
        # ...
        # Se cambia la maginitud del vector direccion con la variable vel
        # ...

        #Control variable for drawing

    def update(self,caja):
        # Se debe de calcular la posible nueva posicion del cubo a partir de su
        # posicion acutual (Position) y el vector de direccion (Direction)
        # ...

        self.cajas.append(caja)

        return
        # self.Position = [posX, 0, posZ]
        # Se debe verificar que el objeto cubo, con su nueva posible direccion
        # no se salga del plano actual (DimBoard)
        # ...

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        # glScaled(2, 2, 2)
        # glColor3f(1.0, 1.0, 1.0)
        # glColor4f(1.0, 1.0, 1.0, 0.5)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 0.0, 0.0, 0.5)  # Set color with alpha for transparency


        print("Contenedor")
        print(self.W_H_D)
        print(self.Position)
        glBegin(GL_LINE_LOOP)

        W = self.W_H_D[0]
        H = self.W_H_D[1]
        D = self.W_H_D[2]


        # Front face, we use Width and Depth
        glVertex3d(0, 0, 0)
        glVertex3d(W, 0, 0)
        glVertex3d(W, 0, D)
        glVertex3d(0, 0, D)

        # Back face use Width and Depth , but now with Height
        glVertex3d(0, H, 0)
        glVertex3d(W, H, 0)
        glVertex3d(W, H, D)
        glVertex3d(0, H, D)

        # Left face (use Height and Depth)
        glVertex3d(0,0, 0)
        glVertex3d(0, H, 0)
        glVertex3d(0, H, D)
        glVertex3d(0, 0, D)

        # Right face (use Height and Depth) but now with Width
        glVertex3d(W,0, 0)
        glVertex3d(W, H, 0)
        glVertex3d(W, H, D)
        glVertex3d(W, 0, D)

        # Top face (use Width and Height)
        glVertex3d(0, 0, 0)
        glVertex3d(W, 0, 0)
        glVertex3d(W, H, 0)
        glVertex3d(0, H, 0)

        # Bottom face (use Width and Height) but now with Depth
        glVertex3d(0, 0, D)
        glVertex3d(W, 0, D)
        glVertex3d(W, H, D)
        glVertex3d(0, H, D)

        glEnd()
        for caja in self.cajas:
            glPushMatrix()
            caja.draw_ordenada()
            glPopMatrix()



        glDisable(GL_BLEND)
        glPopMatrix()