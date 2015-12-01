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

def disableTutorial():
    tutorial.disable()

def disableMenu():
    menu.disable()

def quitGame():
    print("Bye!")
    sys.exit()

def processMenu(menu_object, new_frame, hands, draw_hands, iBox):
    for is_new, hand, draw_hand in zip(new_frame, hands, draw_hands):
        if is_new and hand.is_right:
            draw_hand.setHand(hand,iBox)
            pointer = draw_hand.get2DwindowPosition()
            menu_object.process(pointer)
    return menu_object

# Initializes the game
def initGame(listener):
    global leap, last_data_time, tutorial, b_table, b_whitey, b_balls, force_line, shoot_mode, prev_num_hands, menu

    leap = listener
    last_data_time = [time.time(), time.time()]

    b_table = BilliardTable()

    #height = sqrt( ((BALL_RADIUS*2)**2 + BALL_RADIUS**2))
    height = 22.36
    # The start of the triangle of balls
    triEdge = 60
    corrector = 1.0

    # All the balls in the pool
    b_whitey   = BilliardBall([triEdge,0],[0.0,0.0], BBallType.whitey)
    # First row
    striped_9  = BilliardBall([-triEdge,0],[0.0,0.0], BBallType.striped, steel_red)
    # Second row
    solid_7    = BilliardBall([-(triEdge+height),-(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.solid, steel_yellow)
    striped_12 = BilliardBall([-(triEdge+height),(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.striped, steel_red)
    # Third row
    striped_15 = BilliardBall([-(triEdge+2*height),-2*(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.striped, steel_red)
    b_black    = BilliardBall([-(triEdge+2*height),0],[0.0,0.0], BBallType.black)
    solid_1    = BilliardBall([-(triEdge+2*height),2*(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.solid, steel_orange)
    # Fourth row
    solid_6    = BilliardBall([-(triEdge+3*height),-3*(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.solid, steel_yellow)
    striped_10 = BilliardBall([-(triEdge+3*height),-(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.striped, steel_yellow)
    solid_3    = BilliardBall([-(triEdge+3*height),(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.solid, black)
    striped_14 = BilliardBall([-(triEdge+3*height),3*(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.striped, steel_red)
    # Fifth row
    striped_11 = BilliardBall([-(triEdge+4*height),-4*(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.striped, steel_orange)
    solid_2    = BilliardBall([-(triEdge+4*height),-2*(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.solid, steel_green)
    striped_13 = BilliardBall([-(triEdge+4*height),0],[0.0,0.0], BBallType.striped, steel_red)
    solid_4    = BilliardBall([-(triEdge+4*height),2*(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.solid, steel_yellow)
    solid_5    = BilliardBall([-(triEdge+4*height),4*(corrector+BALL_RADIUS)],[0.0,0.0], BBallType.solid, steel_yellow)

    b_balls = [striped_9, striped_10, striped_11, striped_12, striped_13, striped_14, striped_15, solid_1, solid_2, solid_3, solid_4, solid_5, solid_6, solid_7, b_whitey, b_black]

    # Creates and activate the loader
    loader = primitives.Loader([200.0,200.0])
    loader.activate()
    force_line = ForceLine(b_whitey)

    shoot_mode = False

    prev_num_hands = 0

    #Tutorial screens
    tutorial01_screen = Screen("./Screenshots/tutorial01.png")#, [tutorial_to_02_button])
    tutorial02_screen = Screen("./Screenshots/tutorial02.png")#, [tutorial_to_03_button])
    tutorial03_screen = Screen("./Screenshots/tutorial03.png")#, [tutorial_to_04_button])
    tutorial04_screen = Screen("./Screenshots/tutorial04.png")#, [tutorial_to_05_button])
    tutorial05_screen = Screen("./Screenshots/tutorial05.png")#, [tutorial_to_06_button])
    tutorial06_screen = Screen("./Screenshots/tutorial06.png")#, [tutorial_to_07_button])
    tutorial07_screen = Screen("./Screenshots/tutorial07.png")#, [tutorial_to_08_button])
    tutorial08_screen = Screen("./Screenshots/tutorial08.png")#, [tutorial_start_button])

    #Tutorial buttons
    tutorial_to_02_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], tutorial02_screen)
    tutorial_to_03_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], tutorial03_screen)
    tutorial_to_04_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], tutorial04_screen)
    tutorial_to_05_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], tutorial05_screen)
    tutorial_to_06_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], tutorial06_screen)
    tutorial_to_07_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], tutorial07_screen)
    tutorial_to_08_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], tutorial08_screen)
    tutorial_start_button = ActionButton([[1024-661,800-749],[1024-363,800-451]], disableTutorial)

    # Bind tutorial buttons to tutorial screens
    tutorial01_screen.buttons = [tutorial_to_02_button]
    tutorial02_screen.buttons = [tutorial_to_03_button]
    tutorial03_screen.buttons = [tutorial_to_04_button]
    tutorial04_screen.buttons = [tutorial_to_05_button]
    tutorial05_screen.buttons = [tutorial_to_06_button]
    tutorial06_screen.buttons = [tutorial_to_07_button]
    tutorial07_screen.buttons = [tutorial_to_08_button]
    tutorial08_screen.buttons = [tutorial_start_button]

    #Menu screens
    menu_start_screen = Screen("./Screenshots/menu01_start.png")#, [to_opt_button, quit_menu_button, quit_game_button])
    menu_general_opt_screen = Screen("./Screenshots/menu02_options.png")#, [to_ball_opt_button, to_hand_opt_button, back_to_first_button])
    menu_ball_opt_screen = Screen("./Screenshots/menu03_balls.png")#, [red_ball_button, orange_ball_button, back_to_opt_button])
    menu_hand_opt_screen = Screen("./Screenshots/menu04_hands.png")#, [red_hand_button, green_hand_button, back_to_opt_button])

    #First screen buttons
    menu_to_opt_button = NavigationalButton([[1024-977,800-475],[1024-559,800-57]], menu_general_opt_screen)
    menu_quit_menu_button = ActionButton([[1024-465,800-475],[1024-47,800-57]], disableMenu)
    menu_quit_game_button = ActionButton([[1024-661,800-749],[1024-363,800-451]], quitGame)

    #General options screen buttons
    menu_to_ball_opt_button = NavigationalButton([[1024-977,800-475],[1024-559,800-57]], menu_ball_opt_screen)
    menu_to_hand_opt_button = NavigationalButton([[1024-465,800-475],[1024-47,800-57]], menu_hand_opt_screen)
    menu_back_to_first_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], menu_start_screen)

    #Ball options screen buttons
    menu_orange_ball_button = ActionButton([[1024-977,800-475],[1024-559,800-57]], setBallsToOrangeYellow)
    menu_red_ball_button = ActionButton([[1024-465,800-475],[1024-47,800-57]], setBallsToRedGreen)
    menu_back_to_opt_button = NavigationalButton([[1024-661,800-749],[1024-363,800-451]], menu_general_opt_screen)

    #Hand options screen buttons
    menu_red_hand_button = ActionButton([[1024-977,800-475],[1024-559,800-57]], setHandToRed)
    menu_green_hand_button = ActionButton([[1024-465,800-475],[1024-47,800-57]], setHandToGreen)

    # Bind buttons to screens
    menu_start_screen.buttons = [menu_to_opt_button, menu_quit_menu_button, menu_quit_game_button]
    menu_general_opt_screen.buttons = [menu_to_ball_opt_button, menu_to_hand_opt_button, menu_back_to_first_button]
    menu_ball_opt_screen.buttons = [menu_red_ball_button, menu_orange_ball_button, menu_back_to_opt_button]
    menu_hand_opt_screen.buttons = [menu_red_hand_button, menu_green_hand_button, menu_back_to_opt_button]

    tutorial = Menu(tutorial01_screen,loader)
    tutorial.enable()

    menu = Menu(menu_start_screen,loader)

# Panacea method
def processFrame():
    global shoot_mode, force, prev_num_hands

    new_frame, hands, iBox = leap.getHands()
    objects = [b_table]

    if sum(new_frame) == 2 and prev_num_hands == 1:
        menu.swap()
    prev_num_hands = sum(new_frame)

    # Learn how to play
    if tutorial.enabled:
        objects += [processMenu(tutorial, new_frame, hands, draw_hands, iBox)]

    # Pause the game!
    elif menu.enabled:
        objects += [processMenu(menu, new_frame, hands, draw_hands, iBox)]

    # If the menu and the tutorial are not enabled:
    # Let the pool begins! And may the odds be ever in your favor.
    else:
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

        # Updates the position of all the balls
        for ball in b_balls:
            ball.updatePos()

        objects += b_balls


    return objects
