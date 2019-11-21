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
    print(wifi_state)
    print("check_for_updates")
  else:
    credentials.get()
