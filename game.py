import primitives
from billiardBall import BilliardBall, BilliardTable
from constants import *

import Leap, time

import LeapDriver
import hand
import gestures
from forceLine import ForceLine
from menu import Menu, Screen, ActionButton, NavigationalButton

import itertools

draw_hands = [hand.Hand(), hand.Hand()]
last_data_time = [0,0]
time_margin = 0.07

# Distance
def distance(pos1,pos2):
    return math.sqrt(sum([(pos2[i]-pos1[i])**2 for i in range(3)]))

def doubleRadius():
    print("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY")

def initGame(listener):
    global leap, last_data_time, tutorial, b_table, b_whitey, b_balls, loader, force_line, shoot_mode, prev_num_hands, menu, start_screen, option_screen

    leap = listener
    last_data_time = [time.time(), time.time()]

    b_table = BilliardTable()

    striped_9 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_red)
    striped_10 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_yellow)
    striped_11 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_orange)
    striped_12 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_red)
    striped_13 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_red)
    striped_14 = BilliardBall([0,0],[0.0,0.0], BBallType.striped, steel_red)
    striped_15 = BilliardBall([-100,-20.1],[0.0,0.0], BBallType.striped, steel_red)

    solid_1   = BilliardBall([-100,20.1],[0.0,0.0], BBallType.solid, steel_orange)
    solid_2   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, steel_green)
    solid_3   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, black)
    solid_4   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, steel_yellow)
    solid_5   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, steel_yellow)
    solid_6   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, steel_yellow)
    solid_7   = BilliardBall([0,0],[0.0,0.0], BBallType.solid, steel_yellow)

    b_whitey    = BilliardBall([0,60],[0.0,0.0], BBallType.whitey)
    b_black     = BilliardBall([-100,0],[0.0,0.0], BBallType.black)

    b_balls = [striped_9, striped_10, striped_11, striped_12, striped_13, striped_14, striped_15, solid_1, solid_2, solid_3, solid_4, solid_5, solid_6, solid_7, b_whitey, b_black]
    #b_balls = [striped_1, striped_2, solid_1, solid_2, b_whitey, b_black]

    loader = primitives.Loader([200.0,200.0])
    loader.activate()
    force_line = ForceLine(b_whitey)

    shoot_mode = False

    prev_num_hands = 0

    option_button = ActionButton([[110,120],[160,170]], doubleRadius)
    option_screen = Screen("./Screenshots/02.png", [option_button])

    navigate_button = NavigationalButton([[10,20], [60,70]], option_screen)

    start_screen = Screen("./Screenshots/01.png", [navigate_button])

    menu = Menu(start_screen,loader)

def processFrame():
    global shoot_mode, force, prev_num_hands

    new_frame, hands, iBox = leap.getHands()
    objects = [menu, b_table]

    if sum(new_frame) == 2 and prev_num_hands == 1:
        menu.swap()
    prev_num_hands = sum(new_frame)

    if not menu.enabled:
        for is_new, hand, draw_hand, prev_time in zip(new_frame, hands, draw_hands, last_data_time):
            if is_new:
                if gestures.isGestureOK(hand):
                    shoot_mode = True
                    hand_pos = [hand.palm_position[j] for j in range(3)]

                    force_line.setBall(b_whitey)
                    force_line.setOrigin(hand_pos)

                    force = force_line.getForce()
                    objects.append(force_line)
                elif shoot_mode:
                    shoot_mode = False
                    b_whitey.vel = force

                draw_hand.setHand(hand,iBox)
                objects.append(draw_hand)
                prev_time = time.time()
            elif time.time() - prev_time < time_margin:
                objects.append(draw_hand)

        for ball, other_ball in itertools.combinations(b_balls,2):
            if ball.collide(other_ball):
                ball.ellasticCollisionUpdate(other_ball)

        for ball in b_balls:
            b_table.wallCollisionUpdate(ball)
            ball.updatePos()

        objects += b_balls
    else:
        for is_new, hand, draw_hand in zip(new_frame, hands, draw_hands):
            if is_new and hand.is_right:
                draw_hand.setHand(hand,iBox)
                pointer = draw_hand.get2DwindowPosition()
                menu.process(pointer)

    return objects
