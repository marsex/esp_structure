def update(file_name):
  import urequests
  updated_file=urequests.get('https://raw.githubusercontent.com/marsex/esp_update/master/'+file_name+'.py')
  file = open(file_name+".py","w")
  file.write(updated_file.text)
  file.close()
  print(updated_file.text)
  print('updated')