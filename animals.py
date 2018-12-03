import subprocess
import time
import pygame.mixer
from time import sleep
#import RPi.GPIO as GPIO
from sys import exit
import thread
#from thread import *
import random
#from pprint import pprint
#import sys

stopMPD = subprocess.Popen(["mpc", "stop"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

pygame.init()
pygame.display.quit()
#self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)


pygame.mixer.init(22050, -16, 1, 1024)

pliki0=[
'/home/pi/pygame/animals/kot.wav',
'/home/pi/pygame/animals/pies.wav',
'/home/pi/pygame/animals/krowa.wav',
'/home/pi/pygame/animals/kura.wav',
'/home/pi/pygame/animals/kon.wav'
]


pliki=[
'/home/pi/pygame/animals/ptaki/wav/slowik1.wav',
'/home/pi/pygame/animals/ptaki/wav/slowik2.wav',
'/home/pi/pygame/animals/ptaki/wav/slowik3.wav',
'/home/pi/pygame/animals/ptaki/wav/puchacz.wav',
'/home/pi/pygame/animals/ptaki/wav/puszczyk.wav',
'/home/pi/pygame/animals/ptaki/wav/bogatka.wav',
'/home/pi/pygame/animals/ptaki/wav/kos.wav',
'/home/pi/pygame/animals/ptaki/wav/kos2.wav',
]

sndA = pygame.mixer.Sound(pliki[0])
sndB = pygame.mixer.Sound(pliki[1])
sndC = pygame.mixer.Sound(pliki[2])
sndD = pygame.mixer.Sound(pliki[3])
sndE = pygame.mixer.Sound(pliki[4])
sndF = pygame.mixer.Sound(pliki[5])
sndG = pygame.mixer.Sound(pliki[6])
sndH = pygame.mixer.Sound(pliki[7])


soundChannelA = pygame.mixer.Channel(0)
soundChannelB = pygame.mixer.Channel(1)
soundChannelC = pygame.mixer.Channel(2)
soundChannelD = pygame.mixer.Channel(3)
soundChannelE = pygame.mixer.Channel(4)
soundChannelF = pygame.mixer.Channel(5)
soundChannelG = pygame.mixer.Channel(6)
soundChannelH = pygame.mixer.Channel(7)


#pygame.mixer.Channel(0).play(pygame.mixer.Sound('sound\gun_fire.wav'))
#pygame.mixer.Channel(1).play(pygame.mixer.Sound('sound\enemy_hit.wav'))

print("Sampler Ready.")
def play0():
	soundChannelA.play(sndA)
def play1():
	soundChannelB.play(sndB)
def play2():
	soundChannelC.play(sndC)
def play3():
	soundChannelD.play(sndD)
def play4():
	soundChannelE.play(sndE)
def play5():
	soundChannelF.play(sndF)
def play6():
	soundChannelG.play(sndG)
def play7():
	soundChannelH.play(sndH)


def foo0():
	thread.start_new_thread(play0, ())
def foo1():
	thread.start_new_thread(play1, ())
def foo2():
	thread.start_new_thread(play2, ())
def foo3():
	thread.start_new_thread(play3, ())
def foo4():
	thread.start_new_thread(play4, ())
def foo5():
	thread.start_new_thread(play5, ())
def foo6():
	thread.start_new_thread(play6, ())
def foo7():
	thread.start_new_thread(play7, ())


#time.sleep(2)
glosy = [foo0,foo1,foo2,foo3,foo4,foo5,foo6,foo7]

  
while True:
	try:
		czas = (random.randint(1,5)*25) / 50
		glos = random.choice (glosy)
		print('czas',czas,glos)	
		glos()
		sleep(czas)
	except KeyboardInterrupt:
		exit()
	  
#https://makezine.com/projects/make-33/simple-soundboard/	  
