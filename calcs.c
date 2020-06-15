#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

int angle = 0;
int p_frame;

int chances[] = {7,85,93,100};

float matrix[4][3][4] = {{{ 0.0  , 0.00 ,  0.0,  0.0 },
                          { 0.0  , 0.16 , -0.1,  0.1 },
                          { 0.1  , 0.12 , 0.43, -0.1 }},
                         {{ 0.859, 0.04 , 0.0  ,  0.0 },
                          {-0.04 , 0.92 ,-0.1  , 1.6},
                          { 0.19 ,-0.13 , 0.72 , 1.8}},
                         {{ 0.2  , -0.26,  0  ,  0},
                          { 0.23 ,  0.22,  0.1 ,  1.6},
                          { 0.11 ,-0.3  ,  0.24,  1.5}},
                         {{-0.15 ,0.28 ,0,0} ,
                          {0.26  ,0.24 ,0.1   ,0.44},
                          {-0.20,-0.1  ,0.2   ,0.7}}};

float alter[4][3][4] =    {{{ .0 , .0  , .0  ,  .0 },
                            { .0  , .0 ,-.0  ,  .0 },
                            { .0  , .0 , .0 ,- .0 }},
                           {{.00, .1 , .0  ,  .2 },
                            {.0 , .0 ,-.0  , 0.0 },
                            { .0,-.0 , .0 , 0.0  }},
                           {{ .0  , -.0,  0  ,  0},
                            { .2 ,  .0,  .0 ,  0.0},
                            { .0 ,-.0  ,  .00,  0.0}},
                           {{-.00 ,0.00 ,0,0     } ,
                            {.00  ,0.00 ,.0   ,.0},
                            {-0.10,-.0  ,.1   ,.1}}};

_Bool is_prime(long x){
   if (x < 2)
     return 0;
   if (x == 2 || x == 3)
     return 1;
   long div = 2;
   if ((x %div) == 0)
     return 0;
   div ++;
   long max = (long)(sqrt(x));
   while (1){
     if (x%div == 0)
       return 0;
     if (div > max)
       return 1;
     div+=2;
   }}

void print_all(){
 printf("\ec");
 printf("\e[0;1H \t\t");
 for (int i =0; i < 4; i++)
   printf("%d  ", chances[i]);
 printf("\n");
 for (int k = 0; k < 4; k++)
   for (int j = 0; j < 3; j++)
    for (int i = 0; i < 4;i++)
     { if(alter[k][j][i]!=0)
          printf("\e[%d;%dH\e[31;1m%.2f\e[0m\n ",3+j+k*5,3+i*7, alter[k][j][i]);
       else
          printf("\e[%d;%dH%.2f \n",3+j+k*5,3+i*7, alter[k][j][i]);
       printf("\e[%d;%dH%.2f \n",3+j+k*5,40+i*7, matrix[k][j][i]);
     }
}

void reset(){
 for (int k = 0; k < 4; k++)
   for (int j = 0; j < 3; j++)
     for (int i = 0; i < 4;i++)
        alter[i][j][k] = 0;}

float rnd(float min, float max){
    return min + (rand() / (float) RAND_MAX) * ( max - min );   }

void randomize(){
  srand(time(NULL));
 for (int k = 0; k < 4; k++)
   for (int j = 0; j < 3; j++)
     for (int i = 0; i < 4;i++)
        alter[i][j][k] = rnd(-0.05,0.05);}

void hardreset(){
 srand(0);
 for (int k = 0; k < 4; k++)
   for (int j = 0; j < 3; j++)
     for (int i = 0; i < 4;i++)
        matrix[i][j][k] = ((float)(rand()%50)/100);
 for (int i =0; i < 3; i++)
   chances[i] = rand()%((i+1)*25);
 chances[3] = 100;
 print_all();}

void apply(){
 for (int k = 0; k < 4; k++)
   for (int j = 0; j < 3; j++)
     for (int i = 0; i < 4;i++)
        matrix[i][j][k] += alter[i][j][k]*sin(angle*M_PI/90);
 angle=0;
 randomize();
 print_all();}

void change_alter(unsigned char a, unsigned char b, unsigned char c, float d){
  alter[a][b][c] = d;
  print_all();}

void calc(const int num_points, float *data){
  srand(1);
  printf("\e[0;0HFrame %d\n",p_frame);
  data[0] = 0.0;
  data[1] = 0.0;
  data[2] = 0.0;
  unsigned char x,y;
  float f = sin(angle*M_PI/90);
  int new;
  float old_x, old_y, old_z;
  for(unsigned int i=1;i < num_points;i++){
    x = rand()%100;
    new = 3*i;
    old_x = data[3*(i-1)];
    old_y = data[3*(i-1)+1];
    old_z = data[3*(i-1)+2];
    if(x < chances[0])  y = 0;
    else if(x < chances[1]) y = 1;
    else if(x < chances[2]) y = 2;
    else       y = 3;
    data[new]   = old_x * matrix[y][0][0] + old_y * matrix[y][0][1] + old_z * matrix[y][0][2] + matrix[y][0][3]
                + (old_x * alter[y][0][0]  + old_y * alter[y][0][1]  + old_z * alter[y][0][2]  + alter[y][0][3]) * f;
    data[new+1] = old_x * matrix[y][1][0] + old_y * matrix[y][1][1] + old_z * matrix[y][1][2] + matrix[y][1][3]
                +(old_x * alter[y][1][0] + old_y * alter[y][1][1] + old_z * alter[y][1][2] + alter[y][1][3]) * f;
    data[new+2] = old_x * matrix[y][2][0] + old_y * matrix[y][2][1] + old_z * matrix[y][2][2] + matrix[y][2][3]
                +(old_x * alter[y][2][0] + old_y * alter[y][2][1] + old_z * alter[y][2][2] + alter[y][2][3]) * f;
  }
  angle++;
  p_frame++;
}