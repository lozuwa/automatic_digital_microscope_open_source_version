# Author: Khalil Nallar
# Company: pfm medical
# Description: Supporting functions for microscope movement

import serial
import os, sys, time
from multiprocessing import Process

# Global variables
s = serial.Serial('/dev/ttyACM1',115200)
c = 0
TIME_HOME = 200

def x_s(pasos,dir,time_):
	s.write(('x,'+str(pasos)+','+str(dir)+','+str(time_)).encode())
	time.sleep(0.01)

def y_s(pasos,dir,time_):
	s.write(('y,'+str(pasos)+','+str(dir)+','+str(time_)).encode())
	time.sleep(0.01)

def z_s(pasos,dir,time_):
	s.write(('z,'+str(pasos)+','+str(dir)+','+str(time_)).encode())
	time.sleep(0.01)

def brigthness(b):
	s.write(('l,'+str(0)+','+str(0)+','+str(0)+','+str(b)).encode())
	time.sleep(0.01)

def auto(time_):
	y_s(2000,1,time_)
	time.sleep(3)
	for i in range(10):
		time.sleep(0.5)
		y_s(2000,0,time_)
		time.sleep(5)
		x_s(30,1,time_)
		time.sleep(0.5)
		y_s(2000,1,time_)
		time.sleep(5)
		x_s(30,1,time_)

def exit():
	s.close()

def proc_H_y():
    while(1):
        s.write(('y,'+str(20)+','+str(0)+','+str(500)).encode())
        time.sleep(0.01)

def proc_H_x():
    while(1):
        s.write(('x,'+str(20)+','+str(1)+','+str(500)).encode())
        time.sleep(0.01)

H_y_ = Process(target=proc_H_y)
H_x_ = Process(target=proc_H_x)

def home():
	global H_y_
	global H_x_
	global c
	c=0
	z_s(5000,0,TIME_HOME)
	time.sleep(3.5)
	H_y_.start()
	print('zs ...')
	if (s.readline()[0]==121):
		H_y_.terminate()
	H_y_ = Process(target=proc_H_y)
	time.sleep(0.05)
	H_x_.start()
	if (s.readline()[0]==120):
		time.sleep(0.05)
		H_x_.terminate()
	H_x_ = Process(target=proc_H_x)
	time.sleep(0.5)
	x_s(3000,0,TIME_HOME)
	time.sleep(2.5)
	y_s(1500,1,TIME_HOME)
	time.sleep(4)
	z_s(5000,1,TIME_HOME)
	time.sleep(5)

def change(dir):
        global c
        campos = 30
        if dir == 0:
            c -= 1
            if c < campos:
                y_s(80,0,2500)
            elif c == campos:
                x_s(60,0,5000)
            elif c > campos and c < campos*2:
                y_s(80,1,2500)
            elif c == campos*2:
                x_s(90,0,5000)
                c = 0
        elif dir:
            c += 1
            if c < campos:
                y_s(80,1,2500)
            elif c == campos:
                x_s(60,1,5000)
            elif c > campos and c < campos*2:
                y_s(80,0,2500)
            elif c == campos*2:
                x_s(90,1,5000)
                c = 0
