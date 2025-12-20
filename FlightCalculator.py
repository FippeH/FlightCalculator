import numpy as N
import os

class Validering:
    def __init__(self, Lägsta_Värde=None, Högsta_Värde=None):
        self.Lägsta_Värde = Lägsta_Värde
        self.Högsta_Värde = Högsta_Värde

    def Validera(self, Fråga):
        while True:
            Svar = input(Fråga)
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

STD = 1013
ISA = 15
WS_Validering = Validering()
TAS_Validering = Validering()
WD_Validering = Validering(0, 360)
MT_Validering = Validering(0, 360)
MH_Validering = Validering(0, 360)
Höjd_Validering = Validering()
QNH_Validering = Validering(930, 1070)
Temp_Validering = Validering(-50, 50)
Val_Validering = Validering(1, 6)
IAS_Validering = Validering()

def Uträkning_TAS():
    ALT = Höjd_Validering.Validera("Skriv Flygplanets höjd över havet i fot: ")  
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
    WS = WS_Validering.Validera("Skriv Vindhastighet: ")
    TAS = TAS_Validering.Validera("Skriv TrueAirspeed: ")
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
    TAS = TAS_Validering.Validera("Skriv TrueAirspeed: ")
    WS = WS_Validering.Validera("Skriv Vindhastighet: ")
    WD = WD_Validering.Validera("Skriv Vindriktning: ")
    MH = MH_Validering.Validera("Skriv Magnetisk kurs: ")

    WA = (WD - MH) % 360
    GS = N.sqrt(TAS**2 + WS**2 - 2*TAS*WS*N.cos(N.radians(WA)))

    print(f"Hastigheten över marken är: {GS:.1f} Knop")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_TH():
    ALT = Höjd_Validering.Validera("Skriv Flygplatsens höjd över havet i fot: ")    
    QNH = QNH_Validering.Validera("Skriv aktuellt QNH: ")

    TH = (ALT + ((STD - QNH) * 27))        
    
    print(f"Tryckhöjden är: {TH:.1f} fot")
    input("\nTryck Enter för att fortsätta...")

def Uträkning_DH():
    ALT = Höjd_Validering.Validera("Skriv Flygplatsens eller Flygplanets höjd över havet i fot: ")    
    QNH = QNH_Validering.Validera("Skriv aktuellt QNH: ")
    OAT = Temp_Validering.Validera("Skriv aktuell temperatur(°C): ")

    TH = (ALT + ((STD - QNH) * 27))     
    K_ISA = ISA + (-2 * (TH / 1000))
    DH = TH + (120 * (OAT - K_ISA))

    print(f"Densitetshöjden är: {DH:.1f} fot")
    input("\nTryck Enter för att fortsätta...")

def Välj_Uträkning():
    os.system("cls" if os.name == "nt" else "clear")
    print("\nVälj en av funktionerna i listan nedan.\n")
    print("1 - Räkna True Airspeed")
    print("2 - Räkna Vindupphållningsvinkel")
    print("3 - Räkna Markhastighet")
    print("4 - Räkna Tryckhöjd")
    print("5 - Räkna Densitetshöjd")
    print("6 - Avsluta Programmet")

    Val = Val_Validering.Validera("\nVal: ")
    
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
        print("Programmet avslutas!")
        return
    else:
        print("Fel: Ogiltigt val!")
        return

def main():
    while True:
        Välj_Uträkning()

if __name__=="__main__":
    main()
