from numba import jit
import os
from math import sin,pi,cos
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from random import random,seed
import numpy as np

@jit
def farbe(x,y,z,frame):
    return 0.6+(sin((x*y+frame/2)*pi/30)+1)*0.4,0.3+(cos((y+x+frame/3)*pi/5)+1)*0.25,0.7+(sin(x*z*pi/18)+1)*0.2

@jit
def sin90(val):
    return sin(val*pi/90)

class Animation():
    def __init__(self,frames= 360, max = 1000, save=False):
        self.num_frames = frames
        self.save = save
        pygame.init()
        self.max_points = max
        self.frame = 0
        self.size = (800,800)
        self.screen = pygame.display.set_mode(self.size, DOUBLEBUF|OPENGL)
        gluPerspective(45, (self.size[0]/self.size[1]), 0.1, 50.0)
        glEnable(GL_DEPTH_TEST)
        self.zoom()
        self.running = True
        self.pts = [[.0, .0, .0]]
        self.set_matrices()
        self.mainloop()
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
        a = random() * 100
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
        for j in range(self.max_points):
            self.add_point()

    def draw(self):
        glPointSize(1.0)
        glBegin(GL_POINTS)
        for point in self.pts:
            glColor(farbe(point[0], point[1], point[2], self.frame))
            glVertex3d(point[0] - 0, point[1] - 0, point[2] - 0)
        glEnd()

    def checkpoint(self):
        pass
  
    def mainloop(self):
        while self.running and self.frame < self.num_frames:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            self.checkpoint()
            glRotatef(1, 1, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
            self.make_points()
            self.draw()
            if len(self.pts) %250 == 0:
                print(len(self.pts))
            if not os.path.exists("pics/"):
                os.mkdir("pics/")
            if self.save:
              pygame.image.save(self.screen, "pics/" + "0" * (3 - len(str(self.frame))) + str(self.frame) + ".png")
            print(self.frame)

            pygame.display.flip()
            self.frame += 1
        pygame.quit()
        if self.running and self.save:
            os.system("ffmpeg -f image2 -i ./pics/%03d.png -pix_fmt yuv420p -y "+self.__class__.__name__+".mp4")
            os.system("vlc --no-repeat --play-and-exit "+self.__class__.__name__+".mp4")

class Anim2(Animation):
    def zoom(self):
        glTranslatef(0.0, -0.0, -12)
    def set_matrices(self):
        self.chances = [5, 86, 93, 100]
        self.matrix = np.array([[[.0, .0, .0, .0],
                                 [.0, .16, -.1, .1],
                                 [-.1, .12, .43, - .1]],  ###Ende Array 1
                                [[.85, .075, -.225, -.0],
                                 [-.24, .88, -.03, 1.7],
                                 [.175, -.115, .07, 1.8]],  # Ende Array 2
                                [[.14, -.26, -0.1, 0],
                                 [.14, .22, .1, 1.6],
                                 [-.11, -.04, .24, 1.5]],  # Ende Array 3
                                [[-.15, 0.28, 0, 0],
                                 [.206, 0.24, .1, .44],
                                 [-0.20, -.1, .2, .7]]])  # Ende Array 4
        #                          x     y     z      n
        self.alter = np.array([[[.00, .0, .00, .0],
                                [.002, .02, -.0, .0],
                                [.0, .0, .05, - .0]],  ###Ende Array 1
                               [[.02, .04, .0, .0],
                                [+.03, .06, -.0, 0.0],
                                [.17, -.0, .06, 0.0]],  # Ende Array 2
                               [[.075, -.0, 0.2, .10],
                                [.1, .1, .0, 0.0],
                                [.1, -.2, -.100, 0.0]],  # Ende Array 3
                               [[-.30, 0.10, 0.1, 0],
                                [.02, 0.00, .05, .00],
                                [-0.10, -.0, .05, .02]]])  #Ende Array 4)


    def checkpoint(self):
        if self.frame == 360:
          self.alter = np.array([[[ .0 , .0  , .0  ,  .0 ],
                                  [ .0  , .03 ,-.02  ,  .0 ],
                                  [ .0  , .0 , .0 ,- .0 ]],###Ende Array 1
                                 [[.04, .0 , .04  ,  .06 ],
                                  [+.0 , .05 ,-.0  , 0.03],
                                  [ .05 ,-.0 , .0 , 0.08]],# Ende Array 2
                                 [[ .03  , -.0,  0  ,  0],
                                  [ .0 ,  .0,  .0 ,  0.0],
                                  [ .0 ,-.0  ,  .00,  0.0]],#Ende Array 3
                                 [[-.00 ,0.03 ,0,0] ,
                                  [.00  ,0.00 ,.0   ,.00],
                                  [-0.00,-.0  ,.0   ,.0]]])#Ende Array 4)
    def draw(self):
        glPointSize(1.0)
        glBegin(GL_POINTS)
        for point in self.pts:
            glColor(farbe(point[0], point[1], point[2], self.frame))
            glVertex3d(point[0]*0.3 - 0, point[1]*0.3 - 0, point[2] *0.3- 0)
            glVertex3d(-point[0]*0.3 - 0, -point[1] *0.3 - 0, -point[2] *0.3- 0)
            glVertex3d(-point[0] * 0.3 - 0, point[1] * 0.3 - 0, -point[2] * 0.3 - 0)
            glVertex3d(point[0] * 0.3 - 0, -point[1] * 0.3 - 0, point[2] * 0.3 - 0)
        glEnd()


class Flower(Anim2):
    def zoom(self):
        glTranslatef(0.0, -.0, -12)
    def set_matrices(self):
        self.chances = [5, 86, 93, 100]
        self.matrix = np.array([[[ .0  , .0  , .0  ,  .0 ],
                                  [ .0  , .16 ,-.1  ,  .1 ],
                                  [ .1  , .12 , .43 ,- .1 ]],###Ende Array 1
                                 [[ .87, .075 ,-.225  ,  -.0 ],
                                  [-.24 , .89 ,-.03  , 1.7],
                                  [ .175 ,-.115 , .07 , 1.8]],# Ende Array 2
                                 [[ .14  , -.26, -0.1  ,  0],
                                  [ .14 ,  .22,  .1 ,  1.6],
                                  [-.11 ,-.04 ,  .24,  1.5]],#Ende Array 3
                                 [[-.15 ,0.28 ,0,0] ,
                                  [.206  ,0.24 ,.1   ,.44],
                                  [-0.20,-.1  ,.2   ,.7]]])#Ende Array 4
        #                          x     y     z      n
        self.alter = np.array([[[ .0 , .0  , .0  ,  .0 ],
                                  [ .0  , .0 ,-.0  ,  .0 ],
                                  [ .0  , .0 , .0 ,- .0 ]],###Ende Array 1
                                 [[.00, .07 , .0  ,  .0 ],
                                  [+.0 , .08 ,-.0  , 0.0],
                                  [ .0 ,-.0 , .06 , 0.0]],# Ende Array 2
                                 [[ .0  , -.0,  0  ,  0],
                                  [ .0 ,  .0,  .0 ,  0.0],
                                  [ .0 ,-.0  ,  .00,  0.0]],#Ende Array 3
                                 [[-.00 ,0.00 ,0,0] ,
                                  [.00  ,0.00 ,.0   ,.00],
                                  [-0.00,-.0  ,.0   ,.0]]])#Ende Array 4)

Flower(360,3000)


