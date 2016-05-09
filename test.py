# A simple test code

from mainCode import *

import unittest

def testMaze(inputfile):
    outputfile='./test_cases/out.tex'
    laser_maze=maze_grid(inputfile,outputfile)
    laser_maze.fire()
    f=open(outputfile,'r')
    counter=f.readline().strip()
    hit_pos=f.readline().split()
    if not counter:
        counter=-1
    if not hit_pos:
        hit_pos=[-1,-1]
    return [int(counter),[int(hit_pos[0]),int(hit_pos[1])]]
    
        

class myTest(unittest.TestCase):
    def test_testMaze1(self):
        inputfile='./test_cases/maze_18_0_0.tex'
        self.assertEqual(testMaze(inputfile),[18,[0,0]])
    def test_testMaze2(self):
        inputfile='./test_cases/maze_9_0_0.tex'
        self.assertEqual(testMaze(inputfile),[9,[0,0]])
    def test_testMaze3(self):
        inputfile='./test_cases/maze_11_0_2.tex'
        self.assertEqual(testMaze(inputfile),[11,[0,2]])
    def test_testMaze4(self):
        inputfile='./test_cases/maze_loop_0.tex'
        self.assertEqual(testMaze(inputfile),[-1,[-1,-1]])
    def test_testMaze5(self):
        inputfile='./test_cases/maze_27_5_5.tex'
        self.assertEqual(testMaze(inputfile),[13,[0,0]])
    def test_testMaze6(self):
        inputfile='./test_cases/maze_31_0_2.tex'
        self.assertEqual(testMaze(inputfile),[7,[4,2]])
    def test_testMaze7(self):
        inputfile='./test_cases/maze_n1.tex'
        self.assertEqual(testMaze(inputfile),[-1,[-1,-1]])
    def test_testMaze8(self):
        inputfile='./test_cases/maze_zeroDimen.tex'
        self.assertEqual(testMaze(inputfile),[0,[2,4]])

unittest.main()
    
