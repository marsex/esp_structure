import network

def connect(cred_ssid,cred_psw):
  print('\n{\n\tConnecting to network: ' +cred_ssid)
  st_wlan = network.WLAN(network.STA_IF)
  st_wlan.active(True)
  
  if cred_ssid != 'null':
    if not st_wlan.isconnected():
      st_wlan.connect(cred_ssid,cred_psw)
      while not st_wlan.isconnected():
        pass
      print('\tConnected, st_wlan:', st_wlan.ifconfig(), '\n}\n')
      return True
    else:
      print('\tAlready connected to:', cred_ssid, '\n\t', st_wlan.ifconfig(),'\n}\n')
      return True
  else:
    try:
      print('\n{\n\treconnecting to network: ' +cred_ssid)
      if not st_wlan.isconnected():
        st_wlan.connect()
        while not st_wlan.isconnected():
          pass
        print('\tConnected, st_wlan:', st_wlan.ifconfig(), '\n}\n')
        return True
      else:
        print('\tAlready connected to:', st_wlan.ifconfig(), '\n}\n')
        return True
    except:
      print('failed to reconnect')
      print('get wifi credentials')
      return False