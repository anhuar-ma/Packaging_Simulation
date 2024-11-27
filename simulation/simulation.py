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
from Contenedor import Contenedor

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



screen_width = 800
screen_height = 600
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=1800.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

GLOBAL_CENTER_X=0
GLOBAL_CENTER_Y=10
GLOBAL_CENTER_Z=0

EYE_X=300.0
EYE_Y=150.0
EYE_Z= 0.0
CENTER_X=0
CENTER_Y=30
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


wallHeight = 800
wallWidth = 800


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
filenames = ["textures/img1.bmp","textures/wheel.jpg", "textures/walle1.jpeg",
             "textures/basura.bmp", "concrete/concrete_ja.png", "warehouse/corru_iron.png",
             "warehouse/rusty.jpg"]

textures_backgrounds = []
filenames_backgrounds = ["fondo/front.png", "fondo/back.png", "fondo/left.png", "fondo/right.png",  "fondo/sky.png"]

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


def Background_Texturas(filepath):
    textures_backgrounds.append(glGenTextures(1))
    id = len(textures_backgrounds) - 1
    glBindTexture(GL_TEXTURE_2D, textures_backgrounds[id])
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

    for i in filenames_backgrounds:
        Background_Texturas(i)

    glPushMatrix()
    glTranslatef(100.0, 0.0, 0.0)

    #Creacion de basuras y robots
    i = 0
    glPopMatrix()

Contenedores = []

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
            escala * box["dimension"][0],
            escala * box["dimension"][1],
            escala * box["dimension"][2]
            ))
    elif datos["agents"][i]["type"] == "Robot":
        robot = datos["agents"][i]
        lifters.append(Lifter(
            DimBoard, 0.7, textures,
            escala * robot["pos"][0],
            escala * robot["pos"][1],
            robot["id"]
        ))
    elif datos["agents"][i]["type"] == "Contenedor":
        contenedor = datos["agents"][i]
        Contenedores.append(Contenedor(
            escala * contenedor["position"][0],
            escala * contenedor["position"][1],
            escala * contenedor["dimension"][0],
            escala * contenedor["dimension"][1],
            escala * contenedor["dimension"][2]
        ))

#primera caja para sacar
anterior =datos["queue_front"]

#creacion de contenedor



def planoText():
    # activate textures
    glColor(0.5, 0.5, 0.5)
    glEnable(GL_TEXTURE_2D)
    # front face
# filenames_backgrounds = ["fondo/front.png", "fondo/back.png", "fondo/left.png", "fondo/right.png", "fondo/sky.png"]

    glBindTexture(GL_TEXTURE_2D, textures[4])  # Use the first texture
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
    glDisable(GL_TEXTURE_2D)

def tiled_texture(x_min, x_max, y_min, y_max, texture_id, tile_count_x, tile_count_y):
    """
    Renders a texture repeatedly in a specified area to maintain resolution.
    
    Parameters:
    - x_min, x_max: float, the horizontal bounds of the area.
    - y_min, y_max: float, the vertical bounds of the area.
    - texture_id: int, the OpenGL texture ID to use.
    - tile_count_x: int, number of times to repeat the texture horizontally.
    - tile_count_y: int, number of times to repeat the texture vertically.
    """
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glColor(1.0, 1.0, 1.0)  # Set color to white to preserve texture color

    # Calculate the texture coordinates based on the tile counts
    tex_coord_x_max = tile_count_x
    tex_coord_y_max = tile_count_y

    glBegin(GL_QUADS)
    # Bottom-left
    glTexCoord2f(0.0, 0.0)
    glVertex3d(x_min, 0, y_min)
    
    # Bottom-right
    glTexCoord2f(tex_coord_x_max, 0.0)
    glVertex3d(x_max, 0, y_min)
    
    # Top-right
    glTexCoord2f(tex_coord_x_max, tex_coord_y_max)
    glVertex3d(x_max, 0, y_max)
    
    # Top-left
    glTexCoord2f(0.0, tex_coord_y_max)
    glVertex3d(x_min, 0, y_max)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def tiled_texture_with_loop(x_min, x_max, y_min, y_max, texture_id, tile_size):
    """
    Renders a texture repeatedly in a specified area using a loop.

    Parameters:
    - x_min, x_max: float, the horizontal bounds of the area.
    - y_min, y_max: float, the vertical bounds of the area.
    - texture_id: int, the OpenGL texture ID to use.
    - tile_size: float, the size of each texture tile.
    """
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor(1.0, 1.0, 1.0)  # Set color to white to preserve texture color

    # Loop over the area to create quads
    y = y_min
    while y < y_max:
        x = x_min
        while x < x_max:
            # Calculate the bounds of the current tile
            x1 = x
            x2 = min(x + tile_size, x_max)
            y1 = y
            y2 = min(y + tile_size, y_max)

            glBegin(GL_QUADS)
            # Bottom-left corner
            glTexCoord2f(0.0, 0.0)
            glVertex3f(x1, 0, y1)

            # Bottom-right corner
            glTexCoord2f(1.0, 0.0)
            glVertex3f(x2, 0, y1)

            # Top-right corner
            glTexCoord2f(1.0, 1.0)
            glVertex3f(x2, 0, y2)

            # Top-left corner
            glTexCoord2f(0.0, 1.0)
            glVertex3f(x1, 0, y2)
            glEnd()

            x += tile_size
        y += tile_size

    glDisable(GL_TEXTURE_2D)

def backgrountText():
    glPushMatrix()
    glTranslate(0, -100, 0)
    glEnable(GL_TEXTURE_2D)
    
    # Adjusted front face
    glBindTexture(GL_TEXTURE_2D, textures_backgrounds[1])
    glColor(1.0, 1.0, 1.0)


    dim = wallWidth / 2
    dimHeight = 400
    
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)  # Flip vertically
    glVertex3d(-dim, 0, dim)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(dim, 0, dim)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(dim, dimHeight, dim)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-dim, dimHeight, dim)
    glEnd()


    
    # Adjusted back face
    glBindTexture(GL_TEXTURE_2D, textures_backgrounds[2])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(dim, 0, -dim)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-dim, 0, -dim)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-dim, dimHeight, -dim)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(dim, dimHeight, -dim)
    glEnd()

    # Adjusted left face
    glBindTexture(GL_TEXTURE_2D, textures_backgrounds[0])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-dim, 0, -dim)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-dim, 0, dim)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-dim, dimHeight, dim)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-dim, dimHeight, -dim)
    glEnd()

    # Adjusted right face
    glBindTexture(GL_TEXTURE_2D, textures_backgrounds[3])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(dim, 0, dim)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(dim, 0, -dim)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(dim, dimHeight, -dim)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(dim, dimHeight, dim)
    glEnd()

    # Adjusted top face
    glBindTexture(GL_TEXTURE_2D, textures_backgrounds[4])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-dim, dimHeight, dim)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(dim, dimHeight, dim)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(dim, dimHeight, -dim)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-dim, dimHeight, -dim)
    glEnd()

    # # Adjusted bottom face
    # glBindTexture(GL_TEXTURE_2D, textures_backgrounds[4])
    # glBegin(GL_QUADS)
    # glTexCoord2f(0.0, 1.0)
    # glVertex3d(-dim, 0, -dim)
    # glTexCoord2f(1.0, 1.0)
    # glVertex3d(dim, 0, -dim)
    # glTexCoord2f(1.0, 0.0)
    # glVertex3d(dim, 0, dim)
    # glTexCoord2f(0.0, 0.0)
    # glVertex3d(-dim, 0, dim)
    # glEnd()
    
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()



