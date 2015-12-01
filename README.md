# Leap Motion project

## Introduction
This repository contains the Leap Motion project developed for the course **Nuevos Paradigmas de Interacción** at the University of Granada, Spain.

The final goal is to simulate the classical game of *las chapas*, letting the user to interact with the computer through the movement of its own hands.

### Current state
By now, just a first recognition and interaction phase has been implemented. The functionality now is simple: the scene has just a ball that changes its colour when it is touched.

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
$> pacman -S python2 python2-opengl python2-pygame python2-pillow python2-enum34 python2-shapely
```

[leap-motion-driver](https://aur.archlinux.org/packages/leap-motion-driver) and [leap-motion-sdk](https://aur.archlinux.org/packages/leap-motion-sdk) packages are not in the official repository but in the Arch User Repository. To install them, just build the packages manually or use a package manager like `pacaur`:

```
$> pacaur -S leap-motion-driver leap-motion-sdk
```

Caution! leap-motion-sdk throws an error if the pkg-build is not edited. You have to add `${pkgdir}` in the following lines
```
install -D -m644 "/usr/lib/Leap/Leap.py" "${pkgdir}/usr/lib/python2.7/site-packages/Leap.py"
install -D -m644 "/usr/lib/Leap/LeapPython.so" "${pkgdir}/usr/lib/python2.7/site-packages/LeapPython.so"
```

They have to look like this:
```
install -D -m644 "${pkgdir}/usr/lib/Leap/Leap.py" "${pkgdir}/usr/lib/python2.7/site-packages/Leap.py"
install -D -m644 "${pkgdir}/usr/lib/Leap/LeapPython.so" "${pkgdir}/usr/lib/python2.7/site-packages/LeapPython.so"
```

## Execution and usage
Connect the Leap Motion, start the daemon -with `sudo leapd` or `sudo systemctl start leapd`-, and execute the following order:
```
$> python2 main.py
```

You will see a tutorial like the following:

![Primera escena](Screenshots/01.png)

Follow the tutorial step by step and you will get to the real program!s

![02](Screenshots/02.png)

![03](Screenshots/03.png)

![04](Screenshots/04.png)

When you finish the tutorial, you can start playing with the ball and with its colors. Try to touch it with one hand, the other, or even both of them!

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

### Final implemented solution

Basing in the previus development, we realised that our design had lot of difficulties for being expanded and maintained, for this reasons we decided to use a new design based in mora files and classes. This files are:


- [billiard.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/billiard.py)
- [constants.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/constants.py)
- [forceLine.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/forceLine.py)
- [game.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/game.py)
- [gestures.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/gestures.py)
- [GUI.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/GUI.py)
- [hand.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/hand.py)
- [leapDriver.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/leapDriver.py)
- [main.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/main.py)
- [menu.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/menu.py)
- [primitives.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/primitives.py)

Thanks to this, if in the future we want to continue the development of this game or other person want to create another application, they can base in part of code developed here.

In the opposite the principal objective of *las chapas* development, we changed our principal objective deciding for develop the billiard game. This decision born because of the difficultyness of draw a cap and the game of *las chapas* didn't have a hardly defenited rules than the billiard. Also because of the world know of the billiard, it shows more easyness for being accepted by the society than the game of *las chapas*. Althought both games are quite similar. 


Basándonos en todo lo hecho anteriormente, nos dimos cuenta que nuestro diseño tendría demasiados impedimentos para ser ampliado y mantenido, con lo cual decidimos pasar a un diseño basado en más archivos y varias clases. Los archivos son:

- [billiard.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/billiard.py)
- [constants.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/constants.py)
- [forceLine.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/forceLine.py)
- [game.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/game.py)
- [gestures.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/gestures.py)
- [GUI.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/GUI.py)
- [hand.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/hand.py)
- [leapDriver.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/leapDriver.py)
- [main.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/main.py)
- [menu.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/menu.py)
- [primitives.py](https://github.com/agarciamontoro/leap-motion-project/blob/wip/primitives.py)

De esta manera, si en el futuro deseamos continuar el desarrollo de éste juego o nosotros u otras personas desean crear algún otro, podrán basarse en parte del código aquí desarrollado.

Las contrapartidas del objetivo principal del desarrollo *las chapas*, nos hizo decantarnos por cambiar nuestro objetivo final, decidiendo desarrollar el juego del *billar*. Ésta decisión nació de la dificultad de dibujar una chapa y de que no es un juego con unas reglas tan establecidas cómo es el caso del billar. Además de que el *billar* por ser un juego mundialmente conocido, presentaba más facilidad para ser aceptado por la sociedad que el juego de *las chapas*. Aún así ambos juegos tienen muchas similitudes, con lo que llegar de uno al otro no presenta un gran reto.

#### Breve descripción del problema (Billar)
En el juego del billar, actúan principalmente 2 fuerzas de la naturaleza el **rozamiento** y la **cinética**:

Por ello, para conseguir un billar cercano a la realidad, necesitabamos simular todas esas fuerzas. Para ello se ha hecho simplifación de todas las fuerzas actuantes en el problema, limitando la dimensión de éstas a 2.
Para la simulación de los choques, apliques de fuerzas y su consiguiente resultado se ha usado para el sistema de simulación *elastic collision*, en cambio para la simulación del rozamiento se ha establecido un coeficiente de rozamiento, y en cada frame, ese coeficiente, va alterando la velocidad *cinética* de todas las bolas en movimiento.

Debido a la complejidad de la ecuación que describe la *elastic collision*:

![Elastic collision ecuation](https://upload.wikimedia.org/math/b/0/9/b09d23456a39b81126c36844fdc13582.png)

Se han considerado las masas de todas las bolas 1, obteniendo así una ecuación más fácil al anularse el primer elemto del numerador de ambas, sin alterar en gran medida la realidad de la simulación

Volviendo a la implementación. Como hemos comentado anteriormente hemos optado por un diseño basado en varias archivos y clases. A continuación se va a hacer una breve descripción del contenido de cada uno de los archivos, y de las clases existentes en ellos.

#### constants.py
Éste archivo tan solo contiene algunas de las constantes que se van a usar a lo largo de todo el proyecto
#### LeapDriver.py
Éste archivo tan solo contiene la clase **SampleListener** implementada tal y como se recomienda en la documentación del Leap-Motion con tan solo algunos cambios menores para adaptarlo a nuestro programa.
#### gestures.py
Éste archivo tan solo contiene el control de los distintos gestos que se desea detectar.
#### primitives.py
En este archivo podemos encontrar las clases **Image**, **Line**, **Ball**, **Quad**, **Circle**, **Loader** y **Button**, a continuación las comentarmeos brevemente.

- **Image** Nos permite dibujar una imagen en nuestro mundo virtual de manera que no seamos conscientes que estamos en un mundo 3D.
- **Line** Nos permite dibujar la línea que une 2 puntos en el espacio 3D
- **Ball** Nos permite dibujar una esfera en el punto deseado, con radio y calidad deseados
- **Quad** Nos permite dibujar el *quad* que forman un conjunto de puntos
- **Circle** Nos permite dibujar un disco en el punto deseado, con radio y calidad deseados
- **Loader**
- **Button**

#### hand.py
En este archivo podemos encontrar las clases **Hand** y **Finger**. El principal objetivo de ambas es el correcto dibujado de éstas. Como es natural, la mano (**Hand**) contendrá en su interior los distintos dedos (**Fingers**). **Fingers** en cambio contiene a partir de la identificación mediante el uso de los datos proporcionados por el Leap-Motion, los puntos necesarios para crear las falanges y los nudillos, que simplemente son objetos **Ball** y **Line**.
#### forceLine.py
En este archivo podemos encontrar la clase **ForceLine**. El principal objetivo de esta clase es el obtener los medios para poder pintar e identificar la fuerza con la que se desea golpear a la bola blanca.
#### billiard.py
En este archivo podemos encontrar las clases **BilliardBall** y **BilliardTable**. El principal objetivo de ambas es encapsular las propiedades físicas comentadas anteriormente (Colisiones y Rozamiento), siendo en el caso de **BilliardBall** una subclase de **Ball**.
#### menu.py
#### game.py
Este archivo tal y como su nombre indica, implementa todo lo referente al juego. Posición inicial de las bolas, colores, fuerzas, etc.
Como primera tarea, tiene la de establecer las posicones de las bolas. A continuación inicializa el menú. Y durante el resto de la ejecución se ocupa de la lógica principal del juego, haciendo uso de las distintas clases descritas anteriormente.
#### main.py
Este archivo se limita a inicializar los distintos objetos descritos anteriormente para que comience el juego.

## References
* **GUI.py**: the basic OpenGL functions -init, camera, projection and view settings- in this file are adapted from this [@analca3](https://github.com/analca3)'s repository: [Triodo de Frenet](https://github.com/analca3/TriedroFrenet_Evoluta).
* **LeapDriver.py**: the basic structure of this file is taken from the [Hello World tutorial](https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html).
* Some information about [Elastic collision](https://en.wikipedia.org/wiki/Elastic_collision)
* **Billiard cloth**: the texture used is taken from [](http://www.photos-public-domain.com/2012/08/14/kelly-green-microfiber-cloth-fabric-texture/)
* **Icons**: All icons have Free or CC licenses. See the [gear](https://www.iconfinder.com/icons/103170/gear_preferences_settings_tools_icon#size=128), [arrow](https://www.iconfinder.com/icons/647889/arrow_back_direction_move_previous_icon#size=128), [cross](https://www.iconfinder.com/icons/226589/circle_cross_icon#size=128) and [hand](https://www.iconfinder.com/icons/446303/finger_gesture_hand_interactive_scroll_swipe_tap_icon#size=128) pages for more information.
