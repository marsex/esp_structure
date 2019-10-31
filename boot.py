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

inp_gpio=[36,39,34,35,32,23,22,21]
out_gpio=[13,15,2,4,25,33,5,18]

red=("\033[1;31;40m")
green=("\033[1;32;40m")
yellow=("\033[1;33;40m")
blue=("\033[1;34;40m")
normal=("\033[0;37;40m")

hostname= "
USER="esp01"
SSID="TP-LINK_56A8"
PASSWORD="1234oooooo"
data_in="null"
ap_wlan=None
st_wlan=None
ap_socket=None 
update=-1

dht1 = dht.DHT22(machine.Pin(16, Pin.IN, Pin.PULL_UP))
dht2 = dht.DHT22(machine.Pin(19, Pin.IN, Pin.PULL_UP))

#machine_data = {"command":"null","version":"v0.9.1.1","platform":"esp32","uptime":str(time.time()),"user":USER,"gpio":{"input_enable":[0,0,1,0,0,0,0,0],"input_state":[0,0,1,0,0,0,0,0],"input_prog":[0,0,2,0,0,0,0,0],"output_enable":[1,1,1,1,1,1,1,1],"output_state":[0,0,0,0,0,1,0,0],"output_prog":[0,0,0,0,0,0,0,0]},"dht1":{"tmp":0,"hmd":0,"tmp_out":0,"tmp_set":0,"tmp_off_time":4,"tmp_on_time":10,"hmd_out":0,"hmd_set":0,"hmd_off_time":4,"hmd_on_time":10,"check_interval":10},"dht2":{"tmp":0,"hmd":0,"tmp_out":0,"tmp_set":0,"tmp_off_time":4,"tmp_on_time":10,"hmd_out":0,"hmd_set":0,"hmd_off_time":4,"hmd_on_time":10,"check_interval":10}}
#machine_data = {"command":"null","version":"v0.9.1.1","platform":"esp32","uptime":str(time.time()),"user":USER,"gpio":{"input_enable":[0,0,1,0,0,0,0,0],"input_state":[0,0,1,0,0,0,0,0],"input_prog":[0,0,2,0,0,0,0,0],"output_enable":[1,1,1,1,1,1,1,1],"output_state":[0,0,0,0,0,1,0,0],"output_prog":[0,0,0,0,0,0,0,0]},"dht1":{"tmp_enable":0,"tmp":0,"tmp_out":0,"tmp_set":0,"tmp_on_time":10,"tmp_off_time":4,"tmp_interval":10,"hmd_enable":0,"hmd":0,"hmd_out":0,"hmd_set":0,"hmd_on_time":10,"hmd_off_time":4,"hmd_interval":10},"dht2":{"tmp_enable":0,"tmp":0,"tmp_out":0,"tmp_set":0,"tmp_on_time":10,"tmp_off_time":4,"tmp_interval":10,"hmd_enable":0,"hmd":0,"hmd_out":0,"hmd_set":0,"hmd_on_time":10,"hmd_off_time":4,"hmd_interval":10}}
machine_data = {
  "command":"null",
  "version":"v0.9.1.1",
  "platform":"esp32",
  "uptime":str(time.time()),
  "user":USER,
  "gpio":{
    "input_enable":[0,0,1,0,0,0,0,0],
    "input_state":[0,0,1,0,0,0,0,0],
    "input_prog":[0,0,2,0,0,0,0,0],
    "output_enable":[1,1,1,1,1,1,1,1],
    "output_state":[0,0,0,0,0,1,0,0],
    "output_prog":[0,0,0,0,0,0,0,0]
  },
  "dht1":{
    "tmp_enable":0,
    "tmp":0,
    "tmp_salida":3,
    "tmp_set":0,
    "tmp_on_time":0,
    "tmp_on_tick":0,
    "tmp_off_time":0,
    "tmp_off_tick":0,
    "tmp_interval":0,
    "tmp_tick":0,
    "hmd_enable":0,
    "hmd":0,
    "hmd_salida":3,
    "hmd_set":0,
    "hmd_on_time":0,
    "hmd_on_tick":0,
    "hmd_off_time":0,
    "hmd_off_tick":0,
    "hmd_interval":0,
    "hmd_tick":0
  },
  "dht2":{
    "tmp_enable":0,
    "tmp":0,
    "tmp_salida":3,
    "tmp_set":0,
    "tmp_on_time":0,
    "tmp_on_tick":0,
    "tmp_off_time":0,
    "tmp_off_tick":0,
    "tmp_interval":0,
    "tmp_tick":0,
    "hmd_enable":0,
    "hmd":0,
    "hmd_salida":3,
    "hmd_set":0,
    "hmd_on_time":0,
    "hmd_on_tick":0,
    "hmd_off_time":0,
    "hmd_off_tick":0,
    "hmd_interval":0,
    "hmd_tick":0
  }
}


