from Tkinter import Tk, Canvas, Frame, BOTH

class make_maze(Frame):
  
    def __init__(self, parent,width,height,player_pos,direction,mirrors_loc,lazer_path,isLoop):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.width=width
        self.height=height
        self.space=50
        self.offset=10
        self.origin=[300,self.height*self.space]
        self.person=player_pos
        self.direction=direction
        self.mirror=mirrors_loc
        self.path=lazer_path
        self.loop=isLoop
        self.initUI()
        
    def findCenter(self,i,j):
        return [self.origin[0]+self.space*i+self.space/2,self.origin[1]-self.space*j-self.space/2]
    def draw_smileMan(self,canvas,center):
        r=self.space/3
        canvas.create_oval(center[0]-r,center[1]-r,center[0]+r,center[1]+r,
                          outline="black")
        
        rEyes=r/5
        Xoffset=r/2
        Yoffset=r/2
        #left eye
        canvas.create_oval(center[0]-Xoffset-rEyes,center[1]-Yoffset-rEyes,
                           center[0]-Xoffset+rEyes,center[1]-Yoffset+rEyes,
                            outline="black")
        #right eye
        canvas.create_oval(center[0]+Xoffset-rEyes,center[1]-Yoffset-rEyes,
                           center[0]+Xoffset+rEyes,center[1]-Yoffset+rEyes,
                            outline="black")
        #smile
        canvas.create_arc(center[0]+r/2,center[1]+r/2,
                          center[0]-r/2,center[1]-r/2,start=180,extent=180,style='arc')
    def initUI(self):
      
        self.parent.title("maze")        
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)

        # labels for x axis
        for i in range(self.width):
            canvas.create_text(self.origin[0]+self.space*i+self.space/2,
                               self.origin[1]+self.space/3,text=str(i))
        canvas.create_text(self.origin[0]+self.width*self.space/2, self.origin[1]+self.space,text='x')
        # labels for y axis
        for j in range(self.height):
            canvas.create_text(self.origin[0]+self.space*self.height-self.space/2,
                               self.origin[1]-self.space*j-self.space/2,text=str(j))
        canvas.create_text(self.origin[0]-self.space/2,
                           self.origin[1]-self.space*self.height/2-self.space/2,text='y')
        # create grid and mirrors
        for i in range(self.width):
            for j in range(self.height):
                canvas.create_rectangle(self.origin[0]+self.space*i, self.origin[1]-self.space*j,
                                        self.origin[0]+self.space*(i+1),self.origin[1]-self.space*(j+1),
                                        outline="black", fill="#fb1")
                if (i,j) in self.mirror:
                    if self.mirror[(i,j)]=='/':
                        canvas.create_line(self.origin[0]+self.space*i+self.offset,
                                           self.origin[1]-self.space*j-self.offset,
                                           self.origin[0]+self.space*(i+1)-self.offset,
                                           self.origin[1]-self.space*(j+1)+self.offset)
                    else:
                        canvas.create_line(self.origin[0]+self.space*(i+1)-self.offset,
                                           self.origin[1]-self.space*j-self.offset,
                                           self.origin[0]+self.space*i+self.offset,
                                           self.origin[1]-self.space*(j+1)+self.offset)
        # create smile face for person
        center=self.findCenter(self.person[0],self.person[1])
        r=self.space/3
        self.draw_smileMan(canvas,center)
        # add person direction
        if self.direction=='S':
            canvas.create_line(center[0]+r+2,center[1]-r,center[0]+r+2,center[1]+r,arrow='last')
        elif self.direction=='N':
            canvas.create_line(center[0]+r+2,center[1]-r,center[0]+r+2,center[1]+r,arrow='first')
        elif self.direction=='E':
            canvas.create_line(center[0]-r,center[1]+r+2,center[0]+r,center[1]+r+2,arrow='last')
        else:
            canvas.create_line(center[0]-r,center[1]+r+2,center[0]+r,center[1]+r+2,arrow='first')
        # add directions
        canvas.create_line(self.origin[0]-3*self.space,self.origin[1]-self.height*self.space/2,
                           self.origin[0]-2*self.space,self.origin[1]-self.height*self.space/2,
                           arrow='last')
        canvas.create_text(self.origin[0]-5*self.space/2,self.origin[1]-self.height*self.space/2+5,
                           text='East')
        
        canvas.create_line(self.origin[0]-3*self.space,self.origin[1]-self.height*self.space/2,
                           self.origin[0]-3*self.space,self.origin[1]-self.height*self.space/2+self.space,
                           arrow='last')
        canvas.create_text(self.origin[0]-3*self.space,self.origin[1]-self.height*self.space/2+self.space+2,
                           text='South')
        
        canvas.create_line(self.origin[0]-3*self.space,self.origin[1]-self.height*self.space/2,
                           self.origin[0]-4*self.space,self.origin[1]-self.height*self.space/2,
                           arrow='last')
        canvas.create_text(self.origin[0]-7*self.space/2,self.origin[1]-self.height*self.space/2+5,
                           text='West')
        
        canvas.create_line(self.origin[0]-3*self.space,self.origin[1]-self.height*self.space/2,
                           self.origin[0]-3*self.space,self.origin[1]-self.height*self.space/2-self.space,
                           arrow='last')
        canvas.create_text(self.origin[0]-3*self.space,self.origin[1]-self.height*self.space/2-self.space-2,
                           text='North')
        # add path of lazer beam
        for indx,item in enumerate(self.path):
              if indx==0:
                  person_start=item
              elif indx==1:
                  previous=item
                  first=self.findCenter(person_start[0],person_start[1])
                  second=self.findCenter(item[0],item[1])
                  mid=[(first[0]+second[0])/2.0,(first[1]+second[1])/2.0]
                  canvas.create_line(mid[0],mid[1],second[0],second[1],
                                 fill='red',dash=(4,2))
              else:
                  first=self.findCenter(previous[0],previous[1])
                  second=self.findCenter(item[0],item[1])                      
                  canvas.create_line(first[0],first[1],second[0],second[1],
                                 fill='red',dash=(4,2))
              if indx>0 and indx==len(self.path)-1 and not self.loop:
                  first=self.findCenter(previous[0],previous[1])
                  second=self.findCenter(item[0],item[1])
                  diff=[second[0]-first[0],second[1]-first[1]]
                  end=[second[0]+diff[0]/2.0,second[1]+diff[1]/2.0]
                  canvas.create_line(second[0],second[1],end[0],end[1],
                                 fill='red',dash=(4,2))

                  hit=[end[0]-diff[0]/8,end[1]-diff[1]/8]
                  canvas.create_oval(hit[0]-self.space/10,hit[1]-self.space/10,
                                         hit[0]+self.space/10,hit[1]+self.space/10,fill='red',
                                         outline='black')
              previous=item
        
        canvas.pack(fill=BOTH, expand=1)


##def visualize():
##    width=5
##    height=6
##    person=[1,4]
##    direction='S'
##    mirror={(3,4):'/',(3,2):'\\',(3,0):'/',(1,2):'\\'}
##    path=[(1,4),(1,3),(1,2),(2,2),(3,2),(3,1),(3,0),(2,0),(1,0),(0,0)]
##    root = Tk()
##    maze= make_maze(root,width,height,person,direction,mirror,path)
##    root.geometry(str(width*100+200)+'x'+str(height*50+200)+'+300+300')
##    root.mainloop()  
##
##
##if __name__ == '__main__':
##    visualize()  
