from system import ap_st
    
def get():
  print('Get Wifi Credentials')
  ap_st.scan_wifi(cred_ssid,cred_psw)
  