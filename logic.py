# logic.py

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
           wyswietl_gwiazdy(False)  
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


def dodaj_gwiazde(nazwa: str = None, odleglosc: float = None):
    """
    Została zachowana możliwość użycia w trybie konsolowym (interfejs),
    ale także można wywoływać z GUI, podając argumenty.
    """
    if nazwa is None or odleglosc is None:
        input1 = input("Podaj nazwe gwiazdy: ")
        input2 = float(input("Podaj odleglosc gwiazdy od Ziemi: "))
        nowa_gwiazda = Gwiazda(input1, input2)
    else:
        nowa_gwiazda = Gwiazda(nazwa, odleglosc)
    
    if any(gwiazda.nazwa.lower() == nowa_gwiazda.nazwa.lower() for gwiazda in gwiazdy):
        raise ValueError(f"Gwiazda o nazwie '{nowa_gwiazda.nazwa}' już istnieje.")

    gwiazdy.append(nowa_gwiazda)
    print(f"Dodano: {nowa_gwiazda}")

def zapisz_do_pliku(filepath: str):
    """
    Zapisuje wszystkie gwiazdy z listy `gwiazdy` do wskazanego pliku.
    """
    try:
        with open(filepath, "w") as file:
            for gwiazda in gwiazdy:
                file.write(f"{gwiazda.nazwa},{gwiazda.odleglosc}\n")
        print(f"Dane zostały zapisane do pliku: {filepath}")
    except Exception as e:
        print(f"Błąd podczas zapisywania pliku: {e}")

def wyswietl_gwiazdy(print_out: bool = True):
    if not gwiazdy:
        print("Brak gwiazd")
        return []
    
    # Sortowanie po odległości - tak, jak było w merge_sort
    merge_sort(gwiazdy)
    if print_out == False:
        for id, gwiazda in enumerate(gwiazdy, start=1):
            print(f"{id}. {gwiazda}")
    return gwiazdy


def usun_gwiazde(index: int = None):
    """
    Została zachowana możliwość pracy w konsoli,
    ale także można wywoływać z GUI z odpowiednim indeksem.
    """
    if index is None:
        if not gwiazdy:
            print("Brak gwiazd")
            return
        wyswietl_gwiazdy()
        while True:
            wybor = int(input("Podaj numer gwiazdy do usuniecia: "))
            if (1 <= wybor <= len(gwiazdy)):
                usunieta = gwiazdy.pop(wybor - 1)
                print("Usunieto:", usunieta)
                return
            else:
                print("Podaj odpowiedni znak")
    else:
        if 0 <= index < len(gwiazdy):
            usunieta = gwiazdy.pop(index)
            print(f"Usunięto: {usunieta}")
        else:
            print("Nieprawidłowy indeks")


def wyszukaj_gwiazde(query: str = None):
    """
    Wyszukiwanie liniowe (po fragmencie nazwy), zostaje niezmienione.
    """
    if query is None:
        query = input("Podaj fragment nazwy gwiazdy: ")
    wyniki = [gwiazda for gwiazda in gwiazdy if query.lower() in gwiazda.nazwa.lower()]
    if wyniki:
        for gwiazda in wyniki:
            print(gwiazda)
    else:
        print("Nie znaleziono gwiazd")
    return wyniki

def dodaj_z_pliku(filepath: str = None):
    """
    Dodaje gwiazdy z pliku do istniejącej listy, unikając duplikatów nazw.
    """
    global gwiazdy
    if filepath is None:
        filepath = input("Podaj ścieżkę do pliku: ")
    
    dodane = 0
    try:
        # Wczytujemy dane z pliku
        with open(filepath, "r") as file:
            for line in file:
                if line.strip():  # Ignorujemy puste linie
                    nazwa, odleglosc = line.split(",")
                    nazwa = nazwa.strip()
                    odleglosc = float(odleglosc.strip())
                    
                    # Sprawdzamy, czy gwiazda o tej nazwie już istnieje
                    if any(gwiazda.nazwa.lower() == nazwa.lower() for gwiazda in gwiazdy):
                        print(f"Pominięto duplikat: {nazwa}")
                        continue
                    
                    # Dodajemy nową gwiazdę
                    dodaj_gwiazde(nazwa, odleglosc)
                    dodane += 1
    except Exception as e:
        raise e
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
                i += 1
            else:
                arr[k] = prawa[j]
                j += 1
            k += 1
        while i < len(lewa):
            arr[k] = lewa[i]
            i += 1
            k += 1
        while j < len(prawa):
            arr[k] = prawa[j]
            j += 1
            k += 1


# ---------------- Dodatkowe wyszukiwanie binarne (pokazowe) ----------------
def binary_search(sorted_arr, target: str):
    """
    Przykładowa implementacja wyszukiwania binarnego po nazwie gwiazdy.
    UWAGA: szuka dokładnego dopasowania (arr[mid].nazwa == target).
           Jeśli chcesz szukać fragmentów, trzeba by przerobić kryteria.
    """
    left = 0
    right = len(sorted_arr) - 1
    target = target.lower()

    while left <= right:
        mid = (left + right) // 2
        current = sorted_arr[mid].nazwa.lower().strip()

        if current == target:
            return mid
        elif current < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


if __name__ == "__main__":
    interfejs()