async def check_dht():
  while True:
    tmp_enable=machine_data['dht1']['tmp_enable']
    tmp=machine_data['dht1']['tmp']
    tmp_set=float(machine_data['dht1']['tmp_set'])
    tmp_salida=int(machine_data['dht1']['tmp_salida'])-1
    tmp_on_time=int(machine_data['dht1']['tmp_on_time'])
    tmp_on_tick=int(machine_data['dht1']['tmp_on_tick'])
    tmp_off_time=int(machine_data['dht1']['tmp_off_time'])
    tmp_off_tick=int(machine_data['dht1']['tmp_off_tick']) 

    if tmp_enable == 'true':
      print('tmp_enable = true')

      if tmp_set > tmp:
        if tmp_on_tick < tmp_on_time:
          machine_data['dht1']['tmp_on_tick']=tmp_on_tick+1
          print('tmp_on_tick=', tmp_on_tick)

          if Pin(out_gpio[tmp_salida]).value() != 1:
            Pin(out_gpio[tmp_salida], value=1)

        if tmp_on_tick >= tmp_on_time:
          if Pin(out_gpio[tmp_salida]).value() != 0:
            Pin(out_gpio[tmp_salida], value=0)
          if tmp_off_tick < tmp_off_time:
            print('tmp_off_tick=', tmp_off_tick)
            machine_data['dht1']['tmp_off_tick']=tmp_off_tick+1
        
        if tmp_off_tick >= tmp_off_time:
          if Pin(out_gpio[tmp_salida]).value() != 1:
            Pin(out_gpio[tmp_salida], value=1)
          machine_data['dht1']['tmp_on_tick']=0
          machine_data['dht1']['tmp_off_tick']=0

      if tmp_set < tmp:
        Pin(out_gpio[tmp_salida], value=0)
      
      print('')
    await asyncio.sleep(1)


async def com():
  print('com start')
  while True:
    input_state = [machine.Pin(i, machine.Pin.IN).value() for i in inp_gpio]
    output_state = [machine.Pin(i, machine.Pin.OUT).value() for i in out_gpio]
    machine_data['dht1']['tmp']=dht1.temperature()
    machine_data['dht1']['hmd']=dht1.humidity()
    machine_data['dht2']['tmp']=dht2.temperature()
    machine_data['dht2']['hmd']=dht2.humidity()
    machine_data['uptime']=str(time.time())
    machine_data['gpio']['input_state']=input_state
    machine_data['gpio']['output_state']=output_state
    
    address = socket.getaddrinfo(hostname, 1259)[0][-1]
    ip, port = str(address[0]), str(address[1])
    st_socket = socket.socket()
    st_socket.setblocking(False)
    #print('try to connect')
    try:
      #print('connecting')
      st_socket.connect(address)
    except OSError as e:
      if e.args[0] not in [uerrno.EINPROGRESS, uerrno.ETIMEDOUT]:
        print('Error connecting', e)
    
    
    attempts = 8
    while attempts:
      attempts=attempts-1
      print('try to send data: ', attempts)
      try:
        print('sending data')
        st_socket.sendall(bytes(str(machine_data), 'UTF-8')) # MQTT ping
        print('data sent')
        await asyncio.sleep(0.25)
        while True:
          buffer_data = st_socket.recv(1024)
          host_data = str(buffer_data)
          if host_data.find('null') == -1:
            parse_data(host_data)
          attempts = 0
          print('Got Data: ', host_data)
          break
      except OSError as e:
        if e.args[0] not in [uerrno.EINPROGRESS, uerrno.ETIMEDOUT]:
          print('**** ERROR writing ****', e)
          attempts = 0

    st_socket.close()
  print('com end')


