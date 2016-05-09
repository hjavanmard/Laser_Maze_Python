import sys
from kinter import *
class beam:
    def __init__(self,position,direction):
        self.position=position
        self.next={'S':[0,-1],'N':[0,1],'E':[1,0],'W':[-1,0]}
        self.direction=self.next[direction]
        self.counter=0
        self.bounce=dict()
        self.path=[[position[0],position[1]]]
        self.loop=False
    def update_pos(self,position):
        self.position=position
    def beam_pos(self):
        return self.position
    def move_next(self):
        self.position[0] +=self.direction[0]
        self.position[1] +=self.direction[1]
        self.path.append([self.position[0],self.position[1]])
        self.counter +=1
    def reflect(self,mirror):
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
        new_x_pos=self.position[0]+self.direction[0]
        new_y_pos=self.position[1]+self.direction[1]
        print self.position
        if  new_x_pos<0 or new_x_pos>width-1 or new_y_pos<0 or new_y_pos>height-1:
            return False
        else:
            return True
    def beam_counter(self):
        return self.counter
    def output(self,outputfile,circle=False):
        file_handle=open(outputfile,'w')
        if not circle:
            file_handle.write(str(self.beam_counter())+'\n')
            file_handle.write(' '.join([str(x) for x in self.beam_pos()])+'\n')
        else:
            file_handle.write('-1')
        file_handle.close()
    def beam_path(self):
        return self.path
    def isLoop(self):
        return self.loop
        
class maze_grid:
    def __init__(self,inputfile,outputfile):
        self.file_in=inputfile
        self.file_out=outputfile
        file_handle=open(self.file_in,'r')
        first_line=file_handle.readline().split()
        self.width=int(first_line[0])
        self.height=int(first_line[1])
        self.mirrors=dict()
        second_line=file_handle.readline().split()
        self.player_pos=[int(second_line[0]),int(second_line[1])]
        self.direction=second_line[2]
        start_pos=[self.player_pos[0],self.player_pos[1]]
        self.laser=beam(start_pos,self.direction)
        line=file_handle.readline().split()
        while line:
            mirror_cord=(int(line[0]),int(line[1]))
            if mirror_cord not in self.mirrors:
                self.mirrors[mirror_cord]=line[2]
            line=file_handle.readline().split()
            
    def fire(self):
        while self.laser.check_next(self.width,self.height):
            print 'x'
            self.laser.move_next()
            if tuple(self.laser.beam_pos()) in self.mirrors:
                mirror=self.mirrors[tuple(self.laser.beam_pos())]
                if self.laser.reflect(mirror)==-1:
                    self.laser.output(self.file_out,True)
                    return
        self.laser.output(self.file_out,False)
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
    def visualize(self):
        root = Tk()
        maze= make_maze(root,self.width,self.height,self.player_pos,
                        self.direction,self.mirrors,self.laser.beam_path(),
                        self.laser.isLoop())
        root.geometry(str(self.width*100+200)+'x'+str(self.height*50+200)+'+300+300')
        root.mainloop()
        


def main():
    inputfile=sys.argv[1]
    outputfile=sys.argv[2]

    laser_maze=maze_grid(inputfile,outputfile)
    print ' maze is ready to play'
    laser_maze.draw()
    print 'lets fire'
    laser_maze.fire()
    laser_maze.visualize()

if __name__ == '__main__':
    main()
    
