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
import glob

# python3 ay.py -t 100 -v 60
print(sys.version_info)
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

bankPath = '/home/pi/voices/banks/'
banki = sorted(glob.glob(bankPath+"*/"))
ileBankow = len(banki)
nrBanku   = 0;

def loadBank(bankName):
	return sorted(glob.glob(bankName+"*.wav"))

def playThread(foogracz):
	_lock = thread.allocate_lock()
	#_lock.acquire()
	x=thread.start_new_thread(foogracz, (_lock,))
	#_lock.release()

step  = 0
watek = 0 
bank = loadBank(banki[nrBanku])   
while True:
	try:
		step = (step+1)%100
		czas = (random.randint(0,4)*10) / tempo
		czas += (2*step/tempo)
		glos = random.choice(bank)
		foogracz = lambda i: call(["aplay","-q", glos])
		playThread(foogracz)
		watek = (watek+1)%8
		print(watek,nrBanku,step,'czas',czas)
		sleep(czas)
		if (step % 3 == 2):
			nrBanku = (nrBanku + 1) % ileBankow  
			bank = loadBank(banki[nrBanku])
	except KeyboardInterrupt:
		exit()
