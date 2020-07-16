from os import system
from time import time

system("g++ new.cpp -lGL -lglut -lGLU")
t = time()
system("./a.out")
print(time()-t)

