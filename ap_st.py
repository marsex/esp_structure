import network
import socket

def scan_wifi():
  global html
  
  station = network.WLAN(network.STA_IF) 
  station.active(True)
  
  wifi_list=station.scan()
  
  tr_swap=""
  tr_format="""
  <tr>
    <td onclick="set_ssid(this)">$ssid</td>
    <td class=$signal_state style="width:120px">$signal_state</td>
  </tr>
  """
  
  for wifi_net in wifi_list:
    net_signal=int(str(wifi_net[3]).replace('-',''))
    net_ssid=str(wifi_net[0]).replace("b'",'')
    net_ssid=net_ssid.replace("'",'')
    signal_state=''
    if net_signal <= 66:
      signal_state = "Excelente"
    
    if net_signal >= 67:
      signal_state = "Buena"
      
    if net_signal >= 80:
      signal_state = "Mala"
      
    tr_done = tr_format.replace('$ssid',net_ssid).replace('$signal_state',signal_state)
    tr_swap = tr_swap + tr_done
    
  print(tr_swap)
  file = open('get_wifi.html','r')
  html = file.read()
  html = html.replace('$tr_swap',tr_swap)
  file.close()
  start()

def start():
  try:
    port=80
    ap_wlan = network.WLAN(network.AP_IF)
    ap_wlan.active(True)
    ap_wlan.config(essid='delec_ESP32')
    ap_wlan.config(authmode=3, password='12551255')

    print('Access point created')
    print('AP Network data: ',ap_wlan.ifconfig())

    ap_localhost=ap_wlan.ifconfig()[0]            #get ip addr

    print('Got IP')
    ap_socket = socket.socket()                   #create socket
    print('Socket created')
    ap_socket.bind((ap_localhost,port))           #bind ip and port
    print('Socket bind complete')
    ap_socket.listen(1)                           #listen message
    print('Socket now listening')                 
    print('Listening port:',port)
    
    #Set the value of the given socket option
    ap_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    

    while True:
      client, address = ap_socket.accept()
      ip, port = str(address[0]), str(address[1])
      print('connection from ' + ip + ':' + port)
      client_file = client.makefile('rwb', 0)
      
      while True:
        line = client_file.readline()
        print(line)

        if not line or line == b'\r\n':
          break
      response = html 
      client.send(response)
      client.close()
  except:
    if(ap_socket):
      ap_socket.close()
    ap_wlan.disconnect()
    ap_wlan.active(False)

    print('ap_closed')




