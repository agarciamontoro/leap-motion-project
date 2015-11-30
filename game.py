import primitives
from billiard import BilliardBall, BilliardTable
from constants import *

import Leap, time, sys

import leapDriver
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

def setBallsToColors(color_1, color_2):
    for ball in b_balls:
        if ball.type is not BBallType.whitey and ball.type is not BBallType.black:
            if ball.type is BBallType.striped:
                ball.color = color_1
            else:
                ball.color = color_2

def setBallsToRedGreen():
    setBallsToColors(steel_red, steel_green)

def setBallsToOrangeYellow():
    setBallsToColors(steel_orange, steel_yellow)

def setHandToRed():
    for hand in draw_hands:
        hand.color = steel_rer

def setHandToGreen():
    for hand in draw_hands:
        hand.color = steel_green

def disableMenu():
    menu.disable()

def quitGame():
    print("Bye!")
    sys.exit()

# Initializes the game
def initGame(listener):
    global leap, last_data_time, tutorial, b_table, b_whitey, b_balls, loader, force_line, shoot_mode, prev_num_hands, menu, start_screen, option_screen

    leap = listener
    last_data_time = [time.time(), time.time()]

    b_table = BilliardTable()

    #height = sqrt( ((BALL_RADIUS*2)**2 + BALL_RADIUS**2))
    height = 22.36
    # The start of the triangle of balls
    triEdge = 60
    corrector = 0.1

    # All the balls in the pool
    b_whitey   = BilliardBall([triEdge,0],[0.0,0.0], BBallType.whitey)
    # First row
    striped_9  = BilliardBall([-triEdge,0],[0.0,0.0], BBallType.striped, steel_red)
    # Second row
    solid_7    = BilliardBall([-(triEdge+height),-(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.solid, steel_yellow)
    striped_12 = BilliardBall([-(triEdge+height),(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.striped, steel_red)
    # Third row
    striped_15 = BilliardBall([-(triEdge+2*height),-(corrector+BALL_RADIUS*2)],[0.0,0.0], BBallType.striped, steel_red)
    b_black    = BilliardBall([-(triEdge+2*height),0],[0.0,0.0], BBallType.black)
    solid_1    = BilliardBall([-(triEdge+2*height),(corrector+BALL_RADIUS*2)],[0.0,0.0], BBallType.solid, steel_orange)
    # Fourth row
    solid_6    = BilliardBall([-(triEdge+3*height),-(corrector+BALL_RADIUS*3)],[0.0,0.0], BBallType.solid, steel_yellow)
    striped_10 = BilliardBall([-(triEdge+3*height),-(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.striped, steel_yellow)
    solid_3    = BilliardBall([-(triEdge+3*height),(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.solid, black)
    striped_14 = BilliardBall([-(triEdge+3*height),(corrector+BALL_RADIUS*3)],[0.0,0.0], BBallType.striped, steel_red)
    # Fifth row
    striped_11 = BilliardBall([-(triEdge+4*height),-(corrector+BALL_RADIUS*4)],[0.0,0.0], BBallType.striped, steel_orange)
    solid_2    = BilliardBall([-(triEdge+4*height),-(corrector+BALL_RADIUS*2)],[0.0,0.0], BBallType.solid, steel_green)
    striped_13 = BilliardBall([-(triEdge+4*height),0],[0.0,0.0], BBallType.striped, steel_red)
    solid_4    = BilliardBall([-(triEdge+4*height),(corrector+BALL_RADIUS*2)],[0.0,0.0], BBallType.solid, steel_yellow)
    solid_5    = BilliardBall([-(triEdge+4*height),(corrector+BALL_RADIUS*4)],[0.0,0.0], BBallType.solid, steel_yellow)

    b_balls = [striped_9, striped_10, striped_11, striped_12, striped_13, striped_14, striped_15, solid_1, solid_2, solid_3, solid_4, solid_5, solid_6, solid_7, b_whitey, b_black]
    #b_balls = [striped_1, striped_2, solid_1, solid_2, b_whitey, b_black]

    # Creates and activate the loader
    loader = primitives.Loader([200.0,200.0])
    loader.activate()
    force_line = ForceLine(b_whitey)

    shoot_mode = False

    prev_num_hands = 0

    #Screens
    start_screen = Screen("./Screenshots/menu01_start.png")#, [to_opt_button, quit_menu_button, quit_game_button])
    general_opt_screen = Screen("./Screenshots/menu02_options.png")#, [to_ball_opt_button, to_hand_opt_button, back_to_first_button])
    ball_opt_screen = Screen("./Screenshots/menu03_balls.png")#, [red_ball_button, orange_ball_button, back_to_opt_button])
    hand_opt_screen = Screen("./Screenshots/menu04_hands.png")#, [red_hand_button, green_hand_button, back_to_opt_button])

    #First screen buttons
    to_opt_button = NavigationalButton([[1024-977,800-475],[1024-559,800-57]], general_opt_screen)
    quit_menu_button = ActionButton([[1024-465,800-475],[1024-47,800-57]], disableMenu)
    quit_game_button = ActionButton([[1024-661,800-749],[1024-363,800-451]], quitGame)

    #General options screen buttons
    to_ball_opt_button = NavigationalButton([[1024-977,800-475],[1024-559,800-57]], ball_opt_screen)
    to_hand_opt_button = NavigationalButton([[1024-465,800-475],[1024-47,800-57]], hand_opt_screen)
    back_to_first_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], start_screen)

    #Ball options screen buttons
    orange_ball_button = ActionButton([[1024-977,800-475],[1024-559,800-57]], setBallsToOrangeYellow)
    red_ball_button = ActionButton([[1024-465,800-475],[1024-47,800-57]], setBallsToRedGreen)
    back_to_opt_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], general_opt_screen)

    #Hand options screen buttons
    red_hand_button = ActionButton([[1024-977,800-475],[1024-559,800-57]], setHandToRed)
    green_hand_button = ActionButton([[1024-465,800-475],[1024-47,800-57]], setHandToGreen)

    start_screen.buttons = [to_opt_button, quit_menu_button, quit_game_button]
    general_opt_screen.buttons = [to_ball_opt_button, to_hand_opt_button, back_to_first_button]
    ball_opt_screen.buttons = [red_ball_button, orange_ball_button, back_to_opt_button]
    hand_opt_screen.buttons = [red_hand_button, green_hand_button, back_to_opt_button]

    menu = Menu(start_screen,loader)

# Panacea method
def processFrame():
    global shoot_mode, force, prev_num_hands

    new_frame, hands, iBox = leap.getHands()
    objects = [menu, b_table]

    if sum(new_frame) == 2 and prev_num_hands == 1:
        menu.swap()
    prev_num_hands = sum(new_frame)

    # If the menu is not enabled.
    # Let the pool begins! And may the odds be ever in your favor.
    if not menu.enabled:
        for is_new, hand, draw_hand, prev_time in zip(new_frame, hands, draw_hands, last_data_time):
            if is_new:
                # If OK, activates the shoot mode
                if gestures.isGestureOK(hand):
                    shoot_mode = True
                    hand_pos = [hand.palm_position[j] for j in range(3)]

                    # Stablish the Origin and End of the force line
                    force_line.setBall(b_whitey)
                    force_line.setOrigin(hand_pos)

                    # Force of shoot
                    force = force_line.getForce()
                    objects.append(force_line)
                elif shoot_mode:
                    shoot_mode = False
                    # The white ball continues her way
                    b_whitey.vel = force

                draw_hand.setHand(hand,iBox)
                objects.append(draw_hand)
                prev_time = time.time()
            elif time.time() - prev_time < time_margin:
                objects.append(draw_hand)

        b_balls[:] = [ball for ball in b_balls if not b_table.isBallInPocket(ball)]

        # Calculates all the collisions of all the balls with all the balls
        for ball, other_ball in itertools.combinations(b_balls,2):
            if ball.collide(other_ball):
                ball.ellasticCollisionUpdate(other_ball)

        # Calculates all the collisions of all the balls with the walls
        for ball in b_balls:
            b_table.wallCollisionUpdate(ball)
            ball.updatePos()

        objects += b_balls
    else:
        # Pause the game!
        for is_new, hand, draw_hand in zip(new_frame, hands, draw_hands):
            if is_new and hand.is_right:
                draw_hand.setHand(hand,iBox)
                pointer = draw_hand.get2DwindowPosition()
                menu.process(pointer)

    return objects
