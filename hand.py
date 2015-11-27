import OpenGL
OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from constants import *
import primitives
import Leap

class Finger:
    def __init__(self, finger, color, iBox):
        self.color = color
        self.phalanxes = []
        self.knuckles = []

        for i in range(1,3):
            bone_tip = self.leap_to_world(finger.bone(i).next_joint, iBox)
            bone_base= self.leap_to_world(finger.bone(i+1).next_joint, iBox)

            line = primitives.Line([bone_tip, bone_base], self.color)
            ball_ = primitives.Ball(self.color,finger.bone(i).width/4,bone_tip)

            self.phalanxes.append(line)
            self.knuckles.append(ball_)

        ball_ = primitives.Ball(self.color,finger.bone(3).width/4,self.leap_to_world(finger.bone(3).next_joint, iBox))
        self.knuckles.append(ball_)

    def leap_to_world(self, leap_point, iBox):
	    leap_point.z *= 1.0; #right-hand to left-hand rule
	    normalized = iBox.normalize_point(leap_point, False)
	    normalized = normalized #+ Leap.Vector(-0.5, 0, -0.5); #recenter origin
	    return normalized * 200; #scale

    def draw(self):
        for knuckle in self.knuckles:
            knuckle.draw()
        for phalanx in self.phalanxes:
            phalanx.draw()


class Hand:
    def __init__(self, hand, color):
        self.color = color
        self.setHand(hand)

    def __init__(self):
        self.hand = None
        self.color = steel_red
        self.fingers = []

    def setHand(self,hand,iBox):
        self.hand = hand
        self.fingers = []
        self.iBox = iBox

        for finger in hand.fingers:
            draw_finger = Finger(finger,self.color,self.iBox)
            self.fingers.append(draw_finger)

    def get2DwindowPosition(self):
        window_size = (glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        app_width = window_size[0]
        app_height = window_size[1]

        leapPoint = self.hand.palm_position
        normalizedPoint = self.iBox.normalize_point(leapPoint, False)

        app_x = normalizedPoint.x * app_width
        app_y = (1 - normalizedPoint.z) * app_height

        return([app_x,app_y])

    def draw(self):
        glPushMatrix()
        glTranslatef(self.hand.palm_position[0], self.hand.palm_position[1], self.hand.palm_position[2])
        glScalef(0.5, 0.5, 0.5)
        for finger in self.fingers:
            finger.draw()
        glTranslatef(-self.hand.palm_position[0], -self.hand.palm_position[1], -self.hand.palm_position[2])
        glPopMatrix()
