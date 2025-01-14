#tu bedzie logika apki

class Gwiazda:
    def __init__(self, nazwa: str, odleglosc: float):
        self.nazwa = nazwa
        self.odleglosc = odleglosc

    def __str__(self):
        return f"{self.nazwa} | {self.odleglosc}"
    
gwiazdy = []

def interfejs():
    while True:
        merge_sort(gwiazdy)
        print("\nGwiazdozbior ;-)")
        print("[0] Dodaj Gwiazde")
        print("[1] Wyswietl Gwiazdy")
        print("[2] Usun Gwiazde")
        print("[3] Wyszukaj Gwiazdy")
        print("[4] Dodaj Gwiazdy z pliku")
        print("[5] Zakoncz program")
        wybor = input("Wybierz opcje: ")
        if (wybor == "0"):
           dodaj_gwiazde() 
        elif (wybor == "1"):
           wyswietl_gwiazdy()  
        elif (wybor == "2"):
           usun_gwiazde() 
        elif (wybor == "3"):
           wyszukaj_gwiazdy()    
        elif (wybor == "4"):
            dodaj_z_pliku() 
        elif (wybor == "5"):
            print("Koniec programu")
            exit()
        else:
            print("Podaj odpowiedni znak")
    

def dodaj_gwiazde():
    input1 = input("Podaj nazwe gwiazdy: ")
    input2 = float(input("Podaj odleglosc gwiazdy od Ziemi: "))

    nowa_gwiazda = Gwiazda(input1, input2)
    gwiazdy.append(nowa_gwiazda)
    print(f"Dodano: {nowa_gwiazda}")
    
def wyswietl_gwiazdy():
    if not gwiazdy:
        print("Brak gwiazd")
        return
    
    i = 1
    print(f"Wszystkie gwiazdy: ")
    for i, gwiazda in enumerate(gwiazdy, start=1):
        print(i, gwiazda)

def usun_gwiazde():
    if not gwiazdy:
        print("Brak gwiazd")
        return
    wyswietl_gwiazdy()
    while True:
        wybor = int(input("Podaj numer gwiazdy do usuniecia: "))
        if (wybor >= 1 and wybor <= len(gwiazdy)):
            usunieta = gwiazdy.pop(wybor - 1)
            print("Usunieto:", usunieta)
            return
        else:
                print("Podaj odpowiedni znak")

def wyszukaj_gwiazdy():
    szukaj_po = input("Wprowadź czesc nazwy gwiazdy: ").strip().lower()
    if not szukaj_po:
        print("Podaj niepusty fragment")
        return
    
    pasujace = []
    for i, gwiazda in enumerate(gwiazdy, start=1):
        if szukaj_po in gwiazda.nazwa.lower():
            pasujace.append((i,gwiazda))

    if pasujace:
        for i, gwiazda in pasujace:
            print(i,gwiazda)
    else:
        print("Nie znaleziono pasujacych gwiazd")


def dodaj_z_pliku():
    file = open(r"C:\Users\pmaci\Desktop\pliktest.txt", "r")
    for line in file:
        if line:
            line.strip()
            nazwa, odleglosc = line.split(",")
            nowa_gwiazda = Gwiazda(nazwa.strip(), float(odleglosc.strip()))
            gwiazdy.append(nowa_gwiazda)
    file.close()
    print("Dodano gwiazdy")

def merge_sort(arr):
    if len(arr) > 1:
        srodek = len(arr)//2
        lewa = arr[0:srodek]
        prawa = arr[srodek:len(arr)]

        merge_sort(lewa)
        merge_sort(prawa)

        i = j = k = 0

        while i < len(lewa) and j < len(prawa):
            if lewa[i].odleglosc <= prawa[j].odleglosc:
                arr[k] = lewa[i]
                i+=1
            else:
                arr[k] = prawa[j]
                j+=1
            k+=1
        while i < len(lewa):
            arr[k] = lewa[i]
            i+=1
            k+=1
        while j < len(prawa):
            arr[k] = prawa[j]
            j+=1
            k+=1
        

interfejs()
