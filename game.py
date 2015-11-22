import primitives
from billiardBall import BilliardBall
from constants import *

import Leap, time

import LeapDriver
import hand

import itertools

draw_hand = [hand.Hand(), hand.Hand()]
last_data_time = [0,0]
time_margin = 0.07

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

def initGame(listener):
    global leap, last_data_time, tutorial, b_balls

    leap = listener
    last_data_time = [time.time(), time.time()]
    tutorial = primitives.Image("./Screenshots/01.png")

    b_ball_1 = BilliardBall([100,0],[0.0,0.0], steel_red)
    b_ball_2 = BilliardBall([-500,0],[10.0,0.0], steel_yellow)
    b_ball_3 = BilliardBall([300,25],[0.0,0.0], steel_white)

    b_balls = [b_ball_1, b_ball_2, b_ball_3]

def processFrame():
    #new_frame, hands = leap.getHands()

    # ball_1 = primitives.Ball(steel_yellow, 75, [0.0,125.0,-50.0])
    # ball_2 = primitives.Ball(steel_red, 50, [0.0,125.0,-100.0])
    # ball_3 = primitives.Ball(steel_white, 25, [0.0,125.0,-137.5])
    #
    #
    #
    # objects = []
    #
    # objects.append(ball_1)
    # objects.append(ball_2)
    # objects.append(ball_3)

    # for i in range(2):
    #     if new_frame[i]:
    #         draw_hand[i].setHand(hands[i])
    #         objects.append(draw_hand[i])
    #         last_data_time[i] = time.time()
    #         print("New frame: ",i)
    #     elif time.time() - last_data_time[i] < time_margin:
    #         objects.append(draw_hand[i])
    #         print("Not new frame: ",i)

    # # Test the image object: shows the tutorial image for the first five seconds
    # if time.time() - last_data_time[0] < 5:
    #     objects.append(tutorial)

    for ball, other_ball in itertools.combinations(b_balls,2):
        if ball.collide(other_ball):
            if not ball.isMoving():
                print("BALL PARADA")
                other_ball.ellasticCollisionUpdate_rest(ball)
            elif not other_ball.isMoving():
                print("OTHER_BALL PARADA")
                ball.ellasticCollisionUpdate_rest(other_ball)
            else:
                print("NINGUNA BALL PARADA")
                ball.ellasticCollisionUpdate(other_ball)
        ball.updatePos()
        other_ball.updatePos()

    objects = b_balls

    return objects
