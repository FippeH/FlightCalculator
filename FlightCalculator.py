import numpy as N

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

def Uträkning_WCA():
    WS_Validering = Validering()
    TAS_Validering = Validering()
    WD_Validering = Validering(0, 360)
    MT_Validering = Validering(0, 360)
    
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
    Välj_Uträkning()

def Uträkning_GS():
    WS_Validering = Validering()
    TAS_Validering = Validering()
    WD_Validering = Validering(0, 360)
    MH_Validering = Validering(0, 360)

    TAS = TAS_Validering.Validera("Skriv TrueAirspeed: ")
    WS = WS_Validering.Validera("Skriv Vindhastighet: ")
    WD = WD_Validering.Validera("Skriv Vindriktning: ")
    MH = MH_Validering.Validera("Skriv Magnetisk kurs: ")

    WA = (WD - MH) % 360
    GS = N.sqrt(TAS**2 + WS**2 - 2*TAS*WS*N.cos(N.radians(WA)))

    print(f"Hastigheten över marken är: {GS:.1f} Knop")
    input("\nTryck Enter för att fortsätta...")
    Välj_Uträkning()

def Uträkning_TH():
    STD = 1013
    
    Höjd_Validering = Validering()
    QNH_Validering = Validering(930, 1070)

    H = Höjd_Validering.Validera("Skriv Flygplatsens höjd över havet i fot: ")    
    D = QNH_Validering.Validera("Skriv aktuellt QNH: ")

    TH = (H + ((STD - D) * 27))        
    
    print(f"Tryckhöjden är: {TH:.1f} fot")
    input("\nTryck Enter för att fortsätta...")
    Välj_Uträkning()

def Uträkning_DH():
    STD = 1013
    ISA = 15

    Höjd_Validering = Validering()
    QNH_Validering = Validering(930, 1070)
    Temp_Validering = Validering(-50, 50)

    H = Höjd_Validering.Validera("Skriv Flygplatsens höjd över havet i fot: ")    
    D = QNH_Validering.Validera("Skriv aktuellt QNH: ")
    OAT = Temp_Validering.Validera("Skriv aktuell temperatur(°C): ")

    TH = (H + ((STD - D) * 27))     
    K_ISA = ISA + (-2 * (TH / 1000))
    DH = TH + (120 * (OAT - K_ISA))

    print(f"Densitetshöjden är: {DH:.1f} fot")
    input("\nTryck Enter för att fortsätta...")
    Välj_Uträkning()

def Välj_Uträkning():
    print("\nVälj en av funktionerna i listan nedan.\n")
    print("1 - Räkna Vindupphållningsvinkel")
    print("2 - Räkna Markhastighet")
    print("3 - Räkna Tryckhöjd")
    print("4 - Räkna Densitetshöjd")
    print("5 - Avsluta Programmet")

    Val_Validering = Validering(1, 5)

    Val = Val_Validering.Validera("\nVal: ")
    
    if Val == 1:
        Uträkning_WCA()
    elif Val == 2:
        Uträkning_GS()
    elif Val == 3:
        Uträkning_TH()
    elif Val == 4:
        Uträkning_DH()
    elif Val == 5:
        print("Programmet avslutas!")
        return
    else:
        print("Fel: Ogiltigt val!")
        return

def main():
    Välj_Uträkning()

if __name__=="__main__":
    main()
