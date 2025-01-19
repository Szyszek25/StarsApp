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
        print("\nGwiazdozbior ;-)")
        print("[0] Dodaj Gwiazde")
        print("[1] Wyswietl Gwiazdy")
        print("[2] Usun Gwiazde ")
        print("[3] Wyszukaj Gwiazde ")
        print("[4] Dodaj Gwiazdy z pliku ")
        print("[5] Zakoncz program ")
        wybor = input("Wybierz opcje: ")
        if (wybor == "0"):
           dodaj_gwiazde() 
        elif (wybor == "1"):
           wyswietl_gwiazdy()  
        elif (wybor == "2"):
           usun_gwiazde() 
        elif (wybor == "3"):
           wyszukaj_gwiazde()    
        elif (wybor == "4"):
            dodaj_z_pliku() 
        elif (wybor == "5"):
            print("Koniec programu")
            exit()
        else:
            print("Podaj odpowiedni znak")

def dodaj_gwiazde(nazwa: str, odleglosc:float):
    #input1 = input("Podaj nazwe gwiazdy: ")
    #input2 = float(input("Podaj odleglosc gwiazdy od Ziemi: "))

    nowa_gwiazda = Gwiazda(nazwa,odleglosc)
    gwiazdy.append(nowa_gwiazda)
    print(f"Dodano: {nowa_gwiazda}")
    
def wyswietl_gwiazdy():
    if not gwiazdy:
        print("Brak gwiazd")
        return
    
    merge_sort(gwiazdy)
    return gwiazdy
    
    #i = 1
    #print(f"Wszystkie gwiazdy: ")
    #for gwiazda in gwiazdy:
        #print(i, gwiazda)
       # i+=1

def usun_gwiazde(index: int):
    """
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
    """
    #if 0 <= index < len(gwiazdy):
    usunieta = gwiazdy.pop(index)
    print(f"Usunięto: {usunieta}")  # do gui
    #else:
        #print("Nieprawidłowy indeks")  # do gui


def wyszukaj_gwiazde(query: str):
    wyniki = [gwiazda for gwiazda in gwiazdy if query.lower() in gwiazda.nazwa.lower()]
    return wyniki

def dodaj_z_pliku(filepath: str):
    dodane = 0
    file = open(filepath, "r")
    for line in file:
        if line:
            line.strip()
            nazwa, odleglosc = line.split(",")
            nowa_gwiazda = Gwiazda(nazwa.strip(), float(odleglosc.strip()))
            gwiazdy.append(nowa_gwiazda)
            dodane+=1
    file.close()
    #print("Dodano gwiazdy")
    return dodane

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
        
if __name__ == "__main__":
    interfejs()
