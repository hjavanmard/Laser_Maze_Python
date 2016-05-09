# Laser_Maze_Python

command line application that builds and solves a simple “laser maze”

The command line application can be run as follows:

**./maze ./path/to/input/file  ./path/to/output/file**

The main code is named "manCode.py" written in Python. It includes two calsses for laser beam and maze. There is a helper module
named "mazeDraw.py" which is used in maze class to visualize the maze and laser path.

To testing, there is a folder named "test_cases" where one stores the test files. By running the following command, the main code will be tested agianst files inside provided test cases:
python test.py
