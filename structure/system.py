def start():
  try:
    from structure import com
    print('System running')
    com.start()
  except:
    print('System failure')