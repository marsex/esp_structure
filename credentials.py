import ap_st

def check():
  global cred_ssid, cred_psw
  file = open("credentials","r")
  data = file.read()
  file.close()

  cred_ssid=data.split(",")[0]
  cred_psw=data.split(",")[1]
  
  if cred_ssid == 'null':
    return False,cred_ssid,cred_psw
  else:
    return True,cred_ssid,cred_psw
    
    
def get():
  print('Get Wifi Credentials')
  ap_st.scan_wifi(cred_ssid,cred_psw)
  