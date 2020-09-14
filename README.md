# Interactive Snake Game

_____


<!-- ## Contributers: 

* Dana Abbadi
* Yazan Alshikha 
* Abedalaziz Alissa -->

<!-- ___________ -->

A traditional snake game with an upscale feature of controlling the game with hand gestures using a color detection model.

______

## Table Of Contents

* [Describtion](#desc)
* [Technologies](#tech)
* [Getting Started](#start)

_________


<a name="desc"></a>

## Description

Bringing back the glory of the old and popular arcade game Snake by transforming how the player can control the snake movements, using a color detection tracker, the model can detect the directions of a moving object with the detected color and will move the snake accordingly.  

However, the vission is to develop a model that can control and change some functionalities on the screen according to external or outsider influence, although the model is applied to a simple logic based game, the basic concept is to be able to read hand gestures from the web cam, thus it can be evolved to bigger and more complex applications like controlling a video or offering useful tools to people with disabilities to the point where they can use thier computers without the need of assistance.

Add screenshots
____________

<a name="tech"></a>

## Technologies

For color detection, we used **HSV** tracker from **opencv** library, the model will track the position of the detected color and will perfom an action according to the movement, for the snake game the action is to move the snake towords the correct direction.

To move the snake after detecting the direction, we used **PyAutoGUI**, PyAutoGUI lets your Python scripts control the mouse and keyboard to automate interactions with other applications, in this case the snake game.

The game is recreated using **Tkinter's** very powerful **Canvas** widget, to provide the platform for the Snake program.

_______________

<a name="start"></a>


## Getting Started

The program depends on the following libraries-

    numpy==1.19.1
    imutils==0.5.3
    PyAutoGUI==0.9.50
    opencv-python==4.4.0.42
    opencv-contrib-python==4.4.0.42
    pygame==1.9.6
    future==0.18.2
    

Install the libraries using: pip install -r installation.txt in your terminal.

### Installation

1. Clone the repository in your local computer.
2. Use python < filename.py > to run specific files, two files are needed to run the program:

    python detecting_directions.py
    python snake_game.py



### Built With

* OpenCV - The Open Computer Vision Library.
* PyAutoGUI - Cross platform GUI Automation Python Module.
* Tkinter - Standard Python interface to the Tk GUI toolkit.

____________






  