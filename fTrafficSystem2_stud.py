# Given studentversion av:
# Trafik system 1
# TvÃ¥ filer (lane1, lane2) och ett trafikljus (light) mellan dem.
# Och en kÃ¶, fÃ¶re lane2..
# lane1 - light - lane2 - kÃ¶
# Uppgift:
# I klassen TrafficSystem1 skall metoden number_in_system()
# modifieras.

from fVehicleAndLane_Stud import Lane, Vehicle
from fLight_Stud import Light
from fDestinations import Destinations
from time import sleep  # behÃ¶vs fÃ¶r sleep-fkn
import statistics as stat

class TrafficSystem2:
    """Representerar ett trafik system"""

    # Konstruktorn
    def __init__(self):
        self.time = 0   # Tiden Ã¤r noll, initialt
        self.lane_west = Lane(8)  # Fil efter trafikljuset
        self.lane_south = Lane(8)  # Fil framfÃ¶r trafikljuset
        self.lane_que = Lane(11)
        self.light_west = Light(14, 6) # Trafikljus, period 14, green period 6
        self.light_south = Light(14, 4)
        self.queue = [] # KÃ¶n lÃ¤ngst till hÃ¶ger Ã¤r initialt tom
        self.generator = Destinations() # skapar ett Destinations-objekt
        self.block = " "
        self.temp = ""
        self.createdvehicles = 0
        self.countedw = 0
        self.counteds = 0
        self.blockedtime = 0
        self.quetime = 0
        self.timew = []
        self.times = []
        
    # Skriver ut trafiksystemet vid aktuell tid som exvis
    #   26: [WSSSW](G)[SWWSW]  ['W', 'S']
    # dvs tiden, filen efter trafikljuset, trafikljuset, filen framfÃ¶r trafikljuset, kÃ¶n
    def snapshot(self):
        # Skapa en strÃ¤ng som representerar kÃ¶n
        sq = str([x.get_destination() for x in self.queue])
        # Skapa en strÃ¤ng med vÃ¤rdet pÃ¥ self.time hÃ¶gerjusterat Ã¶ver 4 positioner
        stime = '%4d' % (self.time) + ": "
        snr = '%2d' % (self.number_in_system())
        # Bygg upp strÃ¤ngen med alla dess bestÃ¥ndsdelar
        s = stime + '('+snr+') ' + str(self.light_west) + str(self.lane_west) + str(self.block) + str(self.lane_que) + "  " + sq + "\n           " + str(self.light_south) + str(self.lane_south)
        print(s)
        
    # Stegar trafiksystemet frÃ¥n vÃ¤nster till hÃ¶ger
    def step(self):
        self.temp = str(self.lane_que.get_first())
        self.time += 1
        if self.light_west.is_green(): # Om trafikljuset Ã¤r grÃ¶nt...
            # Flytta trafikljuset frÃ¥n lane2 till lane1
            try:
                self.lane_west.get_first().get_destination() == "W"
                self.countedw += 1
                self.timew.append(self.time - self.lane_west.get_first().get_borntime())
            except:
                pass
            self.lane_west.remove_first()
        self.light_west.step()
        self.lane_west.step()
            
        if self.light_south.is_green():
            try:
                self.lane_south.get_first().get_destination() == "S"
                self.counteds += 1
                self.times.append(self.time - self.lane_south.get_first().get_borntime())
            except:
                pass
            self.lane_south.remove_first()
        self.light_south.step()
        self.lane_south.step()

        destination = self.generator.step() # Ger S, W eller None frÃ¥n generatorn
        if destination != None: # Om nytt fordon:
            # Skapa fordonet och lÃ¤gg det sist i kÃ¶n
            self.queue.append(Vehicle(destination, self.time))
            self.createdvehicles += 1
        
        if self.lane_west.last_free():
            try:
                if self.lane_que.get_first().get_destination() == "W":
                    self.lane_west.enter(self.lane_que.get_first())
                    self.lane_que.remove_first()
            except:
                pass
        
        if self.lane_south.last_free():
            try:
                if self.lane_que.get_first().get_destination() == "S":
                    self.lane_south.enter(self.lane_que.get_first())
                    self.lane_que.remove_first()
            except:
                pass
        
        
        self.lane_que.step()

        if self.temp == str(self.lane_que.get_first()) and self.lane_que.get_first() != None:
            self.block = "*"
            self.blockedtime += 1
        elif self.temp != str(self.lane_que):
            self.block = " "

        # Om det finns minst ett fordon i kÃ¶n OCH sista positionen i lane2 Ã¤r ledig:
        if len(self.queue) > 0 and self.lane_que.last_free():
            # Flytta fordonet frÃ¥n fÃ¶rsta position i kÃ¶n till sista position i lane2.
            self.lane_que.enter(self.queue.pop(0))
        
        if len(self.queue) > 0:
            self.quetime += 1


    # BerÃ¤knar och returnerar hur mÃ¥nga fordon som fÃ¶r tillfÃ¤llet finns i trafikssystemet
    # dvs summan av fordon i de bÃ¥da filerna (lane1, lane2) och i kÃ¶n (queue).
    # Denna metod skall modifieras
    def number_in_system(self):
        s = self.lane_west.number_in_lane()
        s += self.lane_south.number_in_lane()
        s += self.lane_que.number_in_lane()
        return s
    
    def print_statistics(self):
        print("Statistics after 100 timesteps:\n")
        print("Created vehicles: " + str(self.createdvehicles))
        print("In system       : " + str(self.number_in_system()) + "\n")
        print("At exit            West      South")
        print("Vehicles out:       " + str(self.countedw) + "       " + str(self.counteds))
        print("Minimal time:       " + str(min(self.timew)) + "       " + str(min(self.times)))
        print("Maximal time:       " + str(max(self.timew)) + "       " + str(max(self.times)))
        print("Mean time   :       " + str(round(stat.mean(self.timew), 2)) + "    " + str(round(stat.mean(self.times),2)))
        print("Median time :       " + str(stat.median(self.timew)) + "       " + str(stat.median(self.times)))
        print("Blocked     :       " + str(self.blockedtime) + "%")
        print("Queue       :       " + str(self.quetime) + "%")
        

# Funktion som testkÃ¶r TrafficSystem1
def main():
    ts = TrafficSystem2()
    for i in range(100):
        ts.snapshot()
        ts.step()
        sleep(0.1) # VÃ¤nta 100 ms
    print('\nFinal state:')
    ts.snapshot()
    ts.print_statistics()

# TestkÃ¶r main
# if __name__ == '__main__':
main()

"""
NÃ¤r koden kÃ¶rs bÃ¶r fÃ¶ljande skrivas ut
   0: ( 0) [.....](G)[.....]  []
   1: ( 0) [.....](G)[....S]  []
   2: ( 0) [.....](G)[...SS]  []
   3: ( 0) [.....](G)[..SSS]  []
   4: ( 0) [.....](G)[.SSSS]  []
   5: ( 0) [.....](G)[SSSSS]  []
   6: ( 0) [....S](G)[SSSSW]  []
   7: ( 0) [...SS](G)[SSSWS]  []
   8: ( 0) [..SSS](R)[SSWSS]  []
   9: ( 0) [.SSS.](R)[SSWSS]  ['S']
  10: ( 0) [SSS..](G)[SSWSS]  ['S', 'W']
  11: ( 0) [SS..S](G)[SWSSS]  ['W', 'W']
  12: ( 0) [S..SS](G)[WSSSW]  ['W', 'S']
  13: ( 0) [..SSW](G)[SSSWW]  ['S', 'W']
  14: ( 0) [.SSWS](G)[SSWWS]  ['W', 'S']
  15: ( 0) [SSWSS](G)[SWWSW]  ['S', 'S']
  16: ( 0) [SWSSS](G)[WWSWS]  ['S', 'S']
  17: ( 0) [WSSSW](G)[WSWSS]  ['S', 'W']
  18: ( 0) [SSSWW](R)[SWSSS]  ['W', 'S']
  19: ( 0) [SSWW.](R)[SWSSS]  ['W', 'S', 'W']
  20: ( 0) [SWW..](G)[SWSSS]  ['W', 'S', 'W', 'W']
  21: ( 0) [WW..S](G)[WSSSW]  ['S', 'W', 'W', 'S']
  22: ( 0) [W..SW](G)[SSSWS]  ['W', 'W', 'S', 'W']
  23: ( 0) [..SWS](G)[SSWSW]  ['W', 'S', 'W', 'W']
  24: ( 0) [.SWSS](G)[SWSWW]  ['S', 'W', 'W']
  25: ( 0) [SWSSS](G)[WSWWS]  ['W', 'W', 'S']
  26: ( 0) [WSSSW](G)[SWWSW]  ['W', 'S']
  27: ( 0) [SSSWS](G)[WWSWW]  ['S']
  28: ( 0) [SSWSW](R)[WSWWS]  []
  29: ( 0) [SWSW.](R)[WSWWS]  []
  30: ( 0) [WSW..](G)[WSWWS]  ['W']
  31: ( 0) [SW..W](G)[SWWSW]  ['S']
  32: ( 0) [W..WS](G)[WWSWS]  []
  33: ( 0) [..WSW](G)[WSWS.]  []
  34: ( 0) [.WSWW](G)[SWS..]  []
  35: ( 0) [WSWWS](G)[WS..W]  []
  36: ( 0) [SWWSW](G)[S..W.]  []
  37: ( 0) [WWSWS](G)[..W..]  []
  38: ( 0) [WSWS.](R)[.W..S]  []
  39: ( 0) [SWS..](R)[W..S.]  []
  40: ( 0) [WS...](G)[W.S.W]  []
  41: ( 0) [S...W](G)[.S.WS]  []
  42: ( 0) [...W.](G)[S.WS.]  []
  43: ( 0) [..W.S](G)[.WS.W]  []
  44: ( 0) [.W.S.](G)[WS.W.]  []
  45: ( 0) [W.S.W](G)[S.W..]  []
  46: ( 0) [.S.WS](G)[.W...]  []
  47: ( 0) [S.WS.](G)[W....]  []
  48: ( 0) [.WS.W](R)[.....]  []
  49: ( 0) [WS.W.](R)[.....]  []
  50: ( 0) [S.W..](G)[....W]  []
  51: ( 0) [.W...](G)[...W.]  []
  52: ( 0) [W....](G)[..W..]  []
  53: ( 0) [.....](G)[.W...]  []
  54: ( 0) [.....](G)[W...W]  []
  55: ( 0) [....W](G)[...W.]  []
  56: ( 0) [...W.](G)[..W..]  []
  57: ( 0) [..W..](G)[.W...]  []
  58: ( 0) [.W...](R)[W...W]  []
  59: ( 0) [W....](R)[W..W.]  []
  60: ( 0) [.....](G)[W.W.W]  []
  61: ( 0) [....W](G)[.W.W.]  []
  62: ( 0) [...W.](G)[W.W.W]  []
  63: ( 0) [..W.W](G)[.W.W.]  []
  64: ( 0) [.W.W.](G)[W.W..]  []
  65: ( 0) [W.W.W](G)[.W...]  []
  66: ( 0) [.W.W.](G)[W....]  []
  67: ( 0) [W.W.W](G)[.....]  []
  68: ( 0) [.W.W.](R)[....W]  []
  69: ( 0) [W.W..](R)[...W.]  []
  70: ( 0) [.W...](G)[..W..]  []
  71: ( 0) [W....](G)[.W...]  []
  72: ( 0) [.....](G)[W...W]  []
  73: ( 0) [....W](G)[...W.]  []
  74: ( 0) [...W.](G)[..W..]  []
  75: ( 0) [..W..](G)[.W...]  []
  76: ( 0) [.W...](G)[W...W]  []
  77: ( 0) [W...W](G)[...W.]  []
  78: ( 0) [...W.](R)[..W.S]  []
  79: ( 0) [..W..](R)[.W.S.]  []
  80: ( 0) [.W...](G)[W.S..]  []
  81: ( 0) [W...W](G)[.S..W]  []
  82: ( 0) [...W.](G)[S..WS]  []
  83: ( 0) [..W.S](G)[..WS.]  []
  84: ( 0) [.W.S.](G)[.WS.W]  []
  85: ( 0) [W.S..](G)[WS.W.]  []
  86: ( 0) [.S..W](G)[S.W.S]  []
  87: ( 0) [S..WS](G)[.W.S.]  []
  88: ( 0) [..WS.](R)[W.S.S]  []
  89: ( 0) [.WS..](R)[WS.S.]  []
  90: ( 0) [WS...](G)[WSS..]  []
  91: ( 0) [S...W](G)[SS...]  []
  92: ( 0) [...WS](G)[S....]  []
  93: ( 0) [..WSS](G)[....W]  []
  94: ( 0) [.WSS.](G)[...W.]  []
  95: ( 0) [WSS..](G)[..W..]  []
  96: ( 0) [SS...](G)[.W...]  []
  97: ( 0) [S....](G)[W...W]  []
  98: ( 0) [....W](R)[...W.]  []
  99: ( 0) [...W.](R)[..W..]  []

Slutlig status:
 100: ( 0) [..W..](G)[.W..W]  []
"""