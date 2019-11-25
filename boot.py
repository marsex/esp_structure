def check_updates():
  print('Check updates')

def start():
  import wifi
  import credentials
  global cred_ssid, cred_psw, wifi_state
  
  value, cred_ssid, cred_psw = credentials.check()
  print(credentials.check())
  
  if value == True:
    wifi_state = wifi.connect(cred_ssid,cred_psw)
    if wifi_state == True:
      print("check for updates")
      
  else:
    credentials.get()
