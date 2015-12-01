import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# NEEDS PYTHON2-PILLOW
import PIL.Image

from collections import namedtuple

import math

from constants import *

from operator import add

# Provides the capabilities for stablish an image in the 3D virtual world
class Image:
    def __init__(self, img_file_name):
        image = PIL.Image.open(img_file_name).convert("RGBA")
        self.raw_data = image.tobytes("raw", "RGBA", 0, -1)
        self.width, self.height = image.size

        glEnable( GL_TEXTURE_2D )

        # Texture identifier assignment and binding
        self.id_text = glGenTextures( 1 )
        glBindTexture( GL_TEXTURE_2D, self.id_text )

        # Texture mipmaps
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP, GL_TRUE)

        # Send texels to GPU
        # Params: flag, mipmap level, intern format, width, height, border size, texels format, texel type, texture
        glTexImage2D(GL_TEXTURE_2D,0,3,self.width,self.height,0,GL_RGBA,GL_UNSIGNED_BYTE,self.raw_data)

        # Unbinding
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable( GL_TEXTURE_2D )

    def draw(self):
        #window_size = (glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        window_size = (1024,800)

        # Prepares the image region
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, window_size[0], 0.0, window_size[1], -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        glLoadIdentity()

        glColor3f(1,1,1)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.id_text)

        # Draw a textured quad
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex3f(0, 0, 0)
        glTexCoord2f(0, 1); glVertex3f(0, window_size[1], 0)
        glTexCoord2f(1, 1); glVertex3f(window_size[0], window_size[1], 0)
        glTexCoord2f(1, 0); glVertex3f(window_size[0], 0, 0)
        glEnd()

        glDisable(GL_TEXTURE_2D)
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)

# Provides the capabilities for draw the line that join two points
class Line:
    def __init__(self, points, color):
        self.points = [[points[i][j] for j in range(3)] for i in range(2)]
        self.color = color

    def draw(self):
        # Draw the line
        glColor3f(*self.color)
        glBegin(GL_LINES)
        glVertex3f(*self.points[0])
        glVertex3f(*self.points[1])
        glEnd()

        # Draw the line shadow
        shadows = [[self.points[i][j] for j in range(3)] for i in range(2)]
        shadows[0][1] = shadows[1][1] = 0
        glColor3f(*steel_gray)
        glBegin(GL_LINES)
        glVertex3f(*shadows[0])
        glVertex3f(*shadows[1])
        glEnd()

    # Provides the director vector of the line
    def getDirVector(self):
        vector = [self.points[0][i] - self.points[1][i] for i in range(3)]
        vec_module = math.sqrt(sum([vector[i]**2 for i in range(3)]))
        return [vector[i]/vec_module for i in range(3)]

# Provides the capabilities for draw a ball
class Ball:
    # Quality of the ball
    Slices = SLICES
    Stacks = STACKS

    def __init__(self, color, radius, coord):
        self.color = color
        self.radius = radius
        self.coord = [coord[i] for i in range(3)]

    def draw(self):
        # Initialize the MODELVIEW Matrix
        glMatrixMode(GL_MODELVIEW)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glPushMatrix()

        # Draw the sphere
        glColor3f(*self.color)
        glTranslatef(*self.coord)

        glutSolidSphere(self.radius,self.Slices,self.Stacks)

        # Revert the matrix stack to its previous state
        glPopMatrix()

        # Draw the sphere shadow
        shadow_radius = self.radius*(1+self.coord[1]/380)
        glColor3f(*steel_gray)

        # Draw a filled disk
        glBegin(GL_POLYGON)
        for i in range(self.Slices):
            angle = i*2*math.pi/self.Slices
            x = shadow_radius * math.cos(angle) + self.coord[0]
            z = shadow_radius * math.sin(angle) + self.coord[2]

            glVertex3f(x,0.0,z)
        glEnd()

        glutPostRedisplay()

# Provides the capabilities for draw a region described by several points
class Quad:
    def __init__(self, points, color=steel_red):
        self.points = points
        self.color = color

    def draw(self):
        # Initialize the MODELVIEW Matrix
        glMatrixMode(GL_MODELVIEW)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Draw the quad
        glColor3f(*self.color)

        glBegin(GL_QUADS)
        for point in self.points:
            glVertex3f(*point)
        glEnd()

# Provides the capabilities for draw a circle
class Circle:
    def __init__(self,center=[0.,0.],radius=10,color=steel_red):
        self.center = center
        self.radius = radius
        self.color  = color

    def draw(self):
        #window_size = (glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        window_size = (1024,800)

        # Prepares the region for draw
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, window_size[0], 0.0, window_size[1], -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        glLoadIdentity()

        glColor3f(*self.color)

        # Draw a filled disk
        glBegin(GL_POLYGON)
        for i in range(SLICES):
            angle = i*2*math.pi/SLICES
            x = self.radius * math.cos(angle) + self.center[0]
            y = self.radius * math.sin(angle) + self.center[1]

            glVertex2f(x,y)
        glEnd()

        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)


class Loader:
    loader_radius = 55
    loader_width = 25

    def __init__(self, center=[0.0,0.0], color=steel_red):
        self.center = center
        self.color = color
        self.loading = False
        self.load_perc = 0

        self.circle = Circle([0,0],0,self.color)

    def activate(self):
        self.loading = True

    def deactivate(self):
        self.loading = False
        self.reset()

    def reset(self):
        self.load_perc = 0

    def load(self):
        if self.loading:
            self.load_perc = self.load_perc + 1
            return self.load_perc >= 100
        return True

    def draw(self):
        if self.loading:
            for tick in range(self.load_perc):
                radius = 15 + self.loader_width * tick / 100.

                angle  = tick*2.0*math.pi/100.0
                center_x = self.loader_radius * math.cos(angle) + self.center[0]
                center_y = self.loader_radius * math.sin(angle) + self.center[1]

                self.circle.center = [center_x,center_y]
                self.circle.radius = radius
                self.circle.draw()

class Button(object):
    def __init__(self, rect, epsilon = BUTTON_TOL):
        self.rect = rect
        self.epsilon = epsilon

    def isTouched(self, point):
        return self.rect[0][0] - self.epsilon < point[0] < self.rect[1][0] + self.epsilon and self.rect[0][1] - self.epsilon < point[1] < self.rect[1][1] + self.epsilon

    def getCenter(self):
        middle_point = map(add,self.rect[0],self.rect[1])
        return [coord/2 for coord in middle_point]

    def getRadius(self):
        return (self.rect[1][0]-self.rect[0][0])/2.

    def draw(self):
        width = self.rect[1][0] - self.rect[0][0]
        height = self.rect[1][1] - self.rect[0][1]

        bottom_left_c = self.rect[0]
        top_left_c = map(add,bottom_left_c,[0,height])
        top_right_c = self.rect[1]
        bottom_right_c = map(add,bottom_left_c,[width,0])

        #window_size = (glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        window_size = (1024,800)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, window_size[0], 0.0, window_size[1], -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()

        glLoadIdentity()

        glColor3f(1.0,0.0,0.0)

        glBegin(GL_POLYGON)
        glVertex2f(*bottom_left_c)
        glVertex2f(*top_left_c)
        glVertex2f(*top_right_c)
        glVertex2f(*bottom_right_c)
        glEnd()

        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

        glMatrixMode(GL_MODELVIEW)
