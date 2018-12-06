import subprocess
from subprocess import call
import time
from time import sleep
from sys import exit
import thread
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

   
print('...')
bigBank=[]
for i in range(ileBankow):
	print(banki[i])
	bank = loadBank(banki[i]) 
	bigBank.extend(bank)
random.shuffle(bigBank)   
print(bigBank)   
print('...')
   
   
   
def playThread(foogracz):
	_lock = thread.allocate_lock()
	#_lock.acquire()
	x=thread.start_new_thread(foogracz, (_lock,))
	#_lock.release()

step  = 0
#watek = 0 
bank = loadBank(banki[nrBanku])   
while True:
	try:
		step = (step+1)%100
		czas = (random.randint(0,4)*10) / tempo
		czas += (5*step/tempo)
		#glos = random.choice(bank)
		glos = random.choice(bigBank)
		foogracz = lambda i: call(["aplay","-q", glos])
		playThread(foogracz)
		#watek = (watek+1)%8
		arr = glos.split('/')
		print(nrBanku,'/',step,'czas=',(format(czas, '.2f')), arr[-2],arr[-1])
		sleep(czas)
		if (step % 5 == 4):
			nrBanku = (nrBanku + 1) % ileBankow  
			bank = loadBank(banki[nrBanku])
	except KeyboardInterrupt:
		exit()