async def com2():
  print('com start')
  while True:
    input_state = [machine.Pin(i, machine.Pin.IN).value() for i in inp_gpio]
    output_state = [machine.Pin(i, machine.Pin.OUT).value() for i in out_gpio]
    machine_data['dht1']['tmp']=dht1.temperature()
    machine_data['dht1']['hmd']=dht1.humidity()
    machine_data['dht2']['tmp']=dht2.temperature()
    machine_data['dht2']['hmd']=dht2.humidity()
    machine_data['uptime']=str(time.time())
    machine_data['gpio']['input_state']=input_state
    machine_data['gpio']['output_state']=output_state
    
    address = socket.getaddrinfo(hostname, 1259)[0][-1]
    ip, port = str(address[0]), str(address[1])
    st_socket = socket.socket()
    st_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    st_socket.settimeout(.1)

    try:
      st_socket.connect(address)
      attempts = 1
      while attempts:

        try:
          st_socket.sendall(bytes(str(machine_data), 'UTF-8')) # MQTT ping
          #print('Data Sent.')
          while True:
            buffer_data = st_socket.recv(1024)
            host_data = str(buffer_data)
            if host_data.find('null') == -1:
              parse_data(host_data)
            attempts = 0
            #print('Got Data.')
            break
        except OSError as e:
          if e.args[0] not in [uerrno.EINPROGRESS, uerrno.ETIMEDOUT]:
            print('**** ERROR writing ****', e)
            attempts = 0

    except OSError as e:
      if e.args[0] not in [uerrno.EINPROGRESS, uerrno.ETIMEDOUT]:
        print('Error connecting', e)

    st_socket.close()
    await asyncio.sleep_ms(25)


def t2com():
  print('com start')

  input_state = [machine.Pin(i, machine.Pin.IN).value() for i in inp_gpio]
  output_state = [machine.Pin(i, machine.Pin.OUT).value() for i in out_gpio]
  machine_data['dht1']['tmp']=dht1.temperature()
  machine_data['dht1']['hmd']=dht1.humidity()
  machine_data['dht2']['tmp']=dht2.temperature()
  machine_data['dht2']['hmd']=dht2.humidity()
  machine_data['uptime']=str(time.time())
  machine_data['gpio']['input_state']=input_state
  machine_data['gpio']['output_state']=output_state
  
  address = socket.getaddrinfo(hostname, 1259)[0][-1]
  ip, port = str(address[0]), str(address[1])
  st_socket = socket.socket()
  st_socket.setblocking(False)
  print('try to connect')
  try:
    print('connecting')
    st_socket.connect(address)
  except OSError as e:
    if e.args[0] not in [uerrno.EINPROGRESS, uerrno.ETIMEDOUT]:
      print('Error connecting', e)
  
  
  attempts = 5
  while attempts:
    attempts=attempts-1
    print('try to send data: ', attempts)
    try:
      print('sending data')
      st_socket.sendall(bytes(str(machine_data), 'UTF-8')) # MQTT ping
      print('data sent')
      sleep(.1)
      while True:
        buffer_data = st_socket.recv(1024)
        host_data = str(buffer_data)
        if host_data.find('null') == -1:
          parse_data(host_data)
        attempts = 0
        print('Got Data: ', host_data)
        break
    except OSError as e:
      if e.args[0] not in [uerrno.EINPROGRESS, uerrno.ETIMEDOUT]:
        print('**** ERROR writing ****', e)
        attempts = 0

  st_socket.close()
  print('com end')


