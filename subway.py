##
##  SUBWAY 7- OOP means to create Subway Simulation
##
##  *** REDESIGN 4/29/16 - Lockwood
##
##  - updated 5/4/16 Lockwood
##
##  Try to redesign around Train being central information object.
##
##  Build objects for system, lines, routes, stations, trains & people
##
##  This is a working version that builds all of the stations and all of the routes.
##  You can display the whole system along with trains. 
##
##  This version of SUBWAY will include people.
##
##  People will be set up with location, origin of travel, destination.  The system will
##  track if the person is at home, in world, at station, on train.  You will be able to 
##  see how many people are at each station and on which trains.  
##
##  Long term view is to keep characteristics about people, such that you will know who
##  is at these locations - some details about people could be name, gender
##
##  - updated 5/4/16 Lockwood
##
##  Things to add and fix - set up Routes to be "PAIRED" such that when turning around, they match the reverse route. - FIXED
##                        - at end of travel, swap orig-dest so person can go back to where they came from - do some sort of time delay
##                        - swap out "IN WORLD" to "IN TOWN" or something better
##                        - create TripPlanner to plan travel with possible LEGS, add Legs list to Person, this will include changing lines
##                        - this will also fix people getting on wrong train when any train pulls into their station
##

import time



## GLOBAL VARIABLES

## Status for Trains

AT_STATION = "at station"
ENTERING_STATION = "entering station"
LEAVING_STATION = "leaving station"
EN_ROUTE = "en route to"

## Locations for People

HOME="at home"
WORLD="in world"
OSTATION="at origin station"
DSTATION="at destination station"
TRAIN="on train"

BEGINNING="beginning trip"
ENDING="ending trip"

FROM_HOME="from home"
FROM_SUBWAY="from subway"


STATION_DICTIONARY =  { 'Stations':[ {'id':'S001','name':'Braintree', 'line':'Red'},
                                     {'id':'S002','name':'Quincy', 'line':'Red'},
                                     {'id':'S003','name':'North Quincy', 'line':'Red'},
                                     {'id':'S004','name':'JFK-UMass','line':'Red'},
                                     {'id':'S005','name':'Andrew','line':'Red'},
                                     {'id':'S006','name':'Broadway','line':'Red'},
                                     {'id':'S007','name':'Savin Hill','line':'Red'},
                                     {'id':'S008','name':'Bowdoin','line':'Blue'},
                                     {'id':'S009','name':'Government Center','line':'Blue'},   
                                     {'id':'S010','name':'State Station','line':'Blue'},
                                     {'id':'S011','name':'Aquarium','line':'Blue'},
                                     {'id':'S012','name':'Maverick Station','line':'Blue'},
                                     {'id':'S013','name':'Airport Station','line':'Blue'},
                                     {'id':'S014','name':'Wood Island Station','line':'Blue'},   
                                     {'id':'S015','name':'Orient Heights Station','line':'Blue'},
                                     {'id':'S016','name':'Suffolk Downs Station','line':'Blue'},
                                     {'id':'S017','name':'Beachmont Station','line':'Blue'},
                                     {'id':'S018','name':'Revere Beach Station','line':'Blue'},
                                     {'id':'S019','name':'Wonderland Station','line':'Blue'},
                                     {'id':'EOL','name':'end of line','line':'All'}
                                 
                                   ]
 }

SYSTEM_DICTIONARY = { 'System' : { 'Red Line' : { 'R001' : { 'Pair':'R002','Route':[ 'S001','S002','S003','S004','S005','S006','EOL' ]},
                                                  'R002' : { 'Pair':'R001','Route':[ 'S006','S005','S004','S003','S002','S001','EOL' ]},
                                                  'R003' : { 'Pair':'R004','Route':[ 'S006','S005','S004','S007','EOL']},
                                                  'R004' : { 'Pair':'R003','Route':[ 'S007','S004','S005','S006','EOL']}
                                                },
                                  'Blue Line' : { 'B001' : { 'Pair':'B002','Route':[ 'S008','S009','S010','S011','S012','S013','S014','S015','S016','S017','S018','S019','EOL' ]},
                                                  'B002' : { 'Pair':'B001','Route':[ 'S019','S018','S017','S016','S015','S014','S013','S012','S011','S010','S009','S008','EOL' ]}
                                                }
                                 }
}

TRAIN_DICTIONARY = { 'Trains' : [ { 'id':'T001','number':'8521','route':'R001','station':'S001','state':AT_STATION },
                                  { 'id':'T002','number':'6192','route':'R002','station':'S005','state':ENTERING_STATION },
                                  { 'id':'T003','number':'1960','route':'R003','station':'S006','state':LEAVING_STATION },
                                  { 'id':'T004','number':'5632','route':'B001','station':'S008','state':EN_ROUTE },
                                  { 'id':'T005','number':'8825','route':'B002','station':'S017','state':AT_STATION }
                                ]
                    }

PEOPLE_DICTIONARY = { 'People' : [ {'id':'P001','name':'Joe Smith','location':HOME,'origin':'S016','destination':'S009' },
                                   {'id':'P002','name':'James Jameson','location':HOME,'origin':'S009','destination':'S014' },
                                   {'id':'P003','name':'Jessy James','location':HOME,'origin':'S002','destination':'S005' }
                                 ]
                    }



HomeList=[]
WorldList=[]

MasterPeopleList=[]
StationList=[]
TrainList=[]
LineList=[]

TRUE=1
FALSE=0
YES=1
NO=0

GO_TO_NEXT_STATION=2

NULL=""
EOL='EOL'

## END OF GLOBAL VARIABLES


class PersonalInfo(object):
     def __init__(self, name, beginning_ending_status, location):
        self.name=name
        self.beginning_ending_status=beginning_ending_status
        self.location=location   

class People(object):
     def __init__(self, id, personal_info_object, origin_station_object, destination_station_object):
         self.id=id
         self.personal_info_object=personal_info_object
         self.origin_station_object=origin_station_object
         self.destination_station_object=destination_station_object
         self.train_object=NULL
         self.LegList=[]
         self.LOOP=0          ## need to fix this to address more than one LEG

     def dequeue(self, incoming_object,incoming_list):
         incoming_list.index(incoming_object)         ## find index of this object in order to specify removal
         incoming_list.remove(incoming_object)                        ## remove item from list

     def enqueue(self, incoming_object, incoming_list):
         incoming_list.append(incoming_object)

     def NextMove(self):
        location=self.personal_info_object.location
##      print("NEXT MOVE",self.personal_info_object.name,location)
        if location==HOME:
           self.GoIntoWorld(FROM_HOME)
        elif location==WORLD:
           self.GoToStation()
        elif location==OSTATION:
           self.GetOnTrain()
        elif location==TRAIN:
           self.GetOffTrain()
        elif location==DSTATION:
           self.GoIntoWorld(FROM_SUBWAY)

     def GoIntoWorld(self,from_where):
       self.personal_info_object.location=WORLD
       if from_where==FROM_HOME:
          self.dequeue(self,HomeList)
          self.enqueue(self,WorldList)
       elif from_where==FROM_SUBWAY:
          self.dequeue(self,self.destination_station_object.S_PeopleList)
          self.enqueue(self,WorldList)

     def GoToStation(self):
         if self.personal_info_object.beginning_ending_status==BEGINNING:    ## If ENDING then leave in World - Don't go to station.
           self.personal_info_object.location=OSTATION
           self.dequeue(self,WorldList)
           self.enqueue(self,self.origin_station_object.S_PeopleList)

     def GetOnTrain(self):
##      print("GET ON TRAIN REQUEST FOR",self.personal_info_object.name)
##      CAN ONLY GET ON TRAIN IF TRAIN IS AT THE STATION, OTHERWISE DO NOTHING AND WAIT FOR TRAIN TO ARRIVE
##      print("TRAIN FLAG",self.origin_station_object.train_flag)
        if self.origin_station_object.train_flag==YES:
           if self.origin_station_object.train_object.station_object==self.origin_station_object:  ## just double check that train is at correct station
              if self.LegList[self.LOOP].routeid==self.origin_station_object.train_object.route_object.routeid:  ## check to make sure train is going the right way
                 print(self.personal_info_object.name,"IS GETTING ON TRAIN",self.origin_station_object.train_object.number)
                 self.personal_info_object.location=TRAIN
                 self.dequeue(self,self.origin_station_object.S_PeopleList)
                 self.enqueue(self,self.origin_station_object.train_object.T_PeopleList)         ## figure out what Train is at station - add to PeopleList for Train
                 self.train_object=self.origin_station_object.train_object                       ## specify train object to people object
        
     def GetOffTrain(self):
##      CAN ONLY GET OFF TRAIN IF AT A STATION AND AT YOUR DESTINATION STATION OF CHOICE
##      print("GETTING OFF TRAIN",self.personal_info_object.name,"GETTING OFF OF TRAIN",self.destination_station_object.train_object.number)
##      print("TRAIN FLAG",self.destination_station_object.train_flag)
##
## THIS PROBLEM HAS BEEN FIXED!
##
## Funny problem - code checks to see if train is at destination train in order to get off, but it doesn't check for the right train.
## Currently, it tries to have passenger leave train, but right train is not at station.  During enqueue we get an error that item
## does not exist to take off list, which is correct, because we are check the train status incorrectly.  Need to check that actual
## train that this guy is on.
##
## This will be fixed after we develop PlanRoute() - this will make sure person gets on train with matching route
##
        if self.train_object.station_object==self.destination_station_object:
           if self.destination_station_object.train_flag==YES:
              if self.destination_station_object.train_object.station_object==self.destination_station_object:  ## just double checking to make sure train is at our station
                 self.personal_info_object.location=DSTATION
                 self.dequeue(self,self.destination_station_object.train_object.T_PeopleList)
                 self.enqueue(self,self.destination_station_object.S_PeopleList)
                 self.personal_info_object.beginning_ending_status=ENDING
                 self.train_object=NULL                                       ## remove train from people object       



     def PlanRoute(self):
##
##   When a person is created they are assigned an origin and a destination, but there are not assigned the path to get from one to the other.
##   This method will look at the stations and pick a route to get from one to the other.  This may require one or possible two train changes.
##   For this reason we will build a new list called Leg[].  This will be a list of routes required to get from one to the other.  The person will
##   execute the first Leg.  If there is another leg, then they will continue their travel on the next leg, until there are no more.
##   The first leg will be determined by seeing if the destination is on any of the routes that the origin is on.  If so, this is simple and there 
##   only be one leg.  If not, it get much more complex. To speed the checking process up for seeing what routes are available to each station we
##   need to add a new list to the station which list all routes that travel through that station. This routelist per station needs to be built
##   at initiation time.  See new method called BuildStationRouteLists().
##
##   Find origin on Line first - then look for Destination down the line to make sure we select the route going in the correct order.
##   Check all routes connected to the origin station.
##   One planned error in the system is that if there are two routes satsifying the request, only the first one will be chosen.  The after
##   affect of this is that a person may miss a train going to the right place, if it comes first and it is the 2nd route which was not chosed. Capiche!
##
        good_route=NO
        start_check=NO
        for route in self.origin_station_object.S_RouteList:
            print("PLAN ROUTE",route.routeid)
            for station in route.station_list_object:
                if station==self.origin_station_object:
                   start_check=YES
                if start_check==YES:
                   if station==self.destination_station_object:
                      good_route=YES
                      self.LegList.append(route)
                      break                        ## found route done - this is for simple case where destination is on same line as origin
        print("PERSON",self.personal_info_object.name,"is on route",self.LegList[0].routeid,"origin",self.origin_station_object.name,"destination",self.destination_station_object.name)





 

class State(object):
   
    def __init__(self,state):
        self.state=state
 
    def NextState(self):
        go_to_next_station=FALSE
        if self.state==AT_STATION:
           self.state=LEAVING_STATION
        elif self.state==LEAVING_STATION:
           self.state=EN_ROUTE
           go_to_next_station=TRUE
        elif self.state==EN_ROUTE:
           self.state=ENTERING_STATION
        elif self.state==ENTERING_STATION:
           self.state=AT_STATION
        elif self.state==EOL:
           go_to_next_station=TRUE
        else:
           print("Train STATE error! - invalid state.")
        
        if go_to_next_station==TRUE:
           return(GO_TO_NEXT_STATION)


class Train(object):

    def __init__(self,id,number,route_object,station_object,state_object):
        self.id=id
        self.number=number
        self.route_object=route_object
        self.station_object=station_object
        self.state_object=state_object
        self.T_PeopleList=[]

    def DisplayTrain(self):
         print("TRAIN",self.number,"(route",self.route_object.routeid,") on",self.route_object.line,   \
                "is",self.state_object.state,self.station_object.name)
         for t in self.T_PeopleList:
             print(t.personal_info_object.name)

    def NextStation(self):
         CurrentStation=self.station_object
         if self.state_object.state != EOL:
            RouteStationList=self.route_object.station_list_object
            Next=RouteStationList[RouteStationList.index(CurrentStation)+1]    ## increment to the next station
            if Next.id==EOL:                     ## IMPORTANT! DO NOT CHANGE STATION NAME TO EOL, BUT CHANGE STATE TO EOL
               self.state_object.state=EOL       ## TURN AROUND TRAIN
            else:
                self.station_object=Next
         elif self.state_object.state==EOL:
            self.TurnAround()

    def TurnAround(self):
         current_station=self.station_object.id  
         current_route=self.route_object.routeid 
         current_line=self.route_object.line
 
         nextrouteid=self.route_object.pairid     ## this is the paird route - to turn around on to
                                                  ## must look up the object in order for full update
         for line in LineList:
             if line.linename==current_line:
                for route in line.RouteList:
                    if route.routeid==nextrouteid:
                       self.route_object=route
                       self.state_object.state=AT_STATION


class Station(object):
    
   def __init__(self,id,name,line):
       self.id=id
       self.name=name
       self.line=line
       
       self.train_flag=NO       ## this is yes/no for whether or not train is at station
       self.train_object=Train(NULL,NULL,NULL,NULL,NULL)   ## a train object is assigned when train enters station
                                ## train object is removed when train leaves station
       self.S_PeopleList=[]
       self.S_RouteList=[]

   def DisplayStation(self):
         print(self.id,self.name)
         for train in TrainList:
             if train.station_object.id==self.id:
                print("--------------------- Train",train.number,"is",train.state_object.state)
             for r in self.S_RouteList:
                 print(r.routeid)


class Route(object):
   def __init__(self,routeid,pairid,line,station_list_object):
       self.routeid=routeid
       self.pairid=pairid
       self.line=line
       self.station_list_object=station_list_object

   def DisplayRoute(self):
       for i in self.station_list_object:
           i.DisplayStation()
   

class Line(object):
   def __init__(self,linename):
       self.linename=linename
       self.RouteList=[]

   def BuildRoute(self,line,route,pair,station_list_objects):
       print("WAIT - BuildRoute",line,route)
       for s in station_list_objects:
           print(s.id,s.name)
       NewRoute=Route(route,pair,line,station_list_objects)
       self.RouteList.append(NewRoute)
       return(NewRoute)
   
   def DisplayLine(self):
       for route in self.RouteList:
           print("The route is",route.routeid)
           route.DisplayRoute()


class SubwaySystem(object):
      
   def BuildStations(self,station_dict):
       for key, value in station_dict.items():
           for v in value:
               station=Station(v['id'],v['name'],v['line'])
               StationList.append(station)                           ## instantiate Station and append to StationList
##
## For each station we now need to build a station route list (S_RouteList) which keeps a list of all routes that travel 
## through each station.  This is needed for quick look up of station route information when planning routes (PlanRoutes).
##
                              

   def BuildSystem(self, system_dict):
       list_of_station_objects=[]
       for systemkey, lines in system_dict.items():
           for linekey, routes in lines.items():
               NewLine=Line(linekey)                          
               LineList.append(NewLine)
               for routekey, routeinfo in routes.items():
                   pairid=routeinfo['Pair']
                   stations=routeinfo['Route']
                   list_of_station_objects=[]
                   for s1 in stations:
                      for s2 in StationList:
                         if s1==s2.id:                             # find Station Object from station id number
                             list_of_station_objects.append(s2)                     
                   newroute=NewLine.BuildRoute(linekey,routekey,pairid,list_of_station_objects)
                   print("NEW ROUTE CREATED:",newroute.routeid)
## This seems redundant, but we need to do it this way.  We now need to add this new Route to each Stations S_RouteList.

                   for s3 in newroute.station_list_object:
                       s3.S_RouteList.append(newroute)           ## this adds this new route to the station for later reference
                       print("YEEHAW",s3.name,newroute.routeid,"just got added to S_RouteList")



   def DisplaySystem(self):
       print()
       print()
       print("DISPLAY SYSTEM")
       print()

       for line in LineList:
           print("The line name is",line.linename)
           line.DisplayLine()

   def GetRouteObject(self,route):
       print("GET ROUTE OBJECT",route)
       for i in LineList:
          for j in i.RouteList:
              print(j.routeid,route)
              if j.routeid==route:
                 return(j)          ## return Route object

   def GetStationObject(self,station):
       for s in StationList:
           if s.id==station:
              return(s)          ## return Station object

   def CommissionTrains(self, train_dict):
       for key, value in train_dict.items():
           for v in value:
               train_id=v['id']
               train_number=v['number']
               train_route=v['route']
               train_station=v['station']
               train_state=v['state']
               route_object=self.GetRouteObject(train_route)
               station_object=self.GetStationObject(train_station) 
               state_object=State(train_state)               
               NewTrain=Train(train_id,train_number,route_object,station_object,state_object)
               print("APPEND TRAIN TO LIST",train_number)
               TrainList.append(NewTrain)                                                      ## instantiate Train and append to TrainList

   def FindStation(self,station_object):
       for s in StationList:
           if s.id==station_object:
              return(s)               ## return station object in list


   def PopulatePeople(self, people_dict):
       for key, value in people_dict.items():
           for v in value:
               person_id=v['id']
               person_name=v['name']
               person_location=v['location']
               person_origin=v['origin']
               person_destination=v['destination']
               pinfo=PersonalInfo(person_name,BEGINNING,person_location)
               Ostation=self.FindStation(person_origin)
               Dstation=self.FindStation(person_destination)
               person=People(person_id,pinfo,Ostation,Dstation)        ## instatiate person
               MasterPeopleList.append(person)                         ## add person to master list
               if person_location==HOME:
                  HomeList.append(person)
               if person_location==WORLD: 
                  WorldList.append(person)
         
               person.PlanRoute()                                      ## plan route for each person - pick route to get between origin and destination




       print("PEOPLE LIST")
       for p in MasterPeopleList:
           print(p.personal_info_object.name,p.personal_info_object.location)

       print("HOME LIST")
       for h in HomeList:
           print(h.personal_info_object.name)
    
   def DisplayTrains(self):
       print()
       print("Here is a list of all of the trains and status.")
       for i in TrainList:
##         if i.number=="8521":
              i.DisplayTrain()

   def DisplayPeople(self):
       print()
       print("List of People")
       for m in MasterPeopleList:
           print(m.personal_info_object.name,m.personal_info_object.location,m.LegList[0].routeid)
           if m.personal_info_object.location==OSTATION:
              print(m.origin_station_object.name)
           elif m.personal_info_object.location==TRAIN:
              print(m.train_object.number)
              print("with destination",m.destination_station_object.name)
           elif m.personal_info_object.location==DSTATION:
              print(m.destination_station_object.name)

   def AdvanceTime(self):
       print("Advance Time")

       ## UPDATE ALL TRAINS 

       for train in TrainList:
           action=train.state_object.NextState()        ## advance status of train
           if action==GO_TO_NEXT_STATION:
              train.NextStation()
           if train.state_object.state==AT_STATION:           ## set train info to station
              train.station_object.train_flag=YES
              train.station_object.train_object=train        
           if train.state_object.state==LEAVING_STATION:      ## remove train info from station
              train.station_object.train_flag=NO
              train.station_object.train=NULL
                                  
       ## UPDATE ALL PEOPLE

       for person in MasterPeopleList:
           person.NextMove()                            ## advance status of person

##
## MAIN PROGRAM
##

TheT=SubwaySystem()

TheT.BuildStations(STATION_DICTIONARY)
TheT.BuildSystem(SYSTEM_DICTIONARY)
TheT.CommissionTrains(TRAIN_DICTIONARY)

## TheT.DisplaySystem()

TheT.PopulatePeople(PEOPLE_DICTIONARY)

## TheT.DisplaySystem()

## TheT.DisplayTrains()
## TheT.DisplayPeople()
while TRUE:
## time.sleep(5)
   r=input("**")
   TheT.AdvanceTime()
   TheT.DisplayTrains()
## TheT.DisplaySystem()
   TheT.DisplayPeople()
