import credentials

def check_credentials():
  SSID=credentials.read().split(",")[0]
  W_PSW=credentials.read().split(",")[1]

  if SSID == 'null':
    return "false"
  else
    return "true"
    
def get_credentials():
  import ap_st.py
  
  