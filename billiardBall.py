from primitives import Ball, Quad
from constants import *

import math
from operator import add, sub

from shapely.geometry import LineString, Point

# Calculates the distance of two positions
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

# Calculates the product of two vectors
def dotProduct(p,q):
    return sum([p[i]*q[i] for i in range(3)])

# Calculates the squared norm
def squaredNorm(p):
    return dotProduct(p,p)

# Calculates the polar coordinates
def toPolar(pos):
    module = math.sqrt(sum([pos[i]**2 for i in range(2)]))
    angle = math.atan2(pos[1], pos[0])
    return [module,angle]

class BilliardBall(Ball):
    def __init__(self, coord=[0.0,0.0], vel=[0.0,0.0], b_type=BBallType.whitey, color=steel_red):
        self.vel = [vel[0], 0.0, vel[1]]
        self.type = b_type

        self.frame_tick = 0
        self.highlighted = False

        self.first_radius = self.radius = BALL_RADIUS

        if self.type == BBallType.whitey:
            self.first_radius = self.radius = BALL_RADIUS*0.9
            color = steel_white
        elif self.type == BBallType.black:
            color = black

        self.coord = [coord[0], BALL_RADIUS, coord[1]]

        Ball.__init__(self, color, self.radius, self.coord)

    # Updates ball position attending to the friction
    def updatePos(self):
        self.vel = [self.vel[i]*COF for i in range(3)]
        self.coord = map(add,self.coord,self.vel)

    # Changes velocity to polar coordinates
    def velToPolar(self):
        return toPolar([self.vel[0],self.vel[2]])

    # Changes position to polar coordinates
    def posToPolar(self):
        return toPolar([self.pos[0],self.pos[2]])

    # Provides the state of the ball (Moving = True)
    def isMoving(self):
        vel_module = self.velToPolar()[0]
        return vel_module > 0.

    # Calculates if its ball is colliding with other ball
    def collide(self, other_ball):
        # Present and future positions of both balls
        p1 = (self.coord[0], self.coord[2])
        q1 = (self.coord[0] + COF*self.vel[0], self.coord[2] + COF*self.vel[2])

        p2 = (other_ball.coord[0], other_ball.coord[2])
        q2 = (other_ball.coord[0] + COF*other_ball.vel[0], other_ball.coord[2] + COF*other_ball.vel[2])

        # Both balls are moving
        if self.isMoving() and other_ball.isMoving():
            segment1 = LineString([p1,q1])
            segment2 = LineString([p2,q2])
            return segment1.distance(segment2) <= self.radius+other_ball.radius

        # Only this ball is moving
        elif self.isMoving():
            segment1 = LineString([p1,q1])
            return segment1.distance(Point(p2)) <= self.radius+other_ball.radius

        #Only the other ball is moving
        elif other_ball.isMoving():
            segment2 = LineString([p2,q2])
            return segment2.distance(Point(p1)) <= self.radius+other_ball.radius

        return False

    # Changes the velocity of two balls attending their director vectors and velocities
    def ellasticCollisionUpdate(self, other_ball):
        #self.vel, other_ball.vel = COF*other_ball.vel, COF*self.vel
        # Velocity of both balls
        v1 = self.vel
        v2 = other_ball.vel

        # Position of both balls
        x1 = self.coord
        x2 = other_ball.coord

        x1_x2 = map(sub,x1,x2)
        x2_x1 = map(sub,x2,x1)

        v1_v2 = map(sub,v1,v2)
        v2_v1 = map(sub,v2,v1)

        diff_1 = [dotProduct(v1_v2, x1_x2) / squaredNorm(x1_x2) * x1_x2[i] for i in range(3)]
        diff_2 = [dotProduct(v2_v1, x2_x1) / squaredNorm(x2_x1) * x2_x1[i] for i in range(3)]

        self.vel        = map(sub,v1,diff_1)
        other_ball.vel  = map(sub,v2,diff_2)

    def activateHighlight(self):
        self.highlighted = True

    def deactivateHighlight(self):
        self.radius = self.first_radius

    # Creates the effect of highlight in the ball
    def highlight(self):
        if self.highlighted:
            self.frame_tick = (self.frame_tick + 5)%360
            radian_tick = self.frame_tick / 360.0  * 2 * math.pi
            self.radius = self.radius + 0.3*math.sin(radian_tick)

class BilliardTable:
    def __init__(self, width=450, length=300, height=2*BALL_RADIUS, center = [0.0, 0.0, 0.0]):
        self.width = width
        self.length = length
        self.height = height

        half_width = self.width/2.
        half_length = self.length/2.

        top_left_corner     = [center[0] - half_width, -0.01, center[0] + half_length]
        top_right_corner    = [center[0] + half_width, -0.01, center[0] + half_length]
        bottom_right_corner = [center[0] + half_width, -0.01, center[0] - half_length]
        bottom_left_corner  = [center[0] - half_width, -0.01, center[0] - half_length]

        self.corners = [top_left_corner, bottom_left_corner, bottom_right_corner, top_right_corner]

        self.table = Quad(self.corners, billiard_green)

    # Calculates the balls collisions with the table
    def wallCollisionUpdate(self,ball):
        speed_module = ball.velToPolar()[0]
        dist_x = self.width/2.  - abs(ball.coord[0])
        dist_y = self.length/2. - abs(ball.coord[2])

        if dist_x <= ball.radius:
            ball.vel[0] = -ball.vel[0]
        if dist_y <= ball.radius:
            ball.vel[2] = -ball.vel[2]

    def isBallInPocket(self,ball):
        if ball.type is not BBallType.whitey and ball.type is not BBallType.black:
            for corner in self.corners:
                if distance(ball.coord,corner) <= 2*ball.radius:
                    return True
        return False


    def draw(self):
        self.table.draw()
