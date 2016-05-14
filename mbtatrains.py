##
## http request to utilize MBTA API
##
## Graphically represent live location of MBTA trains on the Red Line (Boston)
##
## This code is a little bit brute force.  But is works nicely.
## It could be cleaned up to be more compact.
##
## 5/6/16 - Lockwood 
##
## MBTA - Vehicles by Route
##
##
##
from graphics import *

import urllib
from urllib.request import urlopen

import json
import time

## 42.2735695   North Quincy
## 71.0314803


class NestedDictionary(object):
    def __init__(self,value,file_flag,filename):
        self.value=value
        self.file_flag=file_flag
        self.filename=filename

    def printNest(self,depth):
        if self.file_flag==YES:
           f=open(self.filename,'a')
        spacer="--------------------"
        station=""
        latitude=0
        longitude=0
        newgroup=0
        if type(self.value)==type(dict()):
           for kk, vv in self.value.items():
              if (type(vv)==type(dict())):
                 print("KEY")
                 print(spacer[:depth],kk)
                 if self.file_flag==YES:
                    ostring=spacer[:depth]+kk+LINEFEED
                    f.write(ostring)
                 vvv=(NestedDictionary(vv,self.file_flag,self.filename))
                 depth=depth+3
                 vvv.printNest(depth)
                 depth=depth-3
              else:
                 if (type(vv)==type(list())):
                    for i in vv:
                      vvv=(NestedDictionary(i,self.file_flag,self.filename))
                      depth=depth+3
                      vvv.printNest(depth)
                      depth=depth-3
                 else:
##                  print(spacer[:depth],kk,vv) 
                    if self.file_flag==YES:
                       ostring=spacer[:depth]+kk+SPACE+vv+LINEFEED
                       f.write(ostring)
                    if kk=='stop_lat':
                       latitude=vv
                       newgroup+=1
                    if kk=='stop_lon':
                       longitude=vv
                       newgroup+=1
                    if kk=='parent_station_name':
                       station=vv
                       newgroup+=1
              if newgroup==3:
                 print('***',station,latitude,longitude)
                 StationList.append([station,latitude,longitude])
                 newgroup=0

        if self.file_flag==YES:
           f.close()

class NestedDictionary2(object):
    def __init__(self,value,file_flag,filename):
        self.value=value
        self.file_flag=file_flag
        self.filename=filename

    def printNest2(self,depth):
        if self.file_flag==YES:
           f=open(self.filename,'a')
        spacer="--------------------"
        station=""
        latitude=0
        longitude=0
        newgroup=0
        if type(self.value)==type(dict()):
           for kk, vv in self.value.items():
              if (type(vv)==type(dict())):
                 print("KEY")
                 print(spacer[:depth],kk)
                 if self.file_flag==YES:
                    ostring=spacer[:depth]+kk+LINEFEED
                    f.write(ostring)
                 vvv=(NestedDictionary2(vv,self.file_flag,self.filename))
                 depth=depth+3
                 vvv.printNest2(depth)
                 depth=depth-3
              else:
                 if (type(vv)==type(list())):
                    for i in vv:
                      vvv=(NestedDictionary2(i,self.file_flag,self.filename))
                      depth=depth+3
                      vvv.printNest2(depth)
                      depth=depth-3
                 else:
##                  print(spacer[:depth],kk,vv) 
                    if self.file_flag==YES:
                       ostring=spacer[:depth]+kk+SPACE+vv+LINEFEED
                       f.write(ostring)
                    if kk=='vehicle_lat':
                       latitude=vv
                       newgroup+=1
                    if kk=='vehicle_lon':
                       longitude=vv
                       newgroup+=1
                    if kk=='vehicle_id':
                       print("HEY - vehicle id:",vv)
                       vehicle=vv
                       newgroup+=1
              if newgroup==3:
                 print('***',vehicle,latitude,longitude)
                 TrainList.append([vehicle,latitude,longitude])
                 newgroup=0

        if self.file_flag==YES:
           f.close()
## MAIN PROGRAM

YES=1
NO=0
BEGINNING=1
END=0
TRUE=1
FALSE=1


FILENAME="stationsbyroute.txt"
FILENAME2="vehiclesbyroute.txt"
LINEFEED="\n"
SPACE=" "
COMMA=","
StationList=[]
TrainList=[]
MyTextList=[]
TriangleList=[]

XMAX=1200
YMAX=640

win = GraphWin("MBTA TRAINS",XMAX,YMAX)

## MASTER MAP

GPSx_min=-70.98
GPSx_max=-71.15
GPSy_min=42.19
GPSy_max=42.42

## DOWNTOWN - BASICALLY ZOOM INTO A SMALLER GEO AREA

## GPSx_min=-71.04
## GPSx_max=-71.08
## GPSy_min=42.33
## GPSy_max=42.37

## BRAINTREE AREA - BASICALLY ZOOM INTO A SMALLER GEO AREA

## GPSx_min=-70.99
## GPSx_max=-71.09
## GPSy_min=42.19
## GPSy_max=42.30

x_granularity=abs(GPSx_max-GPSx_min)
y_granularity=abs(GPSy_max-GPSy_min)

realX_width=XMAX
realY_height=YMAX
 
xratio=realX_width/x_granularity
yratio=realY_height/y_granularity

##
## My developer key: VDSv7V_z3EeBpVC7FJHWRw
##


## http1="http://realtime.mbta.com/developer/api/v2/stopsbylocation?api_key=wX9NwuHnZU2ToO7GmGR9uw&lat=42.2735695&lon=-71.0314803&format=json"

## http2="http://realtime.mbta.com/developer/api/v2/routesbystop?api_key=wX9NwuHnZU2ToO7GmGR9uw&stop=place-bbsta&format=json"

## http2="http://realtime.mbta.com/developer/api/v2/routesbystop?api_key=wX9NwuHnZU2ToO7GmGR9uw&stop="
## json_format="&format=json"


http3="http://realtime.mbta.com/developer/api/v2/stopsbyroute?api_key=VDSv7V_z3EeBpVC7FJHWRw&route=Red&format=json"


## DISPLAY STATIONS

urlstring=http3
req=urllib.request.Request(urlstring)
response = urllib.request.urlopen(req)
buffer=response.read().decode("utf-8")
  
f=open("mbtatracker.txt",'w')
f.write(buffer)
f.close()

object3=json.loads(buffer)

writetofile=NO
writetofile=YES
if writetofile==YES:
   f=open(FILENAME,'w')
   f.write("HEADER\n")
   f.close()

p=NestedDictionary(object3,writetofile,FILENAME)
p.printNest(0)

previous_x=0
previous_y=0

for i in StationList:
    print("Station",i[0],"Latitude",i[1],"Longitude",i[2])

    gpslat=float(i[1])
    gpslon=float(i[2])

## convert GPS coords to proporational X, Y

    x=XMAX-(abs(gpslon)-abs(GPSx_min))*xratio
    y=YMAX-(abs(gpslat)-abs(GPSy_min))*yratio

    if previous_x !=0 and previous_y !=0:
## draw line connecting stations

       rail=Line( Point(x,y),Point(previous_x,previous_y))  
       rail.setOutline('red')
       rail.setFill('red')
       rail.setWidth(4)
       rail.draw(win)

    previous_x=x
    previous_y=y

    pt = Point(x,y)
    pt.draw(win)
    cir = Circle(pt, 5)
    cir.setOutline('red')
    cir.setFill('red')
    cir.draw(win)

    MyText=Text(Point(x+60,y-15),i[0])
    MyText.draw(win)


## DISPLAY TRAINS

## Vehicles by Route

http4="http://realtime.mbta.com/developer/api/v2/vehiclesbyroute?api_key=VDSv7V_z3EeBpVC7FJHWRw&route=Red&format=json"

while TRUE:

   urlstring=http4
   req=urllib.request.Request(urlstring)
   response = urllib.request.urlopen(req)
   buffer=response.read().decode("utf-8")
  
## f=open("mbtatracker.txt",'w')
## f.write(buffer)
## f.close()

   object4=json.loads(buffer)

   p=NestedDictionary2(object4,writetofile,FILENAME2)
   p.printNest2(0)

   for i in TrainList:
       print("Train",i[0],"Latitude",i[1],"Longitude",i[2])

       gpslat=float(i[1])
       gpslon=float(i[2])

## convert GPS coords to proporational X, Y

       x=XMAX-(abs(gpslon)-abs(GPSx_min))*xratio
       y=YMAX-(abs(gpslat)-abs(GPSy_min))*yratio

       print("For i",x,y,i[0])
     
       pt1=Point(x,y)
       pt2=Point(x-10,y-15)
       pt3=Point(x+10,y-15)

       Triangle=Polygon([pt1,pt2,pt3])
       Triangle.setOutline('green')
       Triangle.setFill('green')
       Triangle.draw(win)
       TriangleList.append(Triangle)

       MyText=Text(Point(x,y+15),i[0])
       MyText.draw(win)
       MyTextList.append(MyText) 

   time.sleep(10)
   for i in MyTextList:
       i.undraw()
   for i in TriangleList:
       i.undraw()
   MyTextList=[]
   TrainList=[]
   TriangleList=[]