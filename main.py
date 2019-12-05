import credentials
import update
import wifi

def start():
  print('Check WiFi credentials')
  global cred_ssid, cred_psw, wifi_state
  cred_state, cred_ssid, cred_psw = credentials.check()
  if cred_state == True:
    print('Credentials true, connect to WIFI')
    wifi_state = wifi.connect(cred_ssid,cred_psw)
    if wifi_state == True:
      print('Check for updates')
      if update.check('system')[0] == True:
        print('\nSystem outdated\nUpdating system')
      else:
        print('\nSystem up to date\nStart Communication')
  else:
    credentials.get()