import time 
import logging
import json
from datetime import datetime



names = ["bobrien", "seriksson", "mmorales", "aciotti", "oseldon", "tmchugh", "dgarrido", "cdeoliveira"]

#it would get the name using the qr code but for now you will enter the name
while True:
  def after_request():
    print(name_request + " found.")

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    log = {name_request:current_time}
    print("Current Time =", current_time)
    jsonFile = open("logs.json", "a")

  
    input("Press enter when returning")

    returning_time = datetime.now()
    returning_current_time =                       returning_time.strftime("%H:%M:%S")
    return_log = {name_request:current_time, "returned: ": returning_current_time}
    print("Current Time =", returning_current_time)
    return_jsonString = json.dumps(return_log, indent=5)
    jsonFile.write(return_jsonString)
    jsonFile.close()
  


  name_request = input("Enter name: \n")

  for x in range (0,8):
    if(names[x].upper() == name_request.upper()):
      after_request()
      break
    else: 
      print("Name not found, please re-enter")

    
