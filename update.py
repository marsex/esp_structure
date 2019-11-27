def check():
  import urequests
  import json

  git_url = 'https://raw.githubusercontent.com/marsex/esp_structure/master/'
  git_sys_info=json.loads(urequests.get(git_url+'sys_info').text)

  sys_file = open('sys_info','r')
  esp_sys_info = json.loads(sys_file.read())
  sys_file.close()

  print('git_sys_info: ', git_sys_info)
  print('esp_sys_info: ', esp_sys_info)