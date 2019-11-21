def connect(cred_ssid,cred_psw):
  import network
  
  print('Connect to Wifi network')
  st_wlan = network.WLAN(network.STA_IF)
  st_wlan.active(True)
  print('{')
  if cred_ssid != 'null':
    print('cred_ssid not null')
    if not st_wlan.isconnected():
      print('if not st_wlan.isconnected():')
      st_wlan.connect(cred_ssid,cred_psw)
      print('       Connecting to network: ' +cred_ssid)
      while not st_wlan.isconnected():
        pass
      print('   Connected, st_wlan: ', st_wlan.ifconfig())
  else:
    print('cred_ssid null')
    try:
      print('try to reconnect')
      if not st_wlan.isconnected():
        print('attempt to reconnect')

        st_wlan.connect()
        print('     reconnecting to network: ' +cred_ssid)
        while not st_wlan.isconnected():
          pass
        print('   Connected, st_wlan: ', st_wlan.ifconfig())
        print('}')
        return True
      else:
        print('st_wlan already connected')
        return True
    except:
      print('failed to reconnect')
      print('get wifi credentials')
      return False