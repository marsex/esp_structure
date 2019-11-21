def check():
  print('Check Wifi Credentials')
  file = open("credentials.data","r")
  data = file.read()
  file.close()

  cred_ssid=data.split(",")[0]
  cred_psw=data.split(",")[1]
  print(cred_ssid + ' ' + cred_psw)
  if cred_ssid == 'null':
    return False,cred_ssid,cred_psw
  else:
    return True,cred_ssid,cred_psw
    
def get():
  print('Get Wifi Credentials')
  import ap_st
  ap_st.scan_wifi(cred_ssid,cred_psw)
  