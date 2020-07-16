double fRand()
{ 
    double fMin = -1;
    double fMax = 1;
    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}

extern "C"{
  unsigned char chances[] = {10,85,93,100};
  double matrix[4][3][4] = {{{ 0.0  , 0.00 ,  0.0,  0.0 },
                          { 0.0  , 0.16 , -0.1,  -0.2 },
                          { 0.1  , 0.12 , 0.43, -0.1 }},
                         {{ 0.889, 0.04 , 0.0  ,  0.0 },
                          {-0.08 , 0.92 ,-0.1  , 1.6},
                          { 0.19 ,-0.13 , 0.72 , 1.8}},
                         {{ 0.2  , -0.16,  0  ,  0},
                          { 0.23 ,  0.22,  0.1 ,  1.6},
                          { 0.11 ,-0.3  ,  0.24,  1.5}},
                         {{-0.15 ,0.28 ,0,0} ,
                          {0.26  ,0.24 ,0.1   ,0.44},
                          {-0.20,-0.1  ,0.2   ,0.7}}};

  double alter[4][3][4] =    {{{ .0 , .0  , .0  ,  .0 },
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
  void draw_fern(const int num_points){
    srand(1);
    glBegin(GL_POINTS);
    double old[3];
    old[0] = 0.0;
    old[1] = 0.0;
    old[2] = 0.0;
    unsigned char x,y;
    double f = sin(angle*M_PI/90);
    double old_x, old_y, old_z;
    for(unsigned int i=1;i < num_points;i++){
      x = rand()%100;
      old_x = old[0];
      old_y = old[1];
      old_z = old[2];
      if(x < chances[0])  y = 0;
      else if(x < chances[1]) y = 1;
      else if(x < chances[2]) y = 2;
      else       y = 3;
      old[0]   = old_x * matrix[y][0][0] + old_y * matrix[y][0][1] + old_z * matrix[y][0][2] + matrix[y][0][3]
              + (old_x * alter[y][0][0]  + old_y * alter[y][0][1]  + old_z * alter[y][0][2]  + alter[y][0][3]) * f;
      old[1] = old_x * matrix[y][1][0] + old_y * matrix[y][1][1] + old_z * matrix[y][1][2] + matrix[y][1][3]
              +(old_x * alter[y][1][0] + old_y * alter[y][1][1] + old_z * alter[y][1][2] + alter[y][1][3]) * f;
      old[2] = old_x * matrix[y][2][0] + old_y * matrix[y][2][1] + old_z * matrix[y][2][2] + matrix[y][2][3]
              +(old_x * alter[y][2][0] + old_y * alter[y][2][1] + old_z * alter[y][2][2] + alter[y][2][3]) * f;
      glColor3f(old[0]*0.2,old[1]*0.2,old[2]*0.2);
      glVertex3f(old[0]*0.2,old[1]*0.2,old[2]*0.2);
    }
    angle++;
    if(angle > 180)
    angle -= 180;
    glEnd();}}
