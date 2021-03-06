# Leap Motion project

## Introduction
This repository contains the Leap Motion project developed for the course **Nuevos Paradigmas de Interacción** at the University of Granada, Spain.

The final goal is to simulate the classical game of *las chapas*, letting the user to interact with the computer through the movement of its own hands.

The final goal commented before has changed in the current version, now is to simulate the **billiard** game.

## Instalation
The project is coded in Python, using the Leap Motion driver and the OpenGL library. The required dependencies are the following:

1. **Python2**
2. **Leap-Motion-Driver**
3. **Leap-Motion-SDK**
4. **Python2-OpenGL**
6. **Python2-pillow**
7. **Python2-enum34**
8. **Python2-shapely**

The most common distributions have all the library packages needed, but maybe the Leap Motion driver and SDK are not in the repositories. However, it is easy to download them from the [Download](https://developer.leapmotion.com/downloads) section of Leap Motion web page.


The [Python API](https://developer.leapmotion.com/documentation/python/index.html) could also be useful if some error appear.

If the Python OpenGL library is not in your distribution repository, use the package manager **pip** to install them.

### Arch Linux example
Arch Linux has all required packages in the official -and AUR- repositories. To install Python and OpenGL, execute the following order:
```
$> pacman -S python2 python2-opengl python2-pygame python2-pillow
   python2-enum34 python2-shapely
```

[leap-motion-driver](https://aur.archlinux.org/packages/leap-motion-driver) and [leap-motion-sdk](https://aur.archlinux.org/packages/leap-motion-sdk) packages are not in the official repository but in the Arch User Repository. To install them, just build the packages manually or use a package manager like `pacaur`:

```
$> pacaur -S leap-motion-driver leap-motion-sdk
```

Caution! leap-motion-sdk throws an error if the pkg-build is not edited. You have to add `${pkgdir}` in the following lines
```
install -D -m644 "/usr/lib/Leap/Leap.py"
        "${pkgdir}/usr/lib/python2.7/site-packages/Leap.py"
install -D -m644 "/usr/lib/Leap/LeapPython.so"
        "${pkgdir}/usr/lib/python2.7/site-packages/LeapPython.so"
```

They have to look like this:
```
install -D -m644 "${pkgdir}/usr/lib/Leap/Leap.py"
        "${pkgdir}/usr/lib/python2.7/site-packages/Leap.py"
install -D -m644 "${pkgdir}/usr/lib/Leap/LeapPython.so"
        "${pkgdir}/usr/lib/python2.7/site-packages/LeapPython.so"
```

## Execution and usage
Connect the Leap Motion, start the daemon -with `sudo leapd` or `sudo systemctl start leapd`-, and execute the following order:
```
$> python2 main.py
```

When you finish the tutorial, you can start playing with the real game!

*Note: if you just want to know about the current version, go to Second assignment section*

## First assignment
### Problem considered
The final goal is to improve and make more real the interaction with the computer through the use of the Leap Motion device and its developer API.

As a first assignment, we decided to create a scene in which the hands were realistically created and where we could test an interaction proof of concept.

The first idea that came to our heads was to become a Jedi. We wanted the Leap to detect our hand gestures and use the Force to move objects throughout the scene. However, this idea, as it is already implemented by someone else, was changed by a simpler game concept: the old classical *las chapas*.

### Solutions proposed

The first decision we made was the language and graphic library we wanted to use. Initially, we wanted to use Unreal Engine or Unity3D, as its graphic power and ease to use are greater than OpenGL. However, we chose this later option: our computers have low performance and a Linux+OpenGL setup is more appropriate for us; furthermore, Windows and Unreal or Unity are privative and need higher computing power.

Then, we decided which language to use: we needed a multi-platform language in which we could program fast. We did not worry about the computing performance: some milliseconds more or less were not critical. Python fulfill all these requirements and, furthermore, we had a Python code implementing the basic OpenGL structure.

With the language and libraries chosen, we started the project.

We found the first difficulty at the very beginning: the drawing of the hands was not trivial. We spent a lot of time dealing with the hand structure provided by Leap Motion and, overall, with the OpenGL code.

The hand bone structure is simple and easy to use: all the important points are given as three-dimensional vectors in milimiters and the direction of the bones are provided as normalized vectors. We tried to visualize the bones as cylinders that were first drawn in the origin and then were rotated and translated. The translation was easily achieved, but we spent too much time dealing with the rotation code and decided to try a simpler solution: as all the bone junctions were given as points in the space, we just had to draw lines between each pair of them. All our rotation problems vanished.

When we had the hand representation nearly finished, we started to make the interaction code. As a first idea, that was the one we finally implemented, we decided to draw a ball in the space and to let the user touch it and see its color changing.

The implementation of this code was straightforward; we did not have too much problems with it, as just some distances had to be measured and some colors had to be changed. However, when we had all the program working, we realized that the visualization was poor: we needed the user to understand where his/her hands were. We needed to add some reference that could make more real the positioning of the hands in the virtual world: the shadows were the solution!

A simple but powerful shadow was implemented: the hands were just projected in the XZ plane with a gray color. Later, we improved the solution by changing the shadow relative size depending on the Y coordinate.

When the program was finished, we made a simple tutorial that explained how to use the program. Furthermore, we chose to implement Leap gestures to advance throughout the tutorial: the user has to make a key tap gesture in order to get to the next step.

The gesture was easily implemented with the Gesture interface of the API.

## Second assignment
### Final implemented solution

With the experience of our previous development, we realised that our design had a lot of difficulties for being expanded and maintained. For these reasons, we decided to use a new modular design, ordered in structured files and classes. This modular design will help us -or any other developer- in the future to reuse code for any other software.

Furthermore, we changed the principal objective of *las chapas* game, deciding we would develop a billiard game. This decision was based on the difficulty of drawing a *chapa* and the lack of well-defined rules of the game. Also, the billiard is a world known game, whereas *las chapas* is also known in Spain. The change, however, did not force us to change all of our code, as the physics and logics involved in both game are quite similar.

Due to all the changes commented before, many things develpoed in the **First assigment** have change, for example the tutorial.

#### Description of billiard game physics
The physics considered in this billiard game are the following: the **friction** of the balls with the table, the **collisions** between balls and between the balls and the table, and the **force applied** to the white ball. All the movements are then studied as uniformly accelerated movements, slowed down by the friction.

For achieving a realistic billiard, we need to simulate these physics. As all the movements are done in the table plane, a first simplification can be done: the physics can be reduced to a two-dimensional problem. The collisions are implemented as perfectly *ellastic collsions*; i.e., under the law of the following equations, that give the new velocities of two colliding balls depending on their positions, the previous velocities and the masses:

![Elastic collision equation](https://upload.wikimedia.org/math/3/a/7/3a70e57f4a5cc0e5e0e11be153aa4b10.png)

These equations can be simplified considering all ball masses equal to 1. This consideration does not affect the realism of the game, as all the billiard balls have the same mass and, measuring in the appropriate units, can be seen equal to 1.

On the other hand, for the simulation of the *friction*, just a simple **friction** coefficient has been considered. This coefficient slows down, in each frame, the module of the velocity of every ball.

#### Implementation

Our modular design, which follows a pure object-oriented paradigm to ease the expansion and maintaining of the code, is structured in the following files:

- [billiard.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/billiard.py)
- [constants.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/constants.py)
- [forceLine.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/forceLine.py)
- [game.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/game.py)
- [gestures.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/gestures.py)
- [GUI.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/GUI.py)
- [hand.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/hand.py)
- [leapDriver.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/leapDriver.py)
- [main.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/main.py)
- [menu.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/menu.py)
- [primitives.py](https://github.com/agarciamontoro/leap-motion-project/blob/master/primitives.py)

The main structure is quite simple: the endless OpenGL loop of the GUI is always asking the game.py file for objects to draw. This file, when required by the GUI, asks for the hand data to the Leap Motion listener, process the data -see interaction between hands and balls, detect collisions, manage the tutorial/game/menu logic...- and returns to the GUI a list of objects that contain a `draw` method. The GUI, then, draws all the elements returned by the game calling this method in all the objects.

This structure derives in a frame-based animation, and not in a time-based animation. Although this last technique is more often used and more efficient, the first one was implemented, as a lot of the code was already implemented in this kind of structure.

Let's see the files and its classes:

#### constant.py
This file contains just the constants that will be used across the project.

#### leapDriver.py
This file contains the **SampleListener** class, implemented as recommended in the documentation the Leap-Motion, with some little changes for adapting it to our program.

#### gestures.py
This file contains the control of all the gestures that we need to detect.

#### primitives.py
This file contains the basic drawing primitives:

- **Image**: it implements the drawing of a 2D image filling the window.
- **Line**: it implements the drawing of a line that join 2 points in the 3D space.
- **Ball**: it implements the drawing of a sphere given its center, radius and quality desired.
- **Quad**: it implements the drawing of the *quad* that creates a set of points.
- **Circle**: it implements the drawing of a 2D disc projected in the window given its center, radius and quality desired.
- **Loader**: it implements the logic and drawing of a loader that is used when the menu buttons are pressed.
- **Button**: it implements the basics of a button; i.e., the methods used both by navigational and action buttons.

#### hand.py
In this file we can find the classes **Hand** and **Finger**. The principal objective that both is the draw of them. As natural, the hand contains several fingers. **Fingers** in the other hand contains with the identification using data provides by Leap-Motion, the needed points for the phalanx and knucles, tthat only are **Ball** and **Line**

#### billiard.py
In this file we can find the classes **BilliardBall** and **BilliardTable**. The principal objective of both is encapsule the physics properties previously mentioned (collision and friction), being **BilliardBall** a subclass of **Ball**.

##### menu.py
This file contains the necessary classes to implement a menu, which consists of a screen (basically, an image) and an arbitrary number of buttons. The classes in this file are the following:

* **NavigationalButton**: Class implementing a button whose objective is to change the screen; i.e., to navigate between the menu screens.
* **ActionButton**: Class implementing a button whose objective is to execute an arbitrary function when pressed.
* **Screen**: Class implementing the images that form the menu. A screen is formed by an image and a list of buttons in the image.
* **Menu**: Main class, that uses all the classes before to implement an easy-to-use menu. A menu consists only of a start screen and a loader -an auxiliary object to manage the button *clicks*-. The navigation between the screens is transparent to the menu, as it is easily managed by the navigational buttons.

##### game.py
This file uses all the resources commented before for establish the initial position of the balls, colors, forces... As first task, it has to establish the balls position. After, it initializes the menu. Now it only does the principal logic of the game.  

##### main.py
This file only initializes the different objects for the initialization of the game.

### Known bugs
#### Ball collision bug
There are some times that the balls collide and the collision management does not work well. Therefore, the balls stick together one inside the other. Then, the problem disappears as it appeared.

We think the problem is not in the collision management but in the collision detection -we use predictive collision techniques, but for some reason, there are some times that it fails-.

#### Window size
Although the window size is hard-coded to be 1024x800 px, the window behaves in different ways depending on the monitor resolution. We do not know what could cause this bug, as the image stretches in smaller screen resolutions in spite of the hard-coded values.

#### Hand detection in some borders of the device
There are some zones in the Leap Motion detection box that behave worst than the others. For example, the zone closer to the monitor makes the detection to behave strangely. We do not know if this is a problem of the Leap Motion device or of our own code.

## References
* **GUI.py**: the basic OpenGL functions -init, camera, projection and view settings- in this file are adapted from this [@analca3](https://github.com/analca3)'s repository: [Triodo de Frenet](https://github.com/analca3/TriedroFrenet_Evoluta).
* **LeapDriver.py**: the basic structure of this file is taken from the [Hello World tutorial](https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html).
* Some information about [Elastic collision](https://en.wikipedia.org/wiki/Elastic_collision)
* **Icons**: All icons have Free or CC licenses. See the [gear](https://www.iconfinder.com/icons/103170/gear_preferences_settings_tools_icon#size=128), [arrow](https://www.iconfinder.com/icons/647889/arrow_back_direction_move_previous_icon#size=128), [cross](https://www.iconfinder.com/icons/226589/circle_cross_icon#size=128) and [hand](https://www.iconfinder.com/icons/446303/finger_gesture_hand_interactive_scroll_swipe_tap_icon#size=128) pages for more information.
