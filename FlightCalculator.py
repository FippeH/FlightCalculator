import numpy as N
import os
from datetime import datetime
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup as BS

#--------------------------------Validering av input------------------------------#
class Validering:
    def __init__(self, Lägsta_Värde=None, Högsta_Värde=None, Tid=False, ICAO=False):
        self.Lägsta_Värde = Lägsta_Värde
        self.Högsta_Värde = Högsta_Värde
        self.Tid = Tid
        self.ICAO = ICAO

    def Validera(self, Fråga):
        while True:
            Svar = input(Fråga)

            if self.Tid:
                if self.Validera_tid(Svar):
                    return Svar.zfill(4)
                else:
                    print("Fel: Ogiltigt tidsformat!")
                    continue

            if self.ICAO:
                if len(Svar) == 4 and Svar.isalpha():
                    return Svar.upper()
                else:
                    print(f"Fel: {Svar.upper()} är inte en giltig ICAO-kod!\n")
                    continue

            try:
                Svar = Svar.replace(",",".")
                Nummer = float(Svar)

                if self.Lägsta_Värde is not None and Nummer < self.Lägsta_Värde:
                    print(f"Fel: Värdet är för lågt!\n")
                    continue

                if self.Högsta_Värde is not None and Nummer > self.Högsta_Värde:
                    print(f"Fel: Värdet är för högt!\n")
                    continue

                return Nummer
            except ValueError:
                print("Fel: Svaret får ej innehålla bokstäver!")

    def Validera_tid(self, tid):
        if not (tid.isdigit() and 3 <= len(tid) <= 4):
            return False
        tid = tid.zfill(4)
        hh = int(tid[:2])
        mm = int(tid[2:])
        return 0 <= hh <= 23 and 0 <= mm <= 59

#-----------------------Funktion för hämtning av väderdata------------------------#
def HämtaVäder(URL):
    try:
        AROweb = urlopen(URL)
        HTML = AROweb.read().decode("utf-8")
        HTML_PARSER = BS(HTML, "html.parser")
        Rapporter = HTML_PARSER.find_all("div", class_ = "tor-link-text-row")
        Väder = []

        for Lista in Rapporter:
            Väder.append(Lista.get_text().strip("\n").replace("\n", " "))
       
        return Väder        
    
    except HTTPError as e:
        print(f"Fel: Servern svarade med felkod {e.code}. Sidan kan vara nere eller ändrad.") 
        return []
    except URLError: 
        print("Fel: Ingen internetanslutning eller DNS-problem. Kontrollera nätverket.") 
        return [] 
    except Exception as e: 
        print(f"Ett oväntat fel inträffade: {e}")
        return []

#------------------------------------Variabler------------------------------------#
STD = 1013                              #Standard Barometriskt tryck (hPa)        |
ISA = 15                                #Standard ISA temperatur                  | 
WS_Validering = Validering()            #Vindhastighet                            | 
WD_Validering = Validering(0, 360)      #Vindriktning                             |  
MT_Validering = Validering(0, 360)      #Magnetikstrack                           |
MH_Validering = Validering(0, 360)      #Magnetiskkurs                            |
RW_Validering = Validering(0, 360)      #Bana                                     |
ALT_Validering = Validering()           #Höjd                                     |
QNH_Validering = Validering(930, 1070)  #Barometriskt tryck (hPa)                 |
Temp_Validering = Validering(-50, 50)   #Temperatur Celcius                       |
IAS_Validering = Validering()           #Indikeradhastighet                       |
TAS_Validering = Validering()           #True Airspeed                            |
TID_Validering = Validering(Tid=True)   #Tid                                      |
ICAO_Validering = Validering(ICAO=True) #Flyplats                                 | 
MET_URL = "https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=314&type=MET&icao=" # | 
TAF_URL = "https://aro.lfv.se/Links/Link/ViewLink?TorLinkId=315&type=MET&icao="#  | 
#---------------------------------------------------------------------------------#

#------------------------------------Funktioner-----------------------------------#
def Uträkning_TAS():
    ALT = ALT_Validering.Validera("Skriv Flygplanets höjd över havet(Fot): ")  
    IAS = IAS_Validering.Validera("Skriv Indikerad Hastighet(Knop): ")  
    QNH = QNH_Validering.Validera("Skriv aktuellt QNH: ")
    OAT = Temp_Validering.Validera("Skriv aktuell temperatur(°C): ")

    TH = (ALT + ((STD - QNH) * 27))     
    K_ISA = ISA + (-2 * (TH / 1000))
    DH = TH + (120 * (OAT - K_ISA))

    TAS = IAS * (1 + (DH / 1000) * 0.02)
    print(f"True airspeed är: {TAS:.1f}")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_WCA():
    WS = WS_Validering.Validera("Skriv Vindhastighet(Knop): ")
    TAS = TAS_Validering.Validera("Skriv TrueAirspeed(Knop): ")
    WD = WD_Validering.Validera("Skriv Vindriktning: ")
    MT = MT_Validering.Validera("Skriv Magnetisk Track: ")

    WA = (WD - MT) % 360
    Formel = (WS / TAS) * N.sin(N.radians(WA))
    if abs(Formel) > 1:
        print("Fel: Vindkomponenten är för stor för att beräkna WCA.\n")
        input("Tryck ENTER för att fortsätta...")
        return
    
    WCA = N.degrees(N.arcsin(Formel))
    if WCA > 180:
        WCA -= 360
    elif WCA < -180:
        WCA += 360
    
    MH = (WCA + MT) % 360

    print(f"Vindupphållningsvinkeln är: {WCA:.1f}°")
    print(f"Magnetisk kurs är: {MH:.1f}°")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_GS():
    TAS = TAS_Validering.Validera("Skriv TrueAirspeed(Knop): ")
    WS = WS_Validering.Validera("Skriv Vindhastighet(Knop): ")
    WD = WD_Validering.Validera("Skriv Vindriktning: ")
    MH = MH_Validering.Validera("Skriv Magnetisk kurs: ")

    WA = (WD - MH) % 360
    GS = N.sqrt(TAS**2 + WS**2 - 2*TAS*WS*N.cos(N.radians(WA)))

    print(f"Hastigheten över marken är: {GS:.1f} Knop")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_TH():
    ALT = ALT_Validering.Validera("Skriv Flygplatsens höjd över havet(Fot): ")    
    QNH = QNH_Validering.Validera("Skriv aktuellt QNH: ")

    TH = (ALT + ((STD - QNH) * 27))        
    
    print(f"Tryckhöjden är: {TH:.1f} fot")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_DH():
    ALT = ALT_Validering.Validera("Skriv Flygplatsens eller Flygplanets höjd över havet(Fot): ")    
    QNH = QNH_Validering.Validera("Skriv aktuellt QNH: ")
    OAT = Temp_Validering.Validera("Skriv aktuell temperatur(°C): ")

    TH = (ALT + ((STD - QNH) * 27))     
    K_ISA = ISA + (-2 * (TH / 1000))
    DH = TH + (120 * (OAT - K_ISA))

    print(f"Densitetshöjden är: {DH:.1f} fot")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_VK():
    RW = RW_Validering.Validera("Skriv banans riktning: ")
    WD = WD_Validering.Validera("Skriv Vindriktning: ")
    WS = WS_Validering.Validera("Skriv Vindhastighet(Knop): ")

    WA = (WD - RW) % 360
    WA_rad = N.radians(WA)
    SV = N.sin(WA_rad) * WS
    MV = N.cos(WA_rad) * WS
    
    if SV > 0:
        sidvind_riktning = "från höger"
    elif SV < 0:
        sidvind_riktning = "från vänster"
    else:
        sidvind_riktning = "ingen sidvind"

    if MV > 0:
        motvind_riktning = "motvind"
    elif MV < 0:
        motvind_riktning = "medvind"
    else:
        motvind_riktning = "ingen mot-/medvind"

    print(f"\nVindvinkel relativt till banan: {WA:.1f}°")
    print(f"Sidvindskomposant: {abs(SV):.1f} knop {sidvind_riktning}")
    print(f"Motvindskomposant: {abs(MV):.1f} knop {motvind_riktning}")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_RR():
    ALT = ALT_Validering.Validera("Skriv flygplanets höjd över havet(Fot): ")
    GND = ALT_Validering.Validera("Skriv stationens höjd över havet(Fot): ")

    RR = 1.225 * (N.sqrt(ALT) + N.sqrt(GND))
          
    print(f"Räckvidden till stationen från {ALT:.1f} fot är: {RR:.1f} nautiska mil!")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_BT():
    Tid_On = TID_Validering.Validera("Skriv ON-BLOCK tiden (HHMM): ")
    Tid_Off = TID_Validering.Validera("Skriv OFF-BLOCK tiden (HHMM): ")

    Tid_On = Tid_On.zfill(4)
    Tid_Off = Tid_Off.zfill(4)

    Format = "%H%M"
    ONBT = datetime.strptime(Tid_On, Format)
    OFFBT = datetime.strptime(Tid_Off, Format)

    if OFFBT < ONBT:
        OFFBT = OFFBT.replace(day=ONBT.day + 1)

    diff = OFFBT - ONBT
    minuter = diff.total_seconds() / 60
    BT = minuter / 60

    print(f"Blocktiden är {BT:.1f} timmar! ({minuter:.0f} minuter)")
    input("\nTryck Enter för att fortsätta...")

def Hämta_MET_TAF():
    Flygplats = ICAO_Validering.Validera("Skriv Flygplatsens ICAO kod: ")
    METAR = HämtaVäder(MET_URL) 
    TAF = HämtaVäder(TAF_URL) 
    
    print("\n--- METAR ---")
    hittad_met = False
    for rad in METAR:
        if rad.startswith(Flygplats):
            print(rad)
            hittad_met = True
    if not hittad_met:
        print(f"Ingen METAR hittades för {Flygplats}.")

    print("\n--- TAF ---")
    hittad_taf = False
    for rad in TAF:
        if rad.startswith(Flygplats):
            print(rad)

            hittad_taf = True
    if not hittad_taf:
        print(f"Ingen TAF hittades för {Flygplats}.")

    input("\nTryck Enter för att fortsätta...")


def Välj_Uträkning():
    os.system("cls" if os.name == "nt" else "clear")
    print("\nVälj en av funktionerna i listan nedan.\n")
    print("1 - Räkna TrueAirspeed")
    print("2 - Räkna Vindupphållningsvinkel")
    print("3 - Räkna Markhastighet")
    print("4 - Räkna Tryckhöjd")
    print("5 - Räkna Densitetshöjd")
    print("6 - Räkna Vindkomposant")
    print("7 - Räkna Radioräckvidd")
    print("8 - Räkna Blocktid")
    print("9 - Hämta METAR / TAF")
    print("10 - Avsluta Programmet")

    Svar = input("\nVal: ")
    if not Svar.isdigit():
        input("Fel: Endast siffror får skrivas!, Tryck ENTER för att fortsätta!")
        return True
    
    Val = int(Svar)

    Funktioner = { 
        1: Uträkning_TAS, 
        2: Uträkning_WCA, 
        3: Uträkning_GS, 
        4: Uträkning_TH, 
        5: Uträkning_DH, 
        6: Uträkning_VK, 
        7: Uträkning_RR, 
        8: Uträkning_BT,
        9: Hämta_MET_TAF 
        }
    
    if Val in Funktioner:
        os.system("cls" if os.name == "nt" else "clear")
        Funktioner[Val]()
        
    elif Val == 10:
        print("Programmet avslutas!")
        return False
    else:
        input("Fel: Ogiltigt val!, Tryck ENTER för att fortsätta!")
        return True
    return True

def main():
    while Välj_Uträkning():
        pass

if __name__=="__main__":
    main()