def generate_warehouse(dim, textures):

    dim_length = 300
    dim_width = 150
    dim_height = 100
    """
    Generates a textured warehouse starting from the origin, with textures visible from inside.

    Parameters:
    - dim: float, half the size of the warehouse (distance from the origin to each wall).
    - textures: list of int, OpenGL texture IDs for each face in this order:
        [front, back, left, right, top, bottom]
    """
    glEnable(GL_TEXTURE_2D)

    # Front wall (positive Z direction) LEFT WALL
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 0, dim_width)  # Bottom-left
    glTexCoord2f(1.0, 0.0)
    glVertex3f(dim_length, 0, dim_width)   # Bottom-right
    glTexCoord2f(1.0, 1.0)
    glVertex3f(dim_length, dim_height, dim_width)    # Top-right
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, dim_height, dim_width)   # Top-left
    glEnd()

    # Back wall (negative Z direction) RIGHT WALL
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(dim_length, 0, -dim_width)  # Bottom-left
    glTexCoord2f(1.0, 0.0)
    glVertex3f(0, 0, -dim_width) # Bottom-right
    glTexCoord2f(1.0, 1.0)
    glVertex3f(0, dim_height, -dim_width)  # Top-right
    glTexCoord2f(0.0, 1.0)
    glVertex3f(dim_length, dim_height, -dim_width)   # Top-left
    glEnd()

    # # Left wall (negative X direction)
    # glBindTexture(GL_TEXTURE_2D, textures[2])
    # glBegin(GL_QUADS)
    # glTexCoord2f(0.0, 0.0)
    # glVertex3f(-dim, -dim, -dim) # Bottom-left
    # glTexCoord2f(1.0, 0.0)
    # glVertex3f(-dim, -dim, dim)  # Bottom-right
    # glTexCoord2f(1.0, 1.0)
    # glVertex3f(-dim, dim, dim)   # Top-right
    # glTexCoord2f(0.0, 1.0)
    # glVertex3f(-dim, dim, -dim)  # Top-left
    # glEnd()

    # Right wall (positive X direction) Back WALL
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(dim_length, 0, dim_width)   # Bottom-left
    glTexCoord2f(1.0, 0.0)
    glVertex3f(dim_length, 0, -dim_width)  # Bottom-right
    glTexCoord2f(1.0, 1.0)
    glVertex3f(dim_length, dim_height, -dim_width)   # Top-right
    glTexCoord2f(0.0, 1.0)
    glVertex3f(dim_length, dim_height, dim_width)    # Top-left
    glEnd()

    # Ceiling (top)
    glBindTexture(GL_TEXTURE_2D, textures[5])
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, dim_height, dim_width)   # Bottom-left
    glTexCoord2f(1.0, 0.0)
    glVertex3f(dim_length, dim_height, dim_width)    # Bottom-right
    glTexCoord2f(1.0, 1.0)
    glVertex3f(dim_length, dim_height, -dim_width)   # Top-right
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, dim_height, -dim_width)  # Top-left
    glEnd()

    # # Floor (bottom)
    # glBindTexture(GL_TEXTURE_2D, textures[4])
    # glBegin(GL_QUADS)
    # glTexCoord2f(0.0, 0.0)
    # glVertex3f(-dim, -dim, -dim) # Bottom-left
    # glTexCoord2f(1.0, 0.0)
    # glVertex3f(dim, -dim, -dim)  # Bottom-right
    # glTexCoord2f(1.0, 1.0)
    # glVertex3f(dim, -dim, dim)   # Top-right
    # glTexCoord2f(0.0, 1.0)
    # glVertex3f(-dim, -dim, dim)  # Top-left
    # glEnd()

    glDisable(GL_TEXTURE_2D)



def generate_warehouse_with_tiling(dim_length, dim_width, dim_height, textures, tile_size):
    """
    Generates a textured warehouse starting from the origin, with textures visible from inside,
    and textures tiled using a while loop.

    Parameters:
    - dim_length: float, length of the warehouse (X-axis).
    - dim_width: float, width of the warehouse (Z-axis).
    - dim_height: float, height of the warehouse (Y-axis).
    - textures: list of int, OpenGL texture IDs for each face.
    - tile_size: float, size of each texture tile.
    """
    glPushMatrix()
    glTranslate(-20, 0, 0)

    glEnable(GL_TEXTURE_2D)

    # Helper function to draw a tiled wall
    def draw_tiled_wall(x_start, x_end, y_start, y_end, z_value, texture_id, axis):
        """
        Draws a wall with tiled textures.

        Parameters:
        - x_start, x_end: X bounds of the wall.
        - y_start, y_end: Y bounds of the wall.
        - z_value: Fixed Z position for the wall (or X for side walls).
        - texture_id: OpenGL texture ID.
        - axis: 'z' for front/back walls, 'x' for left/right walls, 'y' for top/bottom walls.
        """
        glBindTexture(GL_TEXTURE_2D, texture_id)

        y = y_start
        while y < y_end:
            x = x_start
            while x < x_end:
                x1, x2 = x, min(x + tile_size, x_end)
                y1, y2 = y, min(y + tile_size, y_end)

                glBegin(GL_QUADS)
                if axis == 'z':  # Front or back walls
                    glTexCoord2f(0.0, 0.0)
                    glVertex3f(x1, y1, z_value)
                    glTexCoord2f(1.0, 0.0)
                    glVertex3f(x2, y1, z_value)
                    glTexCoord2f(1.0, 1.0)
                    glVertex3f(x2, y2, z_value)
                    glTexCoord2f(0.0, 1.0)
                    glVertex3f(x1, y2, z_value)
                elif axis == 'x':  # Left or right walls
                    glTexCoord2f(0.0, 0.0)
                    glVertex3f(z_value, y1, x1)
                    glTexCoord2f(1.0, 0.0)
                    glVertex3f(z_value, y1, x2)
                    glTexCoord2f(1.0, 1.0)
                    glVertex3f(z_value, y2, x2)
                    glTexCoord2f(0.0, 1.0)
                    glVertex3f(z_value, y2, x1)
                elif axis == 'y':  # Top or bottom walls
                    glTexCoord2f(0.0, 0.0)
                    glVertex3f(x1, z_value, y1)
                    glTexCoord2f(1.0, 0.0)
                    glVertex3f(x2, z_value, y1)
                    glTexCoord2f(1.0, 1.0)
                    glVertex3f(x2, z_value, y2)
                    glTexCoord2f(0.0, 1.0)
                    glVertex3f(x1, z_value, y2)
                glEnd()

                x += tile_size
            y += tile_size

    # Front wall (positive Z direction)
    draw_tiled_wall(0, dim_length, 0, dim_height, dim_width, textures[6], 'z')

    # Back wall (negative Z direction)
    draw_tiled_wall(0, dim_length, 0, dim_height, -dim_width, textures[6], 'z')

    # Left wall (negative X direction)
    draw_tiled_wall(-dim_width, dim_width, 0, dim_height, 0, textures[6], 'x')

    # Right wall (positive X direction)
    draw_tiled_wall(dim_length, dim_length, 0, dim_height, 0, textures[6], 'x')

    # Ceiling (top)
    draw_tiled_wall(0, dim_length, -dim_width, dim_width, dim_height, textures[6], 'y')

    # Floor (bottom)
    # draw_tiled_wall(0, dim_length, -dim_width, dim_width, 0, textures[5], 'y')

    glDisable(GL_TEXTURE_2D)    

    glPopMatrix()





box_in_container = Basura()
dim_length = 300
dim_width = 150
dim_height = 100
tile_size = 50  # Each tile will cover 50x50 units

def display():
    glPushMatrix()
    glTranslatef(0.0, 0.0, -100.0)

    #Creacion de basuras y robots

    global box_in_container
    global basuras
    global anterior

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
        angle = datos["agents"][i]["angle"]
        status = datos["agents"][i]["state"]
        platformHeight = datos["agents"][i]["platformHeight"]
        box_id = datos["agents"][i]["box_id"]
        lifters[index].update(posX, posZ, angle, status, platformHeight,box_id)
        lifters[index].draw()

        print("platformHeight ", platformHeight)
        print("status ", status)
        print("box_in_container ", box_in_container.id)
        print("-"*100)

        # Se agrega al lifter la caja
        if status == 2 and platformHeight == -150 and box_id != -1:
            for box in basuras:
                if box.id == box_id:
                    lifters[index].getTrash(box)
                    basuras.remove(box)
                    # box_in_container = box
                    break
        #Cuando el lifter la deja, se agrega al contenedor
        # if status == 4 and platformHeight == -150 and box_in_container.id != -1:
        if status == 4 and platformHeight == -150:
            # Contenedores[0].update(box_in_container)
            Contenedores[0].update(lifters[index].basura)
            lifters[index].basura = None
            # box_in_container = Basura()

        index += 1
    index = 0

    for box in basuras:
        box.draw()
        print("Box id: ", box.id)
        print("Box position: ", box.Position)
        print("Anterior: ", anterior)
        print("basuras size: " , len(basuras))
        print("rotation" , box.rotationType)

    for contenedor in Contenedores:
        contenedor.draw()
        print("Contenedor position: ", contenedor.Position)

    # Se dibuja el incinerador
    glColor3f(1.0, 0.5, 0.0)  # Color: Naranja
    square_size = 20.0  # Tamaño
    
    glPopMatrix()

    half_size = square_size / 2.0
    pos_x = 0
    pos_z = 100
    glBegin(GL_QUADS)
    glVertex3d(-half_size, 0.5, -half_size)
    glVertex3d(-half_size, 0.5, half_size)
    glVertex3d(half_size, 0.5, half_size)
    glVertex3d(half_size, 0.5, -half_size)
    glEnd()

    #Se dibuja el eje X en rojo
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3d(0, 0, 0)
    glVertex3d(100, 0, 0)
    glEnd()

    #Se dibuja el eje Y en negro
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3d(0, 0, 0)
    glVertex3d(0, 100, 0)
    glEnd()

    #Se dibuja el eje Z en azul
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3d(0, 0, 0)
    glVertex3d(0, 0, 100)
    glEnd()

    #Se dibuja el plano gris
    # planoText()
    backgrountText()
    # tiled_texture(-DimBoard, DimBoard, -DimBoard, DimBoard, textures_backgrounds[0], 100, 100)
    tiled_texture_with_loop(-wallWidth, wallWidth, -wallWidth, wallWidth, textures[4], 80)

    # generate_warehouse(100, textures)
    generate_warehouse_with_tiling(dim_length, dim_width, dim_height, textures, tile_size)


    # glColor3f(0.3, 0.3, 0.3)
    # glBegin(GL_QUADS)
    # glVertex3d(-DimBoard, 0, -DimBoard)
    # glVertex3d(-DimBoard, 0, DimBoard)
    # glVertex3d(DimBoard, 0, DimBoard)
    # glVertex3d(DimBoard, 0, -DimBoard)
    # glEnd()

    # Draw the walls bounding the plane
    # wall_height = 50.0  # Adjust the wall height as needed

    # glColor3f(0.8, 0.8, 0.8)  # Light gray color for walls

    # Draw the left wall
    # glBegin(GL_QUADS)
    # glVertex3d(-DimBoard, 0, -DimBoard)
    # glVertex3d(-DimBoard, 0, DimBoard)
    # glVertex3d(-DimBoard, wall_height, DimBoard)
    # glVertex3d(-DimBoard, wall_height, -DimBoard)
    # glEnd()

    # # Draw the right wall
    # glBegin(GL_QUADS)
    # glVertex3d(DimBoard, 0, -DimBoard)
    # glVertex3d(DimBoard, 0, DimBoard)
    # glVertex3d(DimBoard, wall_height, DimBoard)
    # glVertex3d(DimBoard, wall_height, -DimBoard)
    # glEnd()

    # # Draw the front wall
    # glBegin(GL_QUADS)
    # glVertex3d(-DimBoard, 0, DimBoard)
    # glVertex3d(DimBoard, 0, DimBoard)
    # glVertex3d(DimBoard, wall_height, DimBoard)
    # glVertex3d(-DimBoard, wall_height, DimBoard)
    # glEnd()

    # # Draw the back wall
    # glBegin(GL_QUADS)
    # glVertex3d(-DimBoard, 0, -DimBoard)
    # glVertex3d(DimBoard, 0, -DimBoard)
    # glVertex3d(DimBoard, wall_height, -DimBoard)
    # glVertex3d(-DimBoard, wall_height, -DimBoard)
    # glEnd()


    # checkCollisions()

