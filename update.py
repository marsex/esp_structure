import urequests
import json

def check(module_name):
  print('git_sys_info: ', get_git_info())
  print('esp_sys_info: ', get_esp_info())
  if esp_sys_info[module_name] != git_sys_info[module_name]:
    print(module_name, "status: OUTDATED")
  else:
    print(module_name, "status: UPDATED")
  
def get_esp_info():
  global esp_sys_info
  sys_file = open('sys_info','r')
  esp_sys_info = json.loads(sys_file.read())
  sys_file.close()
  return esp_sys_info
  
def get_git_info():
  global git_sys_info
  git_url = 'https://raw.githubusercontent.com/marsex/esp_structure/master/'
  git_sys_info = json.loads(urequests.get(git_url+'sys_info').text)
  return git_sys_info