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
import argparse
arg_parser = argparse.ArgumentParser(description='Voice Machine')
arg_parser.add_argument('-b', '--bank', help='voice bank', default=0)
arg_parser.add_argument('-t', '--tempo', help='voice playing tempo', default=50)
arg_parser.add_argument('-v', '--vol', help='audio output volume', default=75)
args = arg_parser.parse_args()
tempo   = int(args.tempo)
vol     = str(args.vol)+'%'
nrBanku = int(args.bank);
print('bank=',nrBanku,'tempo=',tempo,'volume=',vol)

# python3 ay.py -t 100 -v 60
#print(sys.version_info)

stopMPD = subprocess.Popen(["mpc", "stop"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
setVol  = subprocess.Popen(["amixer", "set","PCM",vol], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
os.system('sh /home/pi/voices/.killwav.sh')

bankPath = '/home/pi/voices/banks/'
banki = sorted(glob.glob(bankPath+"*/"))
ileBankow = len(banki)


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

