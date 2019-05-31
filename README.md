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
```python3 socceraa.py [-h] [--input INPUT] [--accuracy {low,medium,high}] [-debug] [-out] [-tr]``` <br><br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; optional arguments:

*-h, --help:* Shows help message and exits. <br><br>
*--input INPUT:* Set INPUT to 'images' to analyse the single images in the directory ``` data/in/targets ``` . Set INPUT
to the name of the video in ``` data/in/videos ``` to analyze whole video. Default: 'images' <br><br>

*--accuracy:* Set accuracy of ad detection (low accuracy has highest performance) <br><br>

*-debug:* Flag which enables debug messages in console. <br><br>

*-out:* Flag which shows in realtime results during process. <br><br>

*-tr:* Flag which shows in realtime filtered Area from various features. 

<br>

**Examples:**<br>
```python3 socceraa.py --input images```<br>
Starts the application and analyzes the pictures in ```data/in/targets ``` for ads in ```data/in/templates ``` <br><br>

```python3 socceraa.py --input wanda.mp4 --accuracy medium -out```<br>
Analyzes the video "wanda.mp4" for ads in ```data/in/templates ``` in medium accuracy 
and shows the results in realtime. <br><br>

```python3 socceraa.py --input qatar.mp4 --accuracy high```<br>
Analyzes the video "qatar.mp4" in highest accuracy.<br><br>

**Output:**<br>
The outputs are generated in the directory: ``` /data/out ```



### Dependencies

- Python 3.7
- opencv-contrib-python 3.4.2.16
- termcolor
- numpy



