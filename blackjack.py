##
## cards3.py - Bob Lockwood - 5/9/2016
##
## complete redesign and rewrite from scratch - new object design
##

import random

Message=''
Playername=''


class Table(object):
   def __init__(self,deck):
       self.deck=deck 
       self.master_deck=CardPile()
       self.iter_master_deck=CardPile()
      
   def PrepTheDeck(self,number_of_decks):
       for suit in Suits:
           for number in Numbers:
               value=CardValue[number]
               name=number+OF+suit
               card=Card(UP,name,number,suit,value)
               self.deck.list_of_cards.append(card)
       
       n=0
       while n<number_of_decks:
           for d in self.deck.list_of_cards:
              self.master_deck.list_of_cards.append(d)
           n+=1
    
       random.shuffle(self.master_deck.list_of_cards)
       iter_list=iter(self.master_deck.list_of_cards)
       self.master_deck.list_of_cards=iter_list
       return(self.master_deck)
 
   def SetUpChairs(self,dealer):
       chairlist=[]
       NullPlayer=Player(NULL,NULL,NULL,NULL,NULL,NULL,NULL)
       chairlist.append(Chair(1,EMPTY,RIGHT,MIDDLE,NullPlayer))
       chairlist.append(Chair(2,EMPTY,MIDRIGHT,MIDBOTTOM,NullPlayer))
       chairlist.append(Chair(3,EMPTY,CENTER,BOTTOM,NullPlayer))
       chairlist.append(Chair(4,EMPTY,MIDLEFT,MIDBOTTOM,NullPlayer))
       chairlist.append(Chair(5,EMPTY,LEFT,MIDDLE,NullPlayer))
       chairlist.append(Chair(6,OCCUPIED,CENTER,TOP,dealer))
       return(chairlist)

   def PickThePlayers(self,playerlist,dealer,guests):

       ## HARD CODE THIS FOR NOW

       PlayerName=input("Hi. What's your name? ")
      
       NullChair=Chair(NULL,NULL,NULL,NULL,NULL)
      
       Hand1=CardPile()
       Hand2=CardPile()
       Hand3=CardPile()

       playerlist.append(Player(OPPONENT,guests[0],NullChair,Hand1,2000,0,WAITING))
       playerlist.append(Player(LIVE_PLAYER,PlayerName,NullChair,Hand2,2000,0,WAITING))
       playerlist.append(Player(OPPONENT,guests[1],NullChair,Hand3,2000,0,WAITING))
       playerlist.append(dealer)
       return(playerlist)

   def AssignSeats(self,playerlist,chairlist):
       for c in chairlist:
          NullHand=CardPile()
          if c.order==1:
             c.player=playerlist[0]
             c.status=OCCUPIED
             c.player.chair=c
          elif c.order==3:
             c.player=playerlist[1]
             c.status=OCCUPIED
             c.player.chair=c
          elif c.order==5:
             c.player=playerlist[2]
             c.status=OCCUPIED
             c.player.chair=c
          elif c.order==6:
             c.player=playerlist[3]
             c.status=OCCUPIED
             c.player.chair=c
          ## dealer is already assigned
       return(chairlist)
 

   def SettleBets(chairs):
      for ch in chairs:
          if ch.player.type==DEALER:
             dealer_total=ch.player.hand.count
             if ch.player.hand.count>21:
                ch.player.status=BUSTED
                dealer_total=0                            ## busted - zero out value so others win
             
      for ch in chairs:
          if ch.status==OCCUPIED:
             if ch.player.type!=DEALER:
                total=ch.player.hand.count
                if total>21:
                    ch.player.status=BUSTED                ## busted - zero out bet
                else:
                    if dealer_total>21:
                       ch.player.purse+=2*ch.player.bet    ## win
                       ch.player.status=WON
                    if total==dealer_total:
                       ch.player.purse+=ch.player.bet      ## restore bet
                       ch.player.status=PUSH               ## push 
                    elif total>dealer_total:
                       ch.player.purse+=2*ch.player.bet    ## win 
                       ch.player.status=WON
                    elif total<dealer_total:
                       ch.player.status=LOST               ## lost - add nothing back to purse - essentially lost bet from purse
                


   def ClearCards(chairs):
       for ch in chairs:
           if ch.status==OCCUPIED:
              ch.player.hand.list_of_cards=[]
              ch.player.hand.count=0
              ch.player.hand.ace=0
              ch.player.bet=0
              ch.player.status=WAITING


class Chair(object):
   def __init__(self,order,status,x,y,player):
       self.order=order
       self.status=status    ## empty or occupied
       self.x=x
       self.y=y
       self.player=player
       

class Player(object):
   def __init__(self,type,name,chair,hand,purse,bet,status):
       self.type=type
       self.name=name
       self.chair=chair
       self.hand=hand
       self.purse=purse
       self.bet=bet
       self.status=status

   def PlaceYourBet(self):
       if self.type != DEALER:
          if self.type==OPPONENT:
             self.bet=STANDARD_BET
             self.purse-=self.bet
          elif self.type==LIVE_PLAYER:
              status=INVALID
              while status==INVALID:
                 r=input("What is your bet:")
                 if r.isnumeric():
                    bet=int(r)                 
                    if bet < MINIMUM_BET:
                       status=INVALID
                    elif bet > self.purse:
                       status=INVALID
                    else:
                       self.bet=bet
                       self.purse-=bet
                       status=VALID
                 else:
                    status=INVALID




   def DealerAction(self,deck):
      stop=NO
      self.status=PLAYING
      Message="Dealer's turn."
      while stop==NO:
         if self.hand.count<17:
            Display.clear()
            Display.build(SHOW_DEALER)
            Display.print()
            r=input("Hit <ENTER> to continue.")
            deck.Deal(self)                                # HIT - take another card
         else:
            stop=YES
            self.status=DONE


   def OpponentAction(self,deck):
      Message=self.name+"'s turn."
      stop=NO
      r=input("Hit <ENTER> to continue.")
      while stop==NO and self.status!=BUSTED:
         if self.hand.count<18:
            if self.hand.count<15 or self.hand.ace>0:
               deck.Deal(self)            # HIT - take another card
               if self.hand.count>21:
                  self.status=BUSTED
               Display.clear()
               Display.build(NORMAL)
               Display.print()
               r=input("Hit <ENTER> to continue.")
            else:
               stop=YES
               self.status=HOLD
         else:
            stop=YES
            self.status=HOLD

   
   def LivePlayerAction(self,deck):
      Message="Your turn."
      stop=NO
      while stop==NO and self.status!=BUSTED:
          r=input("Enter (h) for Hit or (s) for Stay.")
          if r=='h':
             deck.Deal(self)
             if self.hand.count>21:
                self.status=BUSTED
             Display.clear()
             Display.build(NORMAL)
             Display.print()
          else:
             stop=YES
             self.status=HOLD


   def PlayHand(self,deck):
       if self.type != DEALER:
          if self.type==OPPONENT:
             self.OpponentAction(deck)
          elif self.type==LIVE_PLAYER:
             self.LivePlayerAction(deck)
       elif self.type==DEALER:
           self.DealerAction(deck)


class CardPile(object):          # this is for any group of cards - dealer's deck, and all player hands, live player and opponents
   def __init__(self):
       self.list_of_cards=[] 
       self.count=0   
       self.ace=0                                        ## tracks number of aces in hand

   def Deal(self,player):
       card=next(self.list_of_cards)                     ## get next card in iter list
       if card.value==11 and card.number=='Ace':
          player.hand.ace+=1
          print("DEALT ACE",player.name,card.name,player.hand.count)
          r=input()
       player.hand.list_of_cards.append(card)            ## add card to player's hand
       player.hand.count+=card.value
       if player.hand.count>21:
          if player.hand.ace>0:
             print("CONVERT ACE TO ONE",player.hand.ace,player.hand.count)
             player.hand.count-=10
             player.hand.ace-=1
          else:
             player.status=BUSTED

class Card(object):
   def __init__(self,face,name,number,suit,value):
       self.face=face       ## up or down
       self.name=name
       self.number=number   ## Ace,King,Queen,Jack,etc.
       self.suit=suit
       self.value=value


class Screen(object):                    # this class object is to manage the screen output
   def __init__(self,chairlist):         # the core methods are chart() and screenline()
        self.chairlist=chairlist         # chart() specifies the words and phrases to output
        self.screen_buffer=[]            # screenline() builds the individual output buffer line

   def clear(self):
       self.screen_buffer=[]
       n=0
       while n<35:
           self.screen_buffer.append(str(n)) 
           n+=1   
     
   def screenline(self,x,y,phrase):

       if len(self.screen_buffer[y])==1:
          temp=SPACE*x+phrase

       elif len(self.screen_buffer[y]) > x:
          l=len(self.screen_buffer[y])
          p=x+len(phrase)
          old=self.screen_buffer[y][p:l]
          temp=SPACE*x+phrase+old
     
       else:
          l=len(self.screen_buffer)
          p=len(phrase)
          tempx=self.screen_buffer[y][p:l]
          t=len(tempx)
          temp=tempx+SPACE*(x-t)+phrase
 
       self.screen_buffer.remove(self.screen_buffer[y])
       self.screen_buffer.insert(y,temp)
 
   def chart(self,chair,show):
       self.screenline(chair.x,chair.y,chair.player.name+SPACE*10)
       offset=2
       cloop_count=0
       for c in chair.player.hand.list_of_cards:
           if chair.player.type!=DEALER or show==SHOW_DEALER:
              self.screenline(chair.x,chair.y+offset,'> '+c.name+SPACE*10)
           elif chair.player.type==DEALER and cloop_count==0:
              self.screenline(chair.x,chair.y+offset,'<HIDDEN CARD>'+SPACE*10)
           else:
              self.screenline(chair.x,chair.y+offset,'> '+c.name+SPACE*10)
           offset+=1
           cloop_count+=1
       offset+=1

       if chair.player.type != DEALER:
           self.screenline(chair.x,chair.y+offset,'Card Total:'+str(chair.player.hand.count)+SPACE*10)
           offset+=1
           self.screenline(chair.x,chair.y+offset,'Bet:'+str(chair.player.bet)+SPACE*10)
           offset+=1
           self.screenline(chair.x,chair.y+offset,'Chips:'+str(chair.player.purse)+SPACE*10)
           offset+=1
           self.screenline(chair.x,chair.y+offset,'Status:'+str(chair.player.status)+SPACE*10)
      
       elif chair.player.type == DEALER:
           if show==SHOW_DEALER:
               self.screenline(chair.x,chair.y+offset,'Card Total:'+str(chair.player.hand.count)+SPACE*10)
               offset+=1
           self.screenline(chair.x,chair.y+offset,'Status:'+str(chair.player.status)+SPACE*10) 

       self.screenline(10,28,Message)    ## doesn't work yet - message continues to be blank
##     print("MESSAGE:",Message)
##     r=input()

   def build(self,show):
       for c in self.chairlist:
            if c.status==OCCUPIED:
               self.chart(c,show)   
 
   def print(self):
       for l in self.screen_buffer:
           print(l[2:])   
            



## GLOBAL VARIABLES

CardValue={ 'One':1,'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8,'Nine':9,     \
            'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11  }

Suits=['Spades','Hearts','Diamonds','Clubs']

Numbers=['Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']


Guests=['Billy The Kid','Jesse James','Wild Bill Hickock','Charlie Chaplain','Groucho Marx',      \
        'Elvis Presley','Rock Hudson','Fred Astair','Humphrey Bogart','Al Capone','Bill Haley',   \
        'Chuck Berry','Jimi Hendrix','Jim Morrison']

YES='Yes'
NO='No'
TRUE='True'
FALSE='False'
UP='Up'
DOWN='Down'
EMPTY='Empty'
OCCUPIED='Occupied'
OF=' of '
PASS='Pass'
STAY='Stay'
OVER='Over'
BUSTED='Busted'
DEALER='Dealer'
OPPONENT='Opponent'
LIVE_PLAYER='Live Player'
NULL=""
NullList=[]
SPACE=' '
DOT='.'
NORMAL='Normal'
SHOW_DEALER='Show Dealer'
BUSTED='Busted'
WON='Won'
LOST='Lost'
PUSH='Push'
PLAYING='Playing'
WAITING='Waiting'
HOLD='Hold'
DEALING='Dealing'
VALID='Valid'
INVALID='Invalid'
DONE="Done"

STANDARD_BET=100
MINIMUM_BET=50

RIGHT=90
MIDRIGHT=65
CENTER=50
LEFT=10
MIDLEFT=30

TOP=4
MIDTOP=8
MIDDLE=12
MIDBOTTOM=16
BOTTOM=20

Message=''

## MAIN PROGRAM

ListOfCards=[]
PlayerList=[]
Deck=CardPile()                                                ## instatiate the deck
OurGame=Table(Deck)                                            ## instaiate the table
Deck=OurGame.PrepTheDeck(5)                                    ## build the full deck of cards

## PlayerList=OurGame.PickThePlayers()     ## ask how many players / assign opponents / how many decks
## OurGame.AssignSeats(PlayerList)         ## put players in chairs
##
## for now assume 3 players - including LIVE PLAYER
## assume LIVE PLAYER chooses position 3
## assume 1 and 5 are Guest Opponents

NullChair=Chair(NULL,NULL,NULL,NULL,NULL)
DealerHand=CardPile()

print()
print()
print()
print()
print("*************** B L A C K   J A C K **********************")
loop=0
while loop<25:
   print()
   loop+=1

Dealer=Player(DEALER,DEALER,NullChair,DealerHand,NULL,NULL,WAITING)       ## Create the dealer
ChairList=OurGame.SetUpChairs(Dealer)                                   ## Create the chairs at the table
random.shuffle(Guests)                                                  ## Randomize the Guest names
PlayerList=OurGame.PickThePlayers(PlayerList,Dealer,Guests)             ## Build the playerlist
ChairList=OurGame.AssignSeats(PlayerList,ChairList)                     ## Put players in specific seats

Display=Screen(ChairList)                                               ## instantiate the Screen class as object Display
Display.clear()
Display.build(NORMAL)
Display.print()
## Display welcome page

while (TRUE):

   Display.clear()                                                   ## Start new hand
   Display.build(NORMAL)
   Display.print()
   for p in PlayerList:
       p.PlaceYourBet()                                              ## Place your bets

   for p in PlayerList:
       Deck.Deal(p)                                                  ## Deal one card to each player
       if p.type==DEALER:
          p.status=DEALING
##        p.hand.list_of_cards[0].face=DOWN                          ## NOT WORKING!! Force first dealer card face down

   for p in PlayerList:                                              
       Deck.Deal(p)                                                  ## Deal second card to each player

   for p in PlayerList:                                              ## loop thru each player and let them play out their hand
       p.status=PLAYING

       Display.clear()
       Display.build(NORMAL)
       Display.print()
##     r=input("Hit <Enter> to continue.")

       p.PlayHand(Deck)                                              ## play individual hand including the dealer

       Display.clear()
       if p.name==DEALER:
          Display.build(SHOW_DEALER)
          Display.print()
          r=input("Hit <Enter> to continue.")

   Table.SettleBets(ChairList)

   Display.clear()
   Display.build(SHOW_DEALER)
   Display.print()
   r=input("GET READY FOR NEW HAND. Press <ENTER> to continue")

   Table.ClearCards(ChairList)
   









