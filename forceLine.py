from primitives import Line
from billiardBall import *

import math

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

class ForceLine(Line):
    def __init__(self, ball, pos = [0.0, 0.0, 0.0]):
        self.points = [ball.coord, pos]
        self.intensity = self.getIntensity()
        self.color = [self.intensity, 1.0, 0.0]

        Line.__init__(self, self.points, self.color)

    # Provides the force intensity
    def getIntensity(self):
        dist = distance(*self.points)/200.0
        intensity = 1.0 if dist > 1.0 else dist
        return intensity

    # Changes the color of the line attending to the intensity
    def setColor(self):
        self.intensity = self.getIntensity()
        self.color[0] = self.intensity

    # Stablishs the ball point for the force line
    def setBall(self, ball):
        self.points[0] = ball.coord
        self.setColor()

    # Stablish the hand point for the force line
    def setOrigin(self, pos):
        self.points[1] = pos
        self.points[1][1] = self.points[0][1]
        self.setColor()

    # Obtains the force vector
    def getForce(self):
        dir_vector = self.getDirVector()
        force = [FORCE_CONSTANT * self.intensity * dir_vector[i] for i in range(3)]
        # Only working with 2D forces
        force[1] = 0.0
        return force
