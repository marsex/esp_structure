print("ble_basic loaded")
import ubluetooth as bluetooth
from machine import Pin
from time import sleep

inp_gpio=[35,34,39,36,3,21,19,18,5,17,16,4]
out_gpio=[32,33,25,26,27,14,12,13]

def ble_irq(event, data):
  try:
    conn_handle, addr_type, addr = data
  except:
    conn_handle, addr_type = data

  print('\nevent:',event)

  if event == 1:
    print('USER:',addr,'connected')
  elif event == 2:
    print('USER:',addr,'disconnected')
    advertise()
  elif event == 4:
    ble_rx = ble.gatts_read(rx)
    print('ble_rx',ble_rx)
    data = ble_rx.decode('utf8').replace("'", '"')
    print('data',data)
    cmd, arg = data.split('=')
    arg = float(arg)
    print('CMD:', cmd)
    print('ARG:', arg) 
    if cmd == 'sh':
        Pin(out_gpio[1], value=1)
        Pin(out_gpio[2], value=1)
        print('Salida 1 + 2 = ON')
        sleep(arg)
        Pin(out_gpio[1], value=0)
        Pin(out_gpio[2], value=0)
        print('Salida 1 + 2 = OFF')

def stop_ble():
  print('stop ble')
  ble.gap_advertise(0)
  ble.active(False)

def ble_wr(data):
  ble_tx = to_byte(data)
  ble.gatts_write(tx,ble_tx)

def to_byte(string):
  string = bytes(string, 'ascii')
  return bytearray((len(string) + 1, 0x09)) + string

def advertise():
    print("# Start advertising")
    ble.gap_advertise(100, to_byte('ESP32_ENV'))
    

print("config ble")
# Configuration
ble = bluetooth.BLE()
ble.active(True)
ble.irq(ble_irq)

print("start ble service")
# GATT Server
UART_UUID = bluetooth.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
UART_TX = (bluetooth.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
UART_RX = (bluetooth.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'), bluetooth.FLAG_WRITE,)
UART_SERVICE = (UART_UUID, (UART_TX, UART_RX,),)
SERVICES = (UART_SERVICE,)
((tx, rx,), ) = ble.gatts_register_services(SERVICES)
print("ble service started")
