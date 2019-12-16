from system import credentials, update, wifi, com 
import machine 

def boot():
  print('Check WiFi credentials')
  global cred_ssid, cred_psw, wifi_state
  cred_state, cred_ssid, cred_psw = credentials.check()
  if cred_state == True:
    print('Credentials true, connect to WIFI')
    wifi_state = wifi.connect(cred_ssid,cred_psw)
    if wifi_state == True:
      print('Check for updates')
      if update.check('sys_info')[0] == True:
        print('\nSystem OUTDATED')
        update.system()
        machine.reset()
      else:
        print('\nSystem up to date\nStart system')
        #com.start()
  else:
    credentials.get()