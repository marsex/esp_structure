def check_credentials():
  file = open("credentials.data","r")
  data = file.read()
  file.close()

  SSID=data.split(",")[0]
  W_PSW=data.split(",")[1]

  if SSID == 'null':
    return "False"
  else:
    return "True"


def get_credentials():
  import ap_st.py
