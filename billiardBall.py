from primitives import Ball, Quad
from constants import *

import math
from operator import add

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

def crossProduct(v,w):
    return v[0]*w[2] + v[2]*w[0]

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
            color=steel_white
        if self.type == BBallType.black:
            color = black

        self.coord = [coord[0], self.radius, coord[1]]

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
        return vel_module > 0

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
            print("HOLA")
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
    def collide(self, other_ball):
        p = self.coord
        q = other_ball.coord

        pq = [q[i] - p[i] for i in range(3)]

        # Predict position in the next frame
        r = self.vel
        s = other_ball.vel

        if crossProduct(r,s) != 0:
            t = crossProduct(pq,s) / crossProduct(r,s)
            u = crossProduct(pq,r) / crossProduct(r,s)
            return 0 <= t <= 1 and 0 <= u <= 1
        elif crossProduct(pq,r) != 0:
            return False
        else:
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

    def ellasticCollisionUpdate(self, other_ball):
        polar_vel_1 = self.velToPolar()
        polar_vel_2 = other_ball.velToPolar()

        collision_angle = self.collisionAngle(other_ball)

        new_vel_1_x = polar_vel_2[0] * math.cos(polar_vel_2[1]-collision_angle) * math.cos(collision_angle) + polar_vel_1[0] * math.sin(polar_vel_1[1]-collision_angle) * math.cos(collision_angle + math.pi/2)

        new_vel_1_y = polar_vel_2[0] * math.cos(polar_vel_2[1]-collision_angle) * math.sin(collision_angle) + polar_vel_1[0] * math.sin(polar_vel_1[1]-collision_angle) * math.sin(collision_angle + math.pi/2)

        new_vel_2_x = polar_vel_1[0] * math.cos(polar_vel_1[1]-collision_angle) * math.cos(collision_angle) + polar_vel_2[0] * math.sin(polar_vel_2[1]-collision_angle) * math.cos(collision_angle + math.pi/2)

        new_vel_2_y = polar_vel_1[0] * math.cos(polar_vel_1[1]-collision_angle) * math.sin(collision_angle) + polar_vel_2[0] * math.sin(polar_vel_2[1]-collision_angle) * math.sin(collision_angle + math.pi/2)

        self.vel        = [new_vel_1_x, 0.0, new_vel_1_y]
        other_ball.vel  = [new_vel_2_x, 0.0, new_vel_2_y]

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
