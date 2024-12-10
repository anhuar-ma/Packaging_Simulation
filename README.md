# Robot Packaging Simulation

This repository contains a simulation program that models the packaging process carried out by five robots. The robots work collaboratively to pick and pack boxes into a container. The program is implemented with Julia as the back-end and OpenGL for the front-end visualization.
Features

###Box Generation:
The simulation begins by generating 20 randomly placed boxes within the workspace.
Each box has randomly assigned dimensions ranging between 1 and 7 units for width, height, and depth.

###3D Bin Packing:
Given the dimensions of the boxes and the container, the program calculates the optimal way to arrange the boxes using 3D bin packing algorithms.
This process determines the ideal position and sequence for storing the boxes in the container.

###Robot Navigation:
Robots are tasked with retrieving and packing boxes based on the computed optimal order.
Each robot uses the A* algorithm to navigate the shortest path to its assigned box.
If a robot retrieves a box that is out of sequence, it will wait until the correct box is packed before proceeding.

###Collaboration and Coordination:
The simulation ensures proper coordination between robots to avoid conflicts and maintain the optimal packing sequence.
