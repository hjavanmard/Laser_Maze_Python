import sys
from mazeDraw import *  # mazeDraw is a helper module to visualize maze

# we treat lazer beam as a seperate object. This makes easier to add features specific
# to lazer beam. One can even create more than one lazer beam with less effort.
class beam:
    def __init__(self,position,direction):
        self.position=position # initial position of laser
        self.next={'S':[0,-1],'N':[0,1],'E':[1,0],'W':[-1,0]}
        self.direction=self.next[direction] # the initial direction of player
        self.counter=0	    # the number of squers traveled by laser
        self.bounce=dict()   # stores positions where laser is bounced--> to check if laser is traped in a loop or not
        self.path=[[position[0],position[1]]] # stores path of laser for visualization fxn
        self.loop=False # a simple boolean variable to check if the laser is caught up in a loop

    def update_pos(self,position):
        # a helper function to update position
        self.position=position
        
    def beam_pos(self):
        # returns position of laser at anytime
        return self.position
    
    def move_next(self):
        # moves laser to the next square
        self.position[0] +=self.direction[0]
        self.position[1] +=self.direction[1]
        self.path.append([self.position[0],self.position[1]])
        self.counter +=1
        
    def reflect(self,mirror):
        # handles when laser bounce from a mirror, and change direction
        t=(self.position[0],self.position[1])
        if t not in self.bounce:
            self.bounce[t]=[tuple(self.direction)]
        else:
            if tuple(self.direction) in self.bounce[t]:
                self.loop=True
                return -1
            else:
                self.bounce[t].append(tuple(self.direction))
        if mirror=='/':
            self.direction[0],self.direction[1]=self.direction[1],self.direction[0]
            return 1
        elif mirror=="\\":
            self.direction[0],self.direction[1]=-self.direction[1],-self.direction[0]
            return 1
        
    def check_next(self,width,height):
        # checks if laser hit walls or not
        new_x_pos=self.position[0]+self.direction[0]
        new_y_pos=self.position[1]+self.direction[1]
        if  new_x_pos<0 or new_x_pos>width-1 or new_y_pos<0 or new_y_pos>height-1:
            return False
        else:
            return True
        
    def beam_counter(self):
        # return number of traversed squares
        return self.counter
    
    def output(self,outputfile,circle=False):
        # a handler function to output result of laser to outputfile
        file_handle=open(outputfile,'w')
        if not circle:
            file_handle.write(str(self.beam_counter())+'\n')
            file_handle.write(' '.join([str(x) for x in self.beam_pos()])+'\n')
        else:
            file_handle.write('-1')
        file_handle.close()
        
    def beam_path(self):
        # return path of laser in maze, will be used in visualization
        return self.path
    
    def isLoop(self):
        # checks if laser is trapped in a loop or not
        return self.loop

'''
A calss to manage maze, mirrors, and input and output files

'''
class maze_grid:
    def __init__(self,inputfile,outputfile):
        self.file_in=inputfile
        self.file_out=outputfile
        file_handle=open(self.file_in,'r')
        first_line=file_handle.readline().split()
        self.width=int(first_line[0])
        self.height=int(first_line[1])
        self.mirrors=dict()  # A dictionary to store mirrors location 
        second_line=file_handle.readline().split()
        self.player_pos=[int(second_line[0]),int(second_line[1])] # initial player position
        self.direction=second_line[2]
        start_pos=[self.player_pos[0],self.player_pos[1]]
        self.laser=beam(start_pos,self.direction) # A lazer beam is created (if one wants to create more than one lazer, it should be created outsid of the maze class)
        line=file_handle.readline().split()
        while line:
            mirror_cord=(int(line[0]),int(line[1]))
            if mirror_cord not in self.mirrors:
                self.mirrors[mirror_cord]=line[2]
            line=file_handle.readline().split()
            
    def fire(self):
        # starts maze and move laser to the next place
        while self.laser.check_next(self.width,self.height):
            self.laser.move_next()
            if tuple(self.laser.beam_pos()) in self.mirrors:
                mirror=self.mirrors[tuple(self.laser.beam_pos())]
                if self.laser.reflect(mirror)==-1:
                    self.laser.output(self.file_out,True)
                    return
        self.laser.output(self.file_out,False)
        
    # draw is just a simple helper drawer on command line env
    def draw(self):
        for h in range(self.height):
            print self.height-1-h,
            for w in range(self.width):
                p,q=w,self.height-1-h
                if (p,q) in self.mirrors:
                    print self.mirrors[(p,q)],
                else:
                    print 0,
            print
        print ' ',
        for w in range(self.width):
            print w,
        print
        
    # visualize function is a helper function to visualize maze with laser path
    def visualize(self):
        root = Tk()
        maze= make_maze(root,self.width,self.height,self.player_pos,
                        self.direction,self.mirrors,self.laser.beam_path(),
                        self.laser.isLoop())
        root.geometry(str(self.width*100+200)+'x'+str(self.height*50+200)+'+300+300')
        root.mainloop()

    def check_inputfile(self):
        # to check the format of input file
        if self.width>1000 or self.width<1 :
            print 'Error: width of maze out of range 1-1000'
            return False
        if self.height>1000 or self.height<1:
            print 'Error: height of maze out of range 1-1000'
            return False
        if len(self.mirrors) <0 or len(self.mirrors)>1000:
            print 'Error: number of mirrors out of range 0-1000'
            return False
        if tuple(self.player_pos) in self.mirrors:
            print 'Error: player and mirrors can not be in the same location'
            return False
        return True
        
####
        

def main():
    inputfile=sys.argv[1]
    outputfile=sys.argv[2]

    laser_maze=maze_grid(inputfile,outputfile)
    if laser_maze.check_inputfile():
        print ' maze is ready to play'
        laser_maze.draw()
        print 'lets fire'
        laser_maze.fire()
        laser_maze.visualize()
    else:
        print ' input file is not in the correct format'

if __name__ == '__main__':
    main()
    
