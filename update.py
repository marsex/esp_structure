import urequests

def update(file_name):
  git_url = 'https://raw.githubusercontent.com/marsex/esp_structure/master/'
  updated_file=urequests.get(git_url+'version.py')
  
  file = open(file_name+".py","w")
  file.write(updated_file.text)
  file.close()
  print(updated_file.text)
  print('updated')