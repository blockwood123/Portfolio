##
## testing http request  4-18-16
##
##

import urllib.request
import json
import time

ISSFILE="issdata.csv"
TRUE=1
comma=','
linefeed='\n'

http1="https://api.github.com/events"
http2="http://www.timeapi.org/utc/now.json"        ## get time and date
http3="http://api.open-notify.org/iss-now.json"    ## get International Space Station location

f=urllib.request.urlopen(http2)
buffer=f.read().decode("utf-8")
object=json.loads(buffer)
print("The time stamp is",object['dateString'])

f=open(ISSFILE,"a")       # open file to write out ISS position data to a file

while TRUE:
   response=urllib.request.urlopen(http3)
   buffer=response.read().decode("utf-8") 
## print("BUFFER:",buffer)
   object=json.loads(buffer)

   positiontime=object['timestamp']
   latitude=object['iss_position']['latitude']
   longitude=object['iss_position']['longitude']

## print("type positiontime",type(positiontime))
## print("type latitude",type(latitude))
## print("type longitude",type(longitude))

   f.write(str(positiontime)+comma+str(latitude)+comma+str(longitude)+linefeed)
   print("The International Space Station is located at latitude",latitude," with longitude",longitude)
   time.sleep(60)

f.close()



