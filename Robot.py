import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpMat import OpMat

class Robot:

    def __init__(self,opera):
        self.opera = opera
        self.points = np.array([
            #Coche
            [-2, -1, 1], [2, -1, 1], [2, 1, 1],[-2, 1, 1],
            #Llantas
            [-2, 2, 1],[-1, 2, 1],[-1 ,1, 1],
            [2,2,1],[1,2,1],[1,1,1],
            [-2,-2,1],[-1,-2,1],[-1,-1,1],
            [2,-2,1],[1,-1,1],[1,-2,1]
             ])
        self.A = np.identity(3)

        #Movimiento delante y atras
        self.delta_dir = np.array([1.0, 0.0])
        self.deg = 0
        self.deltadeg = 0
        self.deltaT = np.array([1,0 ,0])
        self.T =  np.array([0,0 ,0])
        self.color = [1,0,0]
        self.target_deg = 0

    def setColor(self, r, g, b):
       self.color = [r, g, b]

    def update(self):
        # Calcular la diferencia angular más corta

        diff = (self.target_deg - self.deg + 180) % 360 - 180

        if abs(diff) > 0:  # Solo actualizamos si hay una diferencia
            self.deltadeg = 9 if diff > 0 else -9  # Determinar la dirección
            self.deg += self.deltadeg

            # Asegurar que deg siempre esté en el rango [0, 360)
            self.deg = self.deg % 360


    def render(self):
        self.opera.push()
        self.opera.translation(self.T[0], self.T[1])
        self.opera.rotation(self.deg)
        pointsR = self.points.copy()
        self.opera.mult_Points(pointsR)

        glColor3fv(self.color)
        #Coche
        self.Bresenham(pointsR[0], pointsR[1])
        self.Bresenham(pointsR[1], pointsR[2])
        self.Bresenham(pointsR[2], pointsR[3])
        self.Bresenham(pointsR[3], pointsR[0])

        #Llanta trasera izquierda
        self.Bresenham(pointsR[3], pointsR[4])
        self.Bresenham(pointsR[4], pointsR[5])
        self.Bresenham(pointsR[5], pointsR[6])
        self.Bresenham(pointsR[6], pointsR[3])

        #Llanta delantera izquierda
        self.Bresenham(pointsR[2], pointsR[7])
        self.Bresenham(pointsR[7], pointsR[8])
        self.Bresenham(pointsR[8], pointsR[9])
        self.Bresenham(pointsR[9], pointsR[2])

        #Llanta trasera derecha
        self.Bresenham(pointsR[0], pointsR[10])
        self.Bresenham(pointsR[10], pointsR[11])
        self.Bresenham(pointsR[11], pointsR[12])
        self.Bresenham(pointsR[12], pointsR[0])

        #Llanta delantera derecha
        self.Bresenham(pointsR[1], pointsR[13])
        self.Bresenham(pointsR[13], pointsR[15])
        self.Bresenham(pointsR[15], pointsR[14])
        self.Bresenham(pointsR[14], pointsR[1])

        # Front indicator
        glColor3f(1.0, 0.0, 0.0)  # Red color for the front indicator
        center_x = (pointsR[0][0] + pointsR[2][0]) / 2
        center_y = (pointsR[0][1] + pointsR[2][1]) / 2
        front_x = (pointsR[1][0] + pointsR[2][0]) / 2
        front_y = (pointsR[1][1] + pointsR[2][1]) / 2
        self.Bresenham((center_x, center_y), (front_x, front_y))

        self.opera.pop()
        self.update()


    def Bresenham(self,p1, p2):
        glColor3f(self.color[0], self.color[1], self.color[2])
        x0 = int(p1[0])
        y0 = int(p1[1])
        x1 = int(p2[0])
        y1 = int(p2[1])


        dx = x1 - x0
        dy = y1 - y0

        if dy < 0:
            dy = -dy
            stepy = -1
        else:
            stepy = 1

        if dx < 0:
            dx = -dx
            stepx = -1
        else:
            stepx = 1

        x = x0
        y = y0

        glBegin(GL_POINTS)
        glVertex2i(x0, y0)

        if dx > dy:
            d = 2 * dy - dx
            incE = 2 * dy
            incNE = 2 * (dy - dx)
            while x != x1:
                if d <= 0:
                    d += incE
                else:
                    d += incNE
                    y += stepy
                x += stepx
                glVertex2i(x, y)
        else:
            d = 2 * dx - dy
            incE = 2 * dx
            incNE = 2 * (dx - dy)
            while y != y1:
                if d <= 0:
                    d += incE
                else:
                    d += incNE
                    x += stepx
                y += stepy
                glVertex2i(x, y)
        glEnd()

    def move_forward(self):
        rad = math.radians(self.deg)
        self.T[0] += math.cos(rad)
        self.T[1] += math.sin(rad)

    def move_backward(self):
        rad = math.radians(self.deg)
        self.T[0] -= math.cos(rad)
        self.T[1] -= math.sin(rad)

    def girar(self, angle):
        # Ajuste de orientación para solo 90 grados a la vez
        self.target_deg = (self.deg + angle)
        # Redondear a múltiplos de 90 grados para asegurar que solo se mueva a los ejes
        if self.target_deg < 0:
            self.target_deg += 360
        self.target_deg = angle

