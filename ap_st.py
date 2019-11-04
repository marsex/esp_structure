import network
SSID="TP-LINK_56A8"
PASSWORD="1234oooooo"

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

do_connect(SSID,PASSWORD)