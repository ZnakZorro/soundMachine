import subprocess
import time
import pygame.mixer
from time import sleep
#import RPi.GPIO as GPIO
from sys import exit
import thread
#from thread import *
import random
from pprint import pprint
#import sys
#from os import walk
import glob

banki = ['ptaki','zwierzeta','piano1']

def loadBank(bankName):
	DS='/'
	bankPath = '/home/pi/voices/'
	pathBank   = bankPath+bankName+DS
	return sorted(glob.glob(pathBank+"*.wav"))


bank  = loadBank(banki[0])
#pprint(bank)	
stopMPD = subprocess.Popen(["mpc", "stop"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

pygame.init()
pygame.display.quit()
#self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.mixer.init(22050, -16, 1, 1024)

print("Sampler Ready.")

lastBank=8;
players=[]

for i in range(lastBank):
	players.append(lambda i: pygame.mixer.Channel(i).play(pygame.mixer.Sound(bank[i])))
pprint(players)

def playThread0():
	thread.start_new_thread(players[0], (0,))
def playThread1():
	thread.start_new_thread(players[1], (1,))
def playThread2():
	thread.start_new_thread(players[2], (2,))
def playThread3():
	thread.start_new_thread(players[3], (3,))
def playThread4():
	thread.start_new_thread(players[4], (4,))
def playThread5():
	thread.start_new_thread(players[5], (5,))
def playThread6():
	thread.start_new_thread(players[6], (6,))
def playThread7():
	thread.start_new_thread(players[7], (7,))


#time.sleep(2)
glosy = [playThread0,playThread1,playThread2,playThread3,playThread4,playThread5,playThread6,playThread7]

tempo = 40;
step=0

while True:
	try:
		step = (step+1)%100
		czas = (random.randint(1,5)*10) / tempo
		czas += (3*step/tempo)
		glos = random.choice (glosy)
		print(step,'czas',czas)	
		glos()
		sleep(czas)
	except KeyboardInterrupt:
		exit()
	  
#https://makezine.com/projects/make-33/simple-soundboard/
#https://my-little-piano-app.herokuapp.com/
#https://mrcoles.com/piano/	  
