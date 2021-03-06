# Fuzzy Logic Based Game Implementation
This repository is an implementation of a fuzzy logic based game which was given to me as an assignment for my master's degree program. The logic of the game is described in an article titled "Developing a fuzzy logic based game system" by Utku Kose. 

The aim of the assignment is to build a fuzzy logic engine from scratch without using any already published module. Most of the calculations were carried out with numpy and are very specific to this particular logic. 

The python file takes in input form the user for the ammo and health level and gives an approperate action defined by the fuzzy logic. These results are visualized using graphs, an example of the output graph is shown below:
![Example of Fuzzy Logic Game Engine Output](https://github.com/morukele/Fuzzy-Logice-Based-Game/blob/main/Ammo%2010%2C%20Health%2025%20Sum%20Aggregator%20Defense.png)



The user also has the option of selecting between summation or max aggregator and also between a center of gravity or mean of maximum defuzzification. 

The Fuzzy Logic Engine code is found in FuzzyLogicGameEngine.py while the FuzzyLogicGamePlotCode.py file contains code that created a 3D plot of the overview of the system behaviour as shown below: 
![3D plot of the fuzzy logic system behaviour](https://github.com/morukele/Fuzzy-Logice-Based-Game/blob/main/3D%20Surface%20Plot.png)
