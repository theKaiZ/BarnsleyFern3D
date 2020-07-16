#include <GL/glut.h>
#include <GL/freeglut.h>
#include <complex.h>
#include <math.h>
#include <cstdio>
#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
//compile with g++ new.cpp -lGL -lglut -lGLU

unsigned short int WIDTH = 720;
unsigned short int HEIGHT = 720;
unsigned char angle = 0;
unsigned int frame = 0;
int num_points = 10000;
unsigned char save = 0;
const int MAX_FRAME = 360;
GLubyte* PixelBuffer = new GLubyte[WIDTH * HEIGHT * 3];
static GLubyte *pixels = NULL;

#include "drawables.h"

void init(int argc, char** argv)
{
  glutInit(&argc, argv);
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
  glutInitWindowSize(WIDTH, HEIGHT);
  glutCreateWindow("Introduction to OpenGL");
  glEnable(GL_DEPTH_TEST);
}

void handleResize(int w, int h) 
{
  glViewport(0, 0, w, h);
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluPerspective(45.0,(double)w / (double)h,  1.0, 200.0);
}


void saveScreenshotToFile() {    
    const int numberOfPixels = WIDTH * HEIGHT * 3;
    unsigned char pixels[numberOfPixels];
    glPixelStorei(GL_PACK_ALIGNMENT, 1);
    glReadBuffer(GL_FRONT);
    glReadPixels(0, 0, WIDTH, HEIGHT, GL_BGR_EXT, GL_UNSIGNED_BYTE, pixels);
    char filename[128];
    snprintf(filename, 128,"tmp/pic%.4d.tga",frame);
    FILE *outputFile = fopen(filename, "w");
    short header[] = {0, 2, 0, 0, 0, 0, (short) WIDTH, (short) HEIGHT, 24};
    fwrite(&header, sizeof(header), 1, outputFile);
    fwrite(pixels, numberOfPixels, 1, outputFile);
    fclose(outputFile);
    printf("Finish writing to file %d.\n",frame);
}

void draw()
{
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glMatrixMode(GL_MODELVIEW);
  glLoadIdentity(); 
  glTranslatef(0.0f, 0.0f, -8.0f);
  glRotatef(frame,0,1,0);
  draw_fern(num_points);
  glutSwapBuffers();
  if (save)
    saveScreenshotToFile();
  if(frame++==MAX_FRAME && MAX_FRAME != 0)
    glutLeaveMainLoop();
}

int main(int argc, char** argv) {
	init(argc, argv);
	glutDisplayFunc(draw);
        glutIdleFunc(draw);
	glutReshapeFunc(handleResize);
	
	glutMainLoop();
	return 0;
}