def tcom():
  print('com start')

  input_state = [machine.Pin(i, machine.Pin.IN).value() for i in inp_gpio]
  output_state = [machine.Pin(i, machine.Pin.OUT).value() for i in out_gpio]
  machine_data['dht1']['tmp']=dht1.temperature()
  machine_data['dht1']['hmd']=dht1.humidity()
  machine_data['dht2']['tmp']=dht2.temperature()
  machine_data['dht2']['hmd']=dht2.humidity()
  machine_data['uptime']=str(time.time())
  machine_data['gpio']['input_state']=input_state
  machine_data['gpio']['output_state']=output_state
  
  address = socket.getaddrinfo(hostname, 1259)[0][-1]
  ip, port = str(address[0]), str(address[1])

  s = socket.socket()
  s.setblocking(False)
  try:
    s.connect(address)
  except OSError as e:
    if e.args[0] not in [uerrno.EINPROGRESS, uerrno.ETIMEDOUT]:
      print('Error connecting', e)
      return

  try:
    s.sendall(bytes(str(machine_data), 'UTF-8')) # MQTT ping
    print('Data Sent.')
  except OSError as e:
    if e.args[0] not in [uerrno.EINPROGRESS, uerrno.ETIMEDOUT]:
      print('**** ERROR writing ****', e)

  sleep(.1)
  print('com end')


def parse_data(client_data):
  try:
    parsed_input = str(client_data[2:len(client_data)-1].replace("\'", "\""))
    command_json = ujson.loads(parsed_input)

    if command_json['command'] == 'output_state':
      update = command_json['update'].split('=')
      pin=int(update[0])-1
      state=int(update[1])
      Pin(out_gpio[pin], value=state)

    if command_json['command'] == 'dht1':
      update = command_json['update'].split(',')
      print(update)
      for x in update:
        objeto = x.split('=')
        machine_data['dht1'][objeto[0]]=objeto[1]

  except:
    print('error reading json')


def do_connect(ssid,wpsw):
  st_wlan = network.WLAN(network.STA_IF)
  st_wlan.active(True)
  print('{')
  if ssid != 'null':
    print('ssid not null')
    if not st_wlan.isconnected():
      print('if not st_wlan.isconnected():')
      st_wlan.connect(ssid,wpsw)
      print('       Connecting to network: ' +ssid)
      while not st_wlan.isconnected():
        pass
      print('   Connected, st_wlan: ', st_wlan.ifconfig())
  else:
    print('ssid null')
    try:
      print('try to reconnect')
      if not st_wlan.isconnected():
        print('attempt to reconnect')

        st_wlan.connect()
        print('     reconnecting to network: ' +ssid)
        while not st_wlan.isconnected():
          pass
        print('   Connected, st_wlan: ', st_wlan.ifconfig())
        print('}')
      else:
        print('st_wlan already connected')
    except:
      print('failed to reconnect')
      print('get wifi credentials')
      get_wifi_data()
      print('got wifi credentials')



def async_dht():
  print('async_dht')
  loop = asyncio.get_event_loop()
  loop.create_task(await_dht())
  loop.run_until_complete(async_dht_done())


def async_com():
  print('async_com')
  loop = asyncio.get_event_loop()
  loop.create_task(com())  
  loop.create_task(await_dht())
  loop.create_task(check_dht())
  loop.run_forever()
  
  
async def await_dht():
  print('await_dht start')
  while True:
    print('get dht1')
    try:
      dht1.measure()
      print('dh1 ok')
    except:
      print('dh1 fail')
    
    print('dht1_done')
    print('')
    await asyncio.sleep(5)
    print('get dht2')
    
    try:
      dht2.measure()
      print('dh2 ok')
    except:
      print('dh2 fail')
    print('dht2_done')
    print('')
    await asyncio.sleep(5)


print('do_connect')
do_connect(SSID,PASSWORD)
print('do_connect done')
#async_com()
#measure_timer=Timer(0)
#measure_timer.init(period=5000, mode=Timer.PERIODIC, callback=lambda t:async_dht())

#timeout.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:http_get(hostname))




