##
## testing http request to utilize DuckDuckGo
##
## 4/23/16 - Lockwood 
##

import urllib
import urllib.request

import json
import time
       

##  httpX="http://api.duckduckgo.com/?q=Moon&format=json"

http4="http://api.duckduckgo.com/"
question="?q="
formatjson="&format=json"

TRUE=1
while TRUE:
   print()
   searchstring=input("Hi - what 'something' would you like to know about? ")
   print()

   newstring=""
   for i in searchstring:
       if i==" ":
          newstring+="%20"
       else:
          newstring+=i
   searchstring=newstring

   urlstring=http4+question+searchstring+formatjson
   req=urllib.request.Request(urlstring)
   response = urllib.request.urlopen(req)

   buffer=response.read().decode("utf-8")
  
   f=open("duckduckgo.txt",'w')
   f.write(buffer)
   f.close()

   object=json.loads(buffer)
  
   k=0
   for key, value in object.items():
       if key=="RelatedTopics":
          for i in value:
              for k2, v2 in i.items():
                   if k2=="Result":
                      if len(v2)>0: 
                         newbuffer=v2.split("</a>")
                         if k==0:
                             print(searchstring,"is",newbuffer[1])
                             k+=0    
                                                    


