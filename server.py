import machine
import network
import socket
import time
import dht
import ujson
from machine import Timer
from machine import Pin
import uasyncio as asyncio
from time import sleep
import uerrno

red=("\033[1;31;40m")
green=("\033[1;32;40m")
yellow=("\033[1;33;40m")
blue=("\033[1;34;40m")
normal=("\033[0;37;40m")

USER="esp02"
hostname="192.168.0.107"
SSID="TP-LINK_56A8"
PASSWORD="1234oooooo"
data_in="null"
ap_wlan=None
st_wlan=None
ap_socket=None
update=-1

def do_connect(ssid,wpsw):
  st_wlan = network.WLAN(network.STA_IF)
  st_wlan.active(True)

  if ssid != 'null':
    if not st_wlan.isconnected():
      st_wlan.connect(ssid,wpsw)
      print('Connecting to network: ' +ssid)
      while not st_wlan.isconnected():
        pass
      print('Connected, st_wlan: ', st_wlan.ifconfig())
  else:
    print('ssid null')
    try:
      print('try to reconnect')
      if not st_wlan.isconnected():
        print('attempt to reconnect')

        st_wlan.connect()
        print('reconnecting to network: ' +ssid)
        while not st_wlan.isconnected():
          pass
        print('Connected, st_wlan: ', st_wlan.ifconfig())
      else:
        print('st_wlan already connected')
    except:
      print('failed to reconnect')
      
def check(file_name):
  import urequests
  import json

  git_url = 'https://raw.githubusercontent.com/marsex/esp_structure/master/'
  git_sys_info=urequests.get(git_url+'sys_info').text

  sys_file = open('sys_info','r')
  esp_sys_info = json.loads(sys_file.read())
  sys_file.close()

  print('git_sys_info: ', git_sys_info)
  print('esp_sys_info: ', esp_sys_info)


def update(file_name):
  import urequests
  updated_file=urequests.get('https://raw.githubusercontent.com/marsex/esp_update/master/'+file_name+'.py')
  file = open(file_name+".py","w")
  file.write(updated_file.text)
  file.close()
  print(updated_file.text)
  print('updated')

print('do_connect')
do_connect(SSID,PASSWORD)
print('do_connect done')