# SoccerAA: Soccer Advertisement Analysis
**Advertisement analysis at sport events**

This prototype demonstrates the concept to detect Advertisements specific in football games. 

Object and image detection is already a well-researched area. However, most reliable methods are based on a learning process where the algorithm learns to detect the specific object. This makes it impossible to quickly change the advertising templates as the algorithms (Neural Networks, Haar Cascades) have to be retrained on them. 
This prototype uses the unique features specific for the domain in football games to detect advertisements on the fly. 

This software performs sponsorship evaluation for football games.

![Demo SoccerAA](./demo/demo.gif)

### Installation

1.	Make sure Python 3.7 and pip3 is installed on your local machine.

2.	Clone this repository and change into it: <br>
``` git clone https://github.engineering.zhaw.ch/BA19-wele/SoccerAA.git ```

3.	Use pip3 to install the requirements: <br>
``` pip3 install –r requirements.txt ```

### Usage
Before you start the application, make sure the inputs are placed in the correct directories: <br>

- Place the templates of the advertisements which are going to be searched in: <br>
``` data/in/templates ``` <br>
PNG or JPG images are accepted. The given name of the template will be later used to label the found advertisements. 
Two example templates are already provided.

- Place the videos you want to analyse into: <br>
``` data/in/videos ``` <br>
.mp4 is the only accepted format.

- Place single Images you want to analyse in into: <br>
``` data/in/targets ``` <br>
PNG or JPG images are accepted.

To run the application switch to the directory ```app/``` and use the following command: <br>




### Dependencies

- Python 3.7
- opencv-contrib-python 3.4.2.16
- termcolor
- numpy



