import credentials
import update
import wifi

def start():
  global cred_ssid, cred_psw, wifi_state
  
  print('Check wifi credentials')
  cred_state, cred_ssid, cred_psw = credentials.check()
  if cred_state == True:
    print('Credentials true, connect to WIFI')
    wifi_state = wifi.connect(cred_ssid,cred_psw)
    if wifi_state == True:
      print('Connected to WIFI, check for updates')
      if update.check('system')[0] == True:
        print('Connected to WIFI, check for updates')
  else:
    credentials.get()
    