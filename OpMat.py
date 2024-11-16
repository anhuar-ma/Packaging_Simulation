import numpy as np
import math

class OpMat:

    def __init__(self):
        self.A = np.identity(3)
        self.T = np.identity(3)
        self.R = np.identity(3)
        self.S = np.identity(3)
        self.stack = []


    def translation(self, tx, ty):
        self.T[0][2] = tx
        self.T[1][2] = ty
        self.A = self.A @ self.T


    def rotation(self, deg):
        #los deg tienen que ser convertidos a radianes
        deg = math.radians(deg)
        self.R[0][0] = math.cos(deg)
        self.R[0][1] = - math.sin(deg)
        self.R[1][0] = math.sin(deg)
        self.R[1][1] = math.cos(deg)
        self.A = self.A @ self.R

    def scale(self, sx, sy):
        self.S[0][0] = sx
        self.S[1][1] = sy
        self.A = self.A @ self.S

    def mult_Points(self, points):
        for i in range(len(points)):
            points[i] = np.transpose(self.A @ (np.transpose(np.reshape(points[i], (1, -1)))))
        return points

    def loadId(self):
        self.A = np.identity(3)

    def push(self):
        self.stack.append(self.A.copy())

    def pop(self):
        if len(self.stack) > 0:
            # print("A matrix in STACK")
            self.A = self.stack[-1]
            self.stack.pop()
            # print(self.A)
        else:
            print("No hay posible operaciones")