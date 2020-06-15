from numba import jit
import os
from math import sin,pi,cos
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import random,seed
import numpy as np
from time import time,sleep
from ctypes import *
from math import sin

@jit
def farbe(x,y,z,frame):
    return 0.6+(sin((x*y+frame/2)*pi/30)+1)*0.4,0.3+(cos((y+x+frame/3)*pi/5)+1)*0.25,0.7+(sin(x*z*pi/18)+1)*0.2

@jit
def sin90(val):
    return sin(val*pi/90)

class Animation():
    video = 0
    frame = 0
    size = (800,800)
    p_max = 10000
    save = False
    f_max = 360
    running = True
    color = False
    pt_size = 1
    def __init__(self, **kwargs):
        for key in kwargs:
            setattr(self,key,kwargs[key])
        os.system("rm -r pics/")
        pygame.init()
        self.screen = pygame.display.set_mode(self.size, DOUBLEBUF|OPENGL)
        gluPerspective(45, (self.size[0]/self.size[1]), 0.1, 50.0)
        glEnable(GL_DEPTH_TEST)
        self.zoom()
        self.pts = [[.0, .0, .0]]
        self.set_matrices()
        self.after_init()
        self.mainloop()

    def after_init(self):
        pass

    def zoom(self):
        glTranslatef(0.0, -8.0, -21)

    def set_matrices(self):
        self.chances = [5,86,93,100]
        #the initial matrix to create the static barnsley fern
        #                          x     y     z     n
        self.matrix = np.array([[[ .0  , .0  , .0  ,  .0 ],
                                  [ .0  , .16 ,-.1  ,  .1 ],
                                  [ .1  , .12 , .43 ,- .1 ]],###Ende Array 1
                                 [[ .859, .04 , .0  ,  .0 ],
                                  [-.04 , .92 ,-.1  , 1.6],
                                  [ .19 ,-.13 , .72 , 1.8]],# Ende Array 2
                                 [[ .2  , -.26,  0  ,  0],
                                  [ .23 ,  .22,  .1 ,  1.6],
                                  [ .11 ,-.3  ,  .24,  1.5]],#Ende Array 3
                                 [[-.15 ,0.28 ,0,0] ,
                                  [.26  ,0.24 ,.1   ,.44],
                                  [-0.20,-.1  ,.2   ,.7]]])#Ende Array 4
        #this matrix causes the 'movement' of the fern by altering the stats of the standard matrix depending on the frame, check the calculations in self.add_point()
        #                          x     y     z      n
        self.alter = np.array([[[ .0  , .0  , .0  ,  .0 ],
                                  [ .0  , .1 ,-.0  ,  .1 ],
                                  [ .1  , .0 , .0 ,- .0 ]],###Ende Array 1
                                 [[ .1, .0 , .0  ,  .0 ],
                                  [-.0 , .0 ,-.0  , 0.0],
                                  [ .0 ,-.0 , .0 , 0.0]],# Ende Array 2
                                 [[ .0  , -.0,  0  ,  0],
                                  [ .0 ,  .0,  .0 ,  0.0],
                                  [ .0 ,-.0  ,  .00,  0.0]],#Ende Array 3
                                 [[-.00 ,0.00 ,0,0] ,
                                  [.00  ,0.00 ,.0   ,.00],
                                  [-0.00,-.0  ,.0   ,.0]]])#Ende Array 4)

    def add_point(self):
        a  = random() * 100
        old_point = self.pts[-1]
        new_point = []
        for i in range(len(self.chances)):
           if a <= self.chances[i]:
             used = self.matrix[i]
             alt = self.alter[i]
             break
        for i in range(len(used)):
            new_point.append(old_point[0] * used[i][0] + sin90(self.frame) * alt[i][0] *old_point[0]
                           + old_point[1] * used[i][1] + sin90(self.frame) * alt[i][1] *old_point[1]
                           + old_point[2] * used[i][2] + sin90(self.frame) * alt[i][2] *old_point[2]
                           + used[i][3]                + sin90(self.frame) * alt[i][3]          )

        self.pts.append(new_point)

    def make_points(self):
        self.pts = [[.0, .0, .0]]
        seed(0)
        for j in range(self.p_max):
            self.add_point()

    def draw(self):
        glPointSize(self.pt_size)
        glBegin(GL_POINTS)
        if not self.color:
           glColor(farbe(self.pts[0][0], self.pts[0][1], self.pts[0][2], self.frame))
        for point in self.pts:
            if self.color:
               glColor(farbe(self.pts[0][0], self.pts[0][1], self.pts[0][2], self.frame))
            glVertex3d(point[0] - 0, point[1] - 0, point[2] - 0)
        glEnd()
        
    def checkpoint(self):
        pass

    def save_frame(self):
        pygame.image.save(self.screen, "pics/" + "0" * (3 - len(str(self.frame))) + str(self.frame) + ".png")

    def rotation(self):
        glRotatef(1, 1, 2, 1)

    def mainloop(self):
        while self.running and (self.frame < self.f_max or self.f_max == 0):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_a:
                        self.c_calcs.apply(c_int(self.frame))
                        self.frame = 359
                        self.c_calcs.reset()
                    elif event.key == pygame.K_v:
                        self.video = True
                        self.running  = False
                    elif event.key == pygame.K_DOWN:
                        glTranslatef(0.0, 0, -0.1)
                    elif event.key == pygame.K_UP:
                        glTranslatef(0.0, 0, 0.1)
            self.checkpoint()
            self.rotation()
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.make_points()
            self.draw()
            if len(self.pts) %250 == 0:
                print(len(self.pts))
            if not os.path.exists("pics/"):
                os.mkdir("pics/")
            if self.save:
              self.save_frame()
            pygame.display.flip()
            self.frame += 1
        pygame.quit()
        if (self.save and self.running) or self.video:
            os.system("ffmpeg -f image2 -i ./pics/%03d.png -pix_fmt yuv420p -y "+self.__class__.__name__+".mp4")
            os.system("vlc --no-repeat --play-and-exit "+self.__class__.__name__+".mp4")

class C_Animation(Animation):
    a = 0
    b = 0
    c = 0
    pp = 0
    def zoom(self):
        '''The inititial Zoom perspective, go not to far!'''
        glTranslatef(0.0, -0, -40)

    def after_init(self):
       '''Compile the C-code and load the library with ctypes'''
       os.system("gcc -shared -o calcs.so -lm -fPIC calcs.c")
       sleep(2)
       LibName = 'calcs.so'
       AbsLibPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + LibName
       self.c_calcs = CDLL(AbsLibPath)
       self.result = (c_float*(3*self.p_max))()

    def make_points(self):
        '''In this case, call the ctypes library to calc the points'''
        self.c_calcs.calc(c_int(self.p_max),self.result)

    def rotation(self):
        glRotatef(1, 1, 1, 1)

    def draw(self):
        glPointSize(self.pt_size)
        glBegin(GL_POINTS)
        glColor((0.3+sin(self.pp*pi/180)*0.2, 0.4+0.2*sin(self.pp*pi/90), 0.7+0.25*sin(self.pp*pi/80)))
        for x,y,z in zip(self.result[0::3],self.result[1::3],self.result[2::3]):
           glVertex3d(x,y,z)
        glEnd()
    def save_frame(self):
        pygame.image.save(self.screen, "pics/" + "0" * (3 - len(str(self.pp))) + str(self.pp) + ".png")
        
    def checkpoint(self):
       if self.c_calcs.is_prime(c_long(self.pp)):
          self.c_calcs.apply()     
       self.pp +=1
 
class C_Flower(C_Animation):
    def zoom(self):
        glTranslatef(0.0, -0.0, -25)

    def draw(self):
        glPointSize(self.pt_size)
        glBegin(GL_POINTS)
        if not self.color:
            glColor((0.3+sin(self.pp*pi/360)*0.2, 0.4+0.2*cos(self.pp*pi/360), 0.7+0.25*sin(self.pp*pi/720)))  
        #zip the arguments, i hoped it was faster than the basic iteration
        for x,y,z in zip(self.result[0::3],self.result[1::3],self.result[2::3]):
            if self.color:
                glColor((0.3+sin(x+self.pp*pi/360)*0.2, 0.4+0.2*cos(y+self.pp*pi/360), 0.7+0.25*sin(z+self.pp*pi/720)))  
            glVertex3d(x,y,z)
            glVertex3d(-x,y,z)
            glVertex3d(x,-y,z)
            glVertex3d(-x,-y,z)
        glEnd()

def demo():
   C_Flower(f_max = 0, p_max = 10000,pt_size = 1, color=False)


if __name__ == '__main__':
    demo()
