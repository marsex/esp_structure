def check_credentials():
  print('Check Wifi Credentials')
  global cred_ssid, cred_psw
  file = open("credentials.data","r")
  data = file.read()
  file.close()

  cred_ssid=data.split(",")[0]
  cred_psw=data.split(",")[1]
  print(cred_ssid + ' ' + cred_psw)
  if cred_ssid == 'null':
    return False
  else:
    return True


def get_credentials():
  print('Get Wifi Credentials')
  import ap_st
  ap_st.scan_wifi(cred_ssid,cred_psw)


def connect_wifi():
  print('Connect to Wifi network')

def check_updates():
  print('Check updates')

def start():
  if check_credentials() == True:
    print('Got credentials')
  else:
    get_credentials()
