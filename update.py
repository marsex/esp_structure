import urequests
import json
import color
import sys_info

def system():
  update_list = []
  for module in git_sys_info:
    try:
      if esp_sys_info[module] != git_sys_info[module]:
        update_list.append(module)
    except:
      print("error: module '"+ module +"' not founded")
  print('OUTDATED Modules:', update_list)
  for outdated_module in update_list:
    print(color.blue(),'\nUpdating:', outdated_module+color.normal())
    git_file(outdated_module)


def check(module_name):
  global git_sys_info, esp_sys_info, git_url
  esp_sys_info=sys_info.esp_info()
  git_sys_info=sys_info.git_info()
  git_url=sys_info.git_url()
  print('\n'+color.blue()+'git_sys_info:',color.normal(), str(git_sys_info).replace(',',',\n').replace('{','{\n ').replace('}','\n}'))
  print('\n'+color.red()+'esp_sys_info:',color.normal(), str(esp_sys_info).replace(',',',\n').replace('{','{\n ').replace('}','\n}'))

  sys_state=(False, 'system', 'updated')
  try:
    if module_name == '':
      for module in git_sys_info:
        try:
          if esp_sys_info[module] != git_sys_info[module]:
            sys_state = (False, module, "outdated")
        except:
          print("error: module '"+ module +"' not founded")
      return sys_state
    else:
      if esp_sys_info[module_name] != git_sys_info[module_name]:
        return True, module_name, "outdated"
      else:
        return False, module_name, "updated"
  except:
    return "error: module '"+ module_name +"' not founded"


def git_file(file_name):
  updated_file=urequests.get(git_url+file_name)
  file = open(file_name,"w")
  file.write(updated_file.text)
  file.close()
  print(color.normal()+updated_file.text)
  print(color.green(),file_name,'updated\n'+color.normal())