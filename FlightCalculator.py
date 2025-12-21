import numpy as N
import os
from datetime import datetime

#--------------------------------Validering av input------------------------------#
class Validering:
    def __init__(self, Lägsta_Värde=None, Högsta_Värde=None, Tid="Tid"):
        self.Lägsta_Värde = Lägsta_Värde
        self.Högsta_Värde = Högsta_Värde
        self.Tid = Tid

    def Validera(self, Fråga):
        while True:
            Svar = input(Fråga)

            if self.Tid == "Tid":
                if self.Validera_tid(Svar):
                    return Svar.zfill(4)
                else:
                    print("Fel: Ogiltigt tidsformat!")
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
        if not (tid.isdigit() and 1 <= len(tid) <= 4):
            return False
        tid = tid.zfill(4)
        hh = int(tid[:2])
        mm = int(tid[2:])
        return 0 <= hh <= 23 and 0 <= mm <= 59

#---------------------------------------------------------------------------------#

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
TID_Validering = Validering(Tid="Tid")
#---------------------------------------------------------------------------------#

#------------------------------------Funktioner-----------------------------------#
def Uträkning_TAS():
    os.system("cls" if os.name == "nt" else "clear")
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
    os.system("cls" if os.name == "nt" else "clear")
    WS = WS_Validering.Validera("Skriv Vindhastighet(Knop): ")
    TAS = TAS_Validering.Validera("Skriv TrueAirspeed(Knop): ")
    WD = WD_Validering.Validera("Skriv Vindriktning: ")
    MT = MT_Validering.Validera("Skriv Magnetisk Track: ")

    WA = (WD - MT) % 360
    Formel = (WS / TAS) * N.sin(N.radians(WA))
    if abs(Formel) > 1:
        print("Fel: Vindkomponenten är för stor för att beräkna WCA.\n")
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
    os.system("cls" if os.name == "nt" else "clear")
    TAS = TAS_Validering.Validera("Skriv TrueAirspeed(Knop): ")
    WS = WS_Validering.Validera("Skriv Vindhastighet(Knop): ")
    WD = WD_Validering.Validera("Skriv Vindriktning: ")
    MH = MH_Validering.Validera("Skriv Magnetisk kurs: ")

    WA = (WD - MH) % 360
    GS = N.sqrt(TAS**2 + WS**2 - 2*TAS*WS*N.cos(N.radians(WA)))

    print(f"Hastigheten över marken är: {GS:.1f} Knop")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_TH():
    os.system("cls" if os.name == "nt" else "clear")
    ALT = ALT_Validering.Validera("Skriv Flygplatsens höjd över havet(Fot): ")    
    QNH = QNH_Validering.Validera("Skriv aktuellt QNH: ")

    TH = (ALT + ((STD - QNH) * 27))        
    
    print(f"Tryckhöjden är: {TH:.1f} fot")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_DH():
    os.system("cls" if os.name == "nt" else "clear")
    ALT = ALT_Validering.Validera("Skriv Flygplatsens eller Flygplanets höjd över havet(Fot): ")    
    QNH = QNH_Validering.Validera("Skriv aktuellt QNH: ")
    OAT = Temp_Validering.Validera("Skriv aktuell temperatur(°C): ")

    TH = (ALT + ((STD - QNH) * 27))     
    K_ISA = ISA + (-2 * (TH / 1000))
    DH = TH + (120 * (OAT - K_ISA))

    print(f"Densitetshöjden är: {DH:.1f} fot")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_VK():
    os.system("cls" if os.name == "nt" else "clear")
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
    os.system("cls" if os.name == "nt" else "clear")
    ALT = ALT_Validering.Validera("Skriv flygplanets höjd över havet(Fot): ")
    GND = ALT_Validering.Validera("Skriv stationens höjd över havet(Fot): ")

    RR = 1.225 * (N.sqrt(ALT) + N.sqrt(GND))
          
    print(f"Räckvidden till stationen från {ALT:.1f} fot är: {RR:.1f} nautiska mil!")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_BT():
    os.system("cls" if os.name == "nt" else "clear")
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
    print("9 - Avsluta Programmet")

    Svar = input("\nVal: ")
    if not Svar.isdigit():
        input("Fel: Endast siffror får skrivas!, Tryck ENTER för att fortsätta!")
        return True
    
    Val = int(Svar)
    if Val == 1:
        Uträkning_TAS()
    elif Val == 2:
        Uträkning_WCA()
    elif Val == 3:
        Uträkning_GS()
    elif Val == 4:
        Uträkning_TH()
    elif Val == 5:
        Uträkning_DH()
    elif Val == 6:
        Uträkning_VK()
    elif Val == 7:
        Uträkning_RR()
    elif Val == 8:
        Uträkning_BT()
    elif Val == 9:
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
