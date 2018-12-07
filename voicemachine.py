#!/usr/bin/env python
import subprocess
from subprocess import call
import time
from time import sleep
from sys import exit
import thread
#import random
from pprint import pprint
import sys
import os
#import RPi.GPIO as GPIO
from flask import Flask, render_template
import datetime
import json
import glob
import argparse

arg_parser = argparse.ArgumentParser(description='Voice Machine')
arg_parser.add_argument('-b', '--bank', help='voice bank', default=0)
arg_parser.add_argument('-t', '--tempo', help='voice playing tempo', default=1)
arg_parser.add_argument('-v', '--vol', help='audio output volume', default=75)
args = arg_parser.parse_args()
tempo   = float(args.tempo)
vol     = str(args.vol)+'%'
nrBanku = int(args.bank);
print('bank=',nrBanku,'tempo=',tempo,'volume=',vol)

stopMPD = subprocess.Popen(["mpc", "stop"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
setVol  = subprocess.Popen(["amixer", "set","PCM",vol], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
os.system('sh /home/pi/voices/.killwav.sh')

bankPath = '/home/pi/voices/banks/'
banki = sorted(glob.glob(bankPath+"*/"))
ileBankow = len(banki)

def loadBank(bankName):
   return sorted(glob.glob(bankName+"*.wav"))

def formatuj(name,info):
   global bankNames
   title = name
   now   = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M:%S")
   templateData = {
      'title': title,
      'time':  timeString,
      'banks': bankNames,
      'name':  name,
      'info':  info
      }
   return templateData

   
print('.....')
bigBank=[]
namesBanks={}
bankNames=[]
nazwaBanku=''
for i in range(ileBankow):
   bank = loadBank(banki[i]) 
   arr = banki[i].split('/')
   name = arr[-2]
   nazwaBanku=name
   bankNames.append(name)
	#bigBank.extend(bank) # 1D
   bigBank.append(bank) # 2D
   namesBanks[name]=bank

templateData = formatuj("banks","BANKS")
#print(templateData)
#print(namesBanks)
print('_____')


app = Flask(__name__)

@app.route("/")
def root():
   #templateData = formatuj("VoiceMachine \\nweb\\npage\\n???","vMach")
   return render_template('main.html', **templateData)

@app.route("/bank/<name>")
def bank(name):
   global bankNames
   global nrBanku
   global ileBankow
   global namesBanks
   global nazwaBanku
   nrBanku = (nrBanku + 1) % ileBankow
   print(nrBanku,'bank//////',name)
   nazwaBanku=name
   #print(namesBanks[nazwaBanku])
   #command = "mpc play"
   #result_success = str(subprocess.check_output([command], shell=True))
   templateData = formatuj(name,name)
   return render_template('main.html', **templateData)

@app.route("/tempo/<val>")
def tempoo(val):
   global tempo
   tempo = val
   print('tempo=',tempo)
   templateData = formatuj('tempo','TEMPO')
   return render_template('main.html', **templateData)


@app.route("/radio")
def radio():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   command = "mpc play"
   result_success = str(subprocess.check_output([command], shell=True))
   templateData = formatuj(result_success,'INFO')
   return render_template('main.html', **templateData)



def playThread(foogracz):
   _lock = thread.allocate_lock()
   #_lock.acquire()
   x=thread.start_new_thread(foogracz, (_lock,))
   #_lock.release()

def startplay(b):
   global bigBank
   global nrBanku
   global ileBankow
   global banki
   global tempo
   step  = 0
   watek = 0 
   while True:
      try:
         step = (step+1)%100
         glos = namesBanks[nazwaBanku][watek]
         foogracz = lambda i: call(["aplay","-q", glos])
         playThread(foogracz)
         watek = (watek+1)%8
         arr = glos.split('/')
         czas = float(tempo)
         #print(nrBanku,'/',watek,'czas=',czas, arr[-2],arr[-1])
         sleep(czas)
      except KeyboardInterrupt:
         exit()


def startapp(a):
   startplay(0)
   
      
if __name__ == "__main__":
   thread.start_new_thread(startplay, (0,))
   app.run(host='0.0.0.0', port=5000, debug=True)
   
     
   
   
   
   
   