def lookAt():
    glLoadIdentity()
    rad = theta * math.pi / 180
    newX = EYE_X * math.cos(rad) + EYE_Z * math.sin(rad)
    newZ = -EYE_X * math.sin(rad) + EYE_Z * math.cos(rad)
    gluLookAt(newX,EYE_Y,newZ,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)

def update_camera(view_id):
    global EYE_X, EYE_Y, EYE_Z, CENTER_X, CENTER_Y, CENTER_Z
    if view_id == 1:  # Vista 1
        EYE_X, EYE_Y, EYE_Z = 200.0, 150.0, 200.0
        CENTER_X, CENTER_Y, CENTER_Z = 0, 0, 0
    elif view_id == 2:  # Vista 2
        EYE_X, EYE_Y, EYE_Z = -80.0, 150.0, 80.0
        CENTER_X, CENTER_Y, CENTER_Z = 0, 0, 0
    elif view_id == 3:  # Vista 3
        EYE_X, EYE_Y, EYE_Z = 150.0, 80.0, 0.0
        CENTER_X, CENTER_Y, CENTER_Z = 0, 0, 0
    elif view_id == 4:  # Vista 4
        EYE_X, EYE_Y, EYE_Z = 0.0, 20.0, 110.0
        CENTER_X, CENTER_Y, CENTER_Z = 0, 20, 0
    elif view_id == 5:  # Vista 5
        EYE_X, EYE_Y, EYE_Z = -75.0, 20.0, 0.0
        CENTER_X, CENTER_Y, CENTER_Z = 0, 20, 0

    lookAt()

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
            if event.key == pygame.K_1:
                update_camera(1)
            if event.key == pygame.K_2:
                update_camera(2)
            if event.key == pygame.K_3:
                update_camera(3)
            if event.key == pygame.K_4:
                update_camera(4)
            if event.key == pygame.K_5:
                update_camera(5)

        if event.type == pygame.QUIT:
            done = True

        
    display()

    display()
    pygame.display.flip()
    pygame.time.wait(10)
pygame.quit()