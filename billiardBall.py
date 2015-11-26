from primitives import Ball, Quad
from constants import *

import math
from operator import add, sub

from shapely.geometry import LineString, Point

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

def crossProduct(v,w):
    return v[0]*w[2] + v[2]*w[0]

def dotProduct(p,q):
    return sum([p[i]*q[i] for i in range(3)])

def squaredNorm(p):
    return dotProduct(p,p)

def orientation(p, q, r):
    # See 10th slides from following link for derivation of the formula
    # http://www.dcs.gla.ac.uk/~pat/52233/slides/Geometry1x1.pdf
    val = (q[2] - p[2]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[2] - q[2])

    if val == 0:
        return 0  # colinear

    return 1 if val > 0 else 2 # clock or counterclock wise

def doBoundingBoxesIntersect(p1,q1,p2,q2):
    return p1[0] <= q2[0] and q1[0] >= p2[0] and p1[2] <= q2[2] and q1[2] >= p2[2]

def onSegment(p, q, r):
    if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[2] <= max(p[2], r[2]) and q[2] >= min(p[2], r[2]):
       return True

    return False

def segmentIntersection(p1,q1,p2,q2):
    # Find the four orientations needed for general and
    # special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special Cases
    # p1, q1 and p2 are colinear and p2 lies on segment p1q1
    if o1 == 0 and onSegment(p1, p2, q1):
        return True

    # p1, q1 and p2 are colinear and q2 lies on segment p1q1
    if o2 == 0 and onSegment(p1, q2, q1):
        return True

    # p2, q2 and p1 are colinear and p1 lies on segment p2q2
    if o3 == 0 and onSegment(p2, p1, q2):
        return True

    # p2, q2 and q1 are colinear and q1 lies on segment p2q2
    if o4 == 0 and onSegment(p2, q1, q2):
        return True

    return False # Doesn't fall in any of the above cases


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

    def updatePos(self):
        self.vel = [self.vel[i]*COF for i in range(3)]
        self.coord = map(add,self.coord,self.vel)

    def velToPolar(self):
        return toPolar([self.vel[0],self.vel[2]])

    def posToPolar(self):
        return toPolar([self.pos[0],self.pos[2]])

    def isMoving(self):
        vel_module = self.velToPolar()[0]
        return vel_module > 0.

    def isMovingToBall(self,other_ball):
        x_dir = (other_ball.coord[0] - self.coord[0]) * (self.vel[0] - other_ball.vel[0])
        y_dir = (other_ball.coord[2] - self.coord[2]) * (self.vel[2] - other_ball.vel[2])
        return x_dir + y_dir > 0

    def collide_old(self, other_ball):
        self_speed  = self.velToPolar()[0]
        other_speed = other_ball.velToPolar()[0]
        sum_speed = self_speed + other_speed

        dist = distance(self.coord, other_ball.coord) - (self.radius+other_ball.radius)

        if self.isMovingToBall(other_ball) and sum_speed != 0 and 0 < dist / sum_speed <= 1:
            return True

        return distance(self.coord, other_ball.coord) <= self.radius+other_ball.radius

    def collide_semiold(self, other_ball):
        if self.isMovingToBall(other_ball):
            A = self.vel[0] ** 2 + self.vel[2] ** 2 - 2 * self.vel[0] * other_ball.vel[0] + other_ball.vel[0] ** 2 - 2 * self.vel[2] * other_ball.vel[2] + other_ball.vel[2] ** 2
            B = -self.coord[0] * self.vel[0] - self.coord[2] * self.vel[2] + self.vel[0] * other_ball.coord[0] + self.vel[2] * other_ball.coord[2] + self.coord[0] * other_ball.vel[0] - other_ball.coord[0] * other_ball.vel[0] + self.coord[2] * other_ball.vel[2] - other_ball.coord[2] * other_ball.vel[2]
            C = self.vel[0] ** 2 + self.vel[2] ** 2 - 2 * self.vel[0] * other_ball.vel[0] + other_ball.vel[0] ** 2 - 2 * self.vel[2] * other_ball.vel[2] + other_ball.vel[2] ** 2
            D = self.coord[0] ** 2 + self.coord[2] ** 2 - self.radius ** 2 - 2 * self.coord[0] * other_ball.coord[0] + other_ball.coord[0] ** 2 - 2 * self.coord[2] * other_ball.coord[2] + other_ball.coord[2] ** 2 - 2 * self.radius * other_ball.radius - other_ball.radius ** 2

            discriminant = (-2 * B) ** 2 - 4 * C * D

            if discriminant >= 0:
                t = min(0.5 * (2. * B - math.sqrt(discriminant)) / A, 0.5 * (2. * B + math.sqrt(discriminant)) / A)
                return t <= 1

            return False


    # From http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    def collide_semi_semiold(self, other_ball):
        self_vel_mod = self.velToPolar()[0]
        other_vel_mod= other_ball.velToPolar()[0]

        if self_vel_mod != 0 and other_vel_mod != 0:
            p1 = self.coord
            q1 = map(add,p1,[COF*self.vel[i] for i in range(3)])

            p2 = other_ball.coord
            q2 = map(add,p2,[COF*other_ball.vel[i] for i in range(3)])

            print(p1,q1)
            print(p2,q2)

            return segmentIntersection(p1,q1,p2,q2)
        elif self_vel_mod != 0:
            dist = distance(self.coord, other_ball.coord) - (self.radius+other_ball.radius)
            if self.isMovingToBall(other_ball) and 0 < dist / self_vel_mod <= 1:
                return True
        elif other_vel_mod != 0:
            dist = distance(self.coord, other_ball.coord) - (self.radius+other_ball.radius)
            if other_ball.isMovingToBall(self) and 0 < dist / other_vel_mod <= 1:
                return True

        return False

    def collide_sss_old(self, other_ball):
        self_vel_mod = self.velToPolar()[0]
        other_vel_mod= other_ball.velToPolar()[0]

        # if distance(self.coord, other_ball.coord) <= self.radius+other_ball.radius:
        #     return True

        if self_vel_mod != 0 and other_vel_mod != 0:
            p1 = self.coord
            q1 = map(add,p1,[self.vel[i] for i in range(3)])

            p2 = other_ball.coord
            q2 = map(add,p2,[other_ball.vel[i] for i in range(3)])

            segment1 = LineString([(p1[0],p1[2]), (q1[0],q1[1])])
            segment2 = LineString([(p2[0],p2[2]), (q2[0],q2[1])])

            return not segment1.intersection(segment2).is_empty
        elif self_vel_mod != 0:
            dist = distance(self.coord, other_ball.coord) - (self.radius+other_ball.radius)
            if self.isMovingToBall(other_ball) and 0 < dist / self_vel_mod <= 1:
                return True
        elif other_vel_mod != 0:
            dist = distance(self.coord, other_ball.coord) - (self.radius+other_ball.radius)
            if other_ball.isMovingToBall(self) and 0 < dist / other_vel_mod <= 1:
                return True

        return False

    def collide(self, other_ball):
        p1 = (self.coord[0], self.coord[2])
        q1 = (self.coord[0] + COF*self.vel[0], self.coord[2] + COF*self.vel[2])

        p2 = (other_ball.coord[0], other_ball.coord[2])
        q2 = (other_ball.coord[0] + COF*other_ball.vel[0], other_ball.coord[2] + COF*other_ball.vel[2])

        if self.isMoving() and other_ball.isMoving():
            segment1 = LineString([p1,q1])
            segment2 = LineString([p2,q2])
            print(list(segment1.coords),list(segment2.coords))
            return segment1.distance(segment2) <= self.radius+other_ball.radius

        elif self.isMoving():
            segment1 = LineString([p1,q1])
            return segment1.distance(Point(p2)) <= self.radius+other_ball.radius

        elif other_ball.isMoving():
            segment2 = LineString([p2,q2])
            return segment2.distance(Point(p1)) <= self.radius+other_ball.radius

        return False

    # def tableCollision(self, table):
    #     if table.collision(self) == VERTICAL:
    #         self.vel[0] = -self.vel[0]
    #     else:
    #         self.vel[2] = -self.vel[1]

    def collisionPoint(self, other_ball):
        return [(self.coord[i]+other_ball.coord[i])/2 for i in range(3)]

    def collisionAngle(self, other_ball):
        collision_pt = self.collisionPoint(other_ball)
        polar_collision_point = toPolar([collision_pt[0], collision_pt[2]])
        return polar_collision_point[1]

    def ellasticCollisionUpdate_old(self, other_ball):
        polar_vel_1 = self.velToPolar()
        polar_vel_2 = other_ball.velToPolar()

        collision_angle = self.collisionAngle(other_ball)

        new_vel_1_x = polar_vel_2[0] * math.cos(polar_vel_2[1]-collision_angle) * math.cos(collision_angle) + polar_vel_1[0] * math.sin(polar_vel_1[1]-collision_angle) * math.cos(collision_angle + math.pi/2)

        new_vel_1_y = polar_vel_2[0] * math.cos(polar_vel_2[1]-collision_angle) * math.sin(collision_angle) + polar_vel_1[0] * math.sin(polar_vel_1[1]-collision_angle) * math.sin(collision_angle + math.pi/2)

        new_vel_2_x = polar_vel_1[0] * math.cos(polar_vel_1[1]-collision_angle) * math.cos(collision_angle) + polar_vel_2[0] * math.sin(polar_vel_2[1]-collision_angle) * math.cos(collision_angle + math.pi/2)

        new_vel_2_y = polar_vel_1[0] * math.cos(polar_vel_1[1]-collision_angle) * math.sin(collision_angle) + polar_vel_2[0] * math.sin(polar_vel_2[1]-collision_angle) * math.sin(collision_angle + math.pi/2)

        self.vel        = [new_vel_1_x, 0.0, new_vel_1_y]
        other_ball.vel  = [new_vel_2_x, 0.0, new_vel_2_y]

    def ellasticCollisionUpdate(self, other_ball):
        #self.vel, other_ball.vel = COF*other_ball.vel, COF*self.vel
        v1 = self.vel
        v2 = other_ball.vel

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

    def highlight(self):
        if self.highlighted:
            self.frame_tick = (self.frame_tick + 5)%360
            radian_tick = self.frame_tick / 360.0  * 2 * math.pi
            self.radius = self.radius + 0.3*math.sin(radian_tick)

class BilliardTable:
    def __init__(self, width=200, length=120, height=2*BALL_RADIUS, center = [0.0, 0.0, 0.0]):
        self.width = width
        self.length = length
        self.height = height

        half_width = self.width/2.
        half_length = self.length/2.

        top_left_corner     = [center[0] - half_width, -0.01, center[0] + half_length]
        top_right_corner    = [center[0] + half_width, -0.01, center[0] + half_length]
        bottom_right_corner = [center[0] + half_width, -0.01, center[0] - half_length]
        bottom_left_corner  = [center[0] - half_width, -0.01, center[0] - half_length]

        corners = [top_left_corner, bottom_left_corner, bottom_right_corner, top_right_corner]

        self.table = Quad(corners, billiard_green)

    def wallCollisionUpdate(self,ball):
        speed_module = ball.velToPolar()[0]
        dist_x = self.width/2.  - abs(ball.coord[0])
        dist_y = self.length/2. - abs(ball.coord[2])

        if dist_x <= ball.radius:
            ball.vel[0] = -ball.vel[0]
        if dist_y <= ball.radius:
            ball.vel[2] = -ball.vel[2]


    def draw(self):
        self.table.draw()
