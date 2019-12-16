from system import update, wifi, system 
import machine 

def boot():
  print('System version: 9.1.1.3')
  print('Check WiFi credentials')
  global cred_ssid, cred_psw, wifi_state
  cred_state, cred_ssid, cred_psw = wifi.credentials()
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
        system.start()
  else:
    wifi.get_credentials()