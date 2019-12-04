import urequests
import json

def update_system():
  print('git_sys_info: ', get_git_info())
  print('esp_sys_info: ', get_esp_info(),'\n')
  update_list = []
  for module in git_sys_info:
    try:
      if esp_sys_info[module] != git_sys_info[module]:
        update_list.append(module)
    except:
      print("error: module '"+ module +"' not founded")
  print('OUTDATED Modules:', update_list)
  

def check(module_name):
  print('git_sys_info: ', get_git_info())
  print('esp_sys_info: ', get_esp_info())
  try:
    if esp_sys_info[module_name] != git_sys_info[module_name]:
      return False, module_name, "outdated"
    else:
    
      return True, module_name, "updated"
  except:
    return "error: module '"+ module_name +"' not founded"


def get_esp_info():
  print('\n{\n\tgetting esp system info')
  global esp_sys_info
  try:
    sys_file = open('sys_info','r')
    esp_sys_info = json.loads(sys_file.read())
    sys_file.close()
    print('\tgot esp system info\n}')
    return esp_sys_info
  except:
    print('\terror getting esp system info\n}\n')


def get_git_info():
  print('\n{\n\tgetting git system info')
  global git_sys_info
  git_url = 'https://raw.githubusercontent.com/marsex/esp_structure/master/'
  try:
    git_sys_info = json.loads(urequests.get(git_url+'sys_info').text)
    print('\tgot git system info\n}')
    return git_sys_info
  except:
    print('\terror getting git system info\n}\n')