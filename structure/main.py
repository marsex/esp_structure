from structure import wifi, update, system 
import machine 

def boot():
  print('System version: 9.1.1.3')
  global cred_ssid, cred_psw, wifi_state
  print('Check WiFi credentials')
  credentials_state, cred_ssid, cred_psw = wifi.check_credentials()
  if credentials_state == True:
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
        system.start()
  else:
    wifi.get_credentials()