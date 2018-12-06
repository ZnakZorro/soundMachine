import os
import subprocess
from subprocess import call
import time

from time import sleep
#import RPi.GPIO as GPIO
from sys import exit
import thread
#from thread import *
import random
from pprint import pprint
import sys
import os
#from os import walk
import glob

# python3 ay.py -t 100 -v 60

ttempo = 0
vvol = 0
vol = 75;
tempo = 50;

#pprint(sys.argv)
if (len(sys.argv)>2):
   if (sys.argv[1]=="-t"):
      ttempo = int(sys.argv[2])

if (ttempo>0):
   tempo = ttempo
      
if (len(sys.argv)>4):
   if (sys.argv[3]=="-v"):
      vvol = int(sys.argv[4])

if (vvol>0):
   vol = vvol
   
svol = str(vol)+"%"   
print('tempo='+str(tempo),'vol='+svol)



stopMPD = subprocess.Popen(["mpc", "stop"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
setVol  = subprocess.Popen(["amixer", "set","PCM",svol], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
os.system('sh /home/pi/voices/.killwav.sh')


#banki = ['wind','strings','vocals1','bells','instrumenty','ptaki','zwierzeta','piano1']
#ileBankow = len(banki)

nrBanku = 0;
lastVoice=8;
players=[]

bankPath = '/home/pi/voices/banks/'
banki = sorted(glob.glob(bankPath+"*/"))
#print(b)
pprint(banki)
print('==========================')
ileBankow = len(banki)


def loadBank(bankName):
	DS='/'
	#bankPath = '/home/pi/voices/banks/'
	#pathBank   = bankPath+bankName+DS
	pathBank   = bankName
	return sorted(glob.glob(pathBank+"*.wav"))

   
bank = loadBank(banki[nrBanku])

gracz = lambda i: call(["aplay","-q", glos])

def playThread(w):
	thread.start_new_thread(gracz, (w,))

step  = 0
watek = 0 
   
while True:
	try:
		step = (step+1)%100
		czas = (random.randint(0,4)*10) / tempo
		czas += (2*step/tempo)
		glos = random.choice(bank)
		gracz = lambda i: call(["aplay","-q", glos])
		playThread(watek)
		watek = (watek+1)%8
		print(watek,nrBanku,step,'czas',czas)
		sleep(czas)
		if (step % 20 == 19):
			nrBanku = (nrBanku + 1) % ileBankow  
			bank = loadBank(banki[nrBanku])
	except KeyboardInterrupt:
		exit()



      
#https://makezine.com/projects/make-33/simple-soundboard/
#https://my-little-piano-app.herokuapp.com/
#https://mrcoles.com/piano/
#https://freewavesamples.com/?page=67
#http://soundbible.com/tags-waves.html 
#https://ttsmp3.com/text-to-speech/Polish/
