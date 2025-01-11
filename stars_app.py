#mój commit HHHHHH
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Optional


class Star:
    """
    Prosta klasa reprezentująca gwiazdę.
    """
    def __init__(self, name: str, distance: float, spectral_type: str):
        self.name = name
        self.distance = distance
        self.spectral_type = spectral_type

    def __str__(self):
        return f"{self.name} | {self.distance:.2f} ly | {self.spectral_type}"


def merge_sort(stars_list: List[Star]) -> List[Star]:
    """
    Własna implementacja merge sort.
    Sortujemy obiekty Star rosnąco według pola distance.
    Zwracamy nową, posortowaną listę.
    """
    if len(stars_list) <= 1:
        return stars_list

    mid = len(stars_list) // 2
    left_half = merge_sort(stars_list[:mid])
    right_half = merge_sort(stars_list[mid:])

    return merge(left_half, right_half)

def merge(left: List[Star], right: List[Star]) -> List[Star]:
    """
    Funkcja scalająca dwie listy posortowane rosnąco według distance.
    """
    merged = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i].distance <= right[j].distance:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Dołączamy pozostałe elementy (jeśli któreś listy nie przerobiliśmy w całości)
    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged

def binary_search_by_name(stars_list: List[Star], target_name: str) -> Optional[int]:
    """
    Własna implementacja wyszukiwania binarnego po *nazwie*.
    Ale żeby to miało sens, musimy mieć listę posortowaną również po nazwie
    (lub posortować tymczasowo przed wyszukiwaniem).
    Tutaj jednak demonstrujemy sztucznie samo wywołanie. 
    W praktyce, jeśli chcemy wyszukiwać binarnie po nazwie,
    musimy sortować listę rosnąco po 'name', a nie po 'distance'.

    Dla demonstracji: 
    - Tworzymy tymczasową kopię listy, sortujemy ją po nazwie,
    - Następnie robimy binary search.

    Zwracamy indeks w posortowanej (po nazwie) liście albo None, jeśli brak.
    """
    # Kopia i sortowanie po nazwie (rosnąco)
    sorted_by_name = sorted(stars_list, key=lambda s: s.name.lower())

    left, right = 0, len(sorted_by_name) - 1
    target_name_lower = target_name.lower()

    while left <= right:
        mid = (left + right) // 2
        mid_name = sorted_by_name[mid].name.lower()

        if mid_name == target_name_lower:
            return mid  # zwracamy indeks w liście posortowanej po nazwie
        elif mid_name < target_name_lower:
            left = mid + 1
        else:
            right = mid - 1

    return None


class StarsApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Aplikacja: Gwiazdy w Kosmosie (Tkinter)")
        self.root.geometry("700x400")
        
        # Kolekcja gwiazd (lista)
        self.stars: List[Star] = []

        # Sekcja wejściowa (dodawanie gwiazdy)
        self.input_frame = tk.LabelFrame(self.root, text="Dodaj / Wyszukaj gwiazdę")
        self.input_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(self.input_frame, text="Nazwa:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = tk.Entry(self.input_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Odległość (ly):").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.distance_entry = tk.Entry(self.input_frame, width=10)
        self.distance_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.input_frame, text="Typ widmowy:").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.spectral_type_entry = tk.Entry(self.input_frame, width=10)
        self.spectral_type_entry.grid(row=0, column=5, padx=5, pady=5)

        self.add_button = tk.Button(self.input_frame, text="Dodaj gwiazdę", command=self.add_star)
        self.add_button.grid(row=0, column=6, padx=5, pady=5)

        # Przyciski do operacji
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(fill="x", padx=5, pady=5)

        self.load_button = tk.Button(self.buttons_frame, text="Wczytaj z pliku", command=self.load_from_file)
        self.load_button.pack(side="left", padx=5)

        self.search_button = tk.Button(self.buttons_frame, text="Szukaj (częściowe)", command=self.search_stars_partial)
        self.search_button.pack(side="left", padx=5)

        self.search_exact_button = tk.Button(self.buttons_frame, text="Szukaj (dokładne, binarne)", command=self.search_star_exact)
        self.search_exact_button.pack(side="left", padx=5)

        self.remove_button = tk.Button(self.buttons_frame, text="Usuń wybraną", command=self.remove_selected)
        self.remove_button.pack(side="left", padx=5)

        self.refresh_button = tk.Button(self.buttons_frame, text="Odśwież listę", command=self.refresh_list)
        self.refresh_button.pack(side="left", padx=5)

        # Lista gwiazd (Listbox + Scrollbar)
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.star_listbox = tk.Listbox(self.list_frame, height=10)
        self.star_listbox.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.star_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.star_listbox.yview)

    def add_star(self):
        """
        Dodawanie gwiazdy z pól tekstowych do listy self.stars.
        Walidacja danych (odległość jako float).
        """
        name = self.name_entry.get().strip()
        distance_str = self.distance_entry.get().strip()
        spectral_type = self.spectral_type_entry.get().strip()

        # Walidacja pola "nazwa"
        if not name:
            messagebox.showerror("Błąd", "Nazwa gwiazdy nie może być pusta.")
            return

        # Walidacja pola "distance"
        try:
            distance = float(distance_str)
        except ValueError:
            messagebox.showerror("Błąd", "Odległość musi być liczbą (float).")
            return

        if distance < 0:
            messagebox.showerror("Błąd", "Odległość nie może być ujemna.")
            return

        # Jeśli nie ma błędów – tworzymy obiekt Star
        star = Star(name, distance, spectral_type)
        self.stars.append(star)

        # Sortujemy listę po odległości (własny merge sort)
        self.stars = merge_sort(self.stars)

        # Czyścimy pola wpisu i odświeżamy Listbox
        self.name_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.spectral_type_entry.delete(0, tk.END)

        self.refresh_list()

    def remove_selected(self):
        """
        Usuwa wybraną gwiazdę (po indeksie w Listboxie) z listy self.stars.
        """
        selection = self.star_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Najpierw wybierz gwiazdę z listy.")
            return

        index = selection[0]
        # W star_listbox mamy listę wyświetleniową, ale musimy usunąć 
        # z self.stars odpowiedni obiekt. Zakładamy, że jest 1:1 w kolejności.
        star_to_remove = self.stars[index]

        # Potwierdzenie od użytkownika
        answer = messagebox.askyesno("Potwierdzenie usunięcia",
                                     f"Czy na pewno chcesz usunąć gwiazdę?\n\n{star_to_remove}")
        if answer:
            self.stars.pop(index)
            self.refresh_list()

    def refresh_list(self):
        """
        Odświeża zawartość Listboxa – wyświetla aktualną listę gwiazd w kolejności od najbliższej do najdalszej.
        """
        # Najpierw sortujemy (dla pewności, jeśli lista się zmieniła)
        self.stars = merge_sort(self.stars)

        self.star_listbox.delete(0, tk.END)
        for star in self.stars:
            self.star_listbox.insert(tk.END, str(star))

    def load_from_file(self):
        """
        Odczyt z pliku .txt o formacie:
        nazwa;odleglosc;typ
        """
        filepath = filedialog.askopenfilename(
            title="Wybierz plik z gwiazdami",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for line in lines:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(";")
                if len(parts) != 3:
                    continue  # pomijamy niepoprawny format

                name, dist_str, spectral = parts
                name = name.strip()
                spectral = spectral.strip()

                # Próbujemy konwertować odległość
                try:
                    distance = float(dist_str)
                except ValueError:
                    continue  # pomijamy jeśli nie da się przekonwertować

                star = Star(name, distance, spectral)
                self.stars.append(star)

            # Sortujemy i odświeżamy
            self.stars = merge_sort(self.stars)
            self.refresh_list()
            messagebox.showinfo("Sukces", f"Wczytano dane z pliku: {filepath}")

        except FileNotFoundError:
            messagebox.showerror("Błąd", f"Nie znaleziono pliku: {filepath}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać pliku.\n{str(e)}")

    def search_stars_partial(self):
        """
        Wyszukiwanie cząstkowe – jeśli nazwa wpisana przez użytkownika
        pojawia się w polu self.name_entry, to wyświetlamy pasujące gwiazdy.
        """
        query = self.name_entry.get().strip().lower()
        if not query:
            messagebox.showerror("Błąd", "Podaj fragment nazwy gwiazdy do wyszukania.")
            return

        matching_stars = []
        for star in self.stars:
            if query in star.name.lower():
                matching_stars.append(star)

        if not matching_stars:
            messagebox.showinfo("Wynik wyszukiwania", "Nie znaleziono gwiazd pasujących do wzorca.")
            return

        # Wyświetlamy wyniki wyszukiwania w nowym oknie (lub można zastąpić listę główną)
        result_window = tk.Toplevel(self.root)
        result_window.title("Wyniki wyszukiwania (częściowe)")

        listbox = tk.Listbox(result_window, width=60, height=10)
        listbox.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(result_window, orient="vertical")
        scroll.pack(side="right", fill="y")

        listbox.config(yscrollcommand=scroll.set)
        scroll.config(command=listbox.yview)

        for star in matching_stars:
            listbox.insert(tk.END, str(star))

    def search_star_exact(self):
        """
        Szukanie dokładne po nazwie gwiazdy, z użyciem binary_search_by_name (implementacja własna).
        Tu jednak musimy pamiętać, że binary search zadziała na liście
        posortowanej alfabetycznie (po nazwie), a nie po odległości.
        Demonstracja – jeśli znajdziemy gwiazdę, pokazujemy jej dane.
        """
        target_name = self.name_entry.get().strip()
        if not target_name:
            messagebox.showerror("Błąd", "Podaj dokładną nazwę gwiazdy do wyszukania.")
            return

        # Uruchamiamy binary search
        index_in_sorted_list = binary_search_by_name(self.stars, target_name)
        if index_in_sorted_list is None:
            messagebox.showinfo("Wynik wyszukiwania", f"Gwiazda '{target_name}' nie została znaleziona (binarne).")
        else:
            # Musimy wyciągnąć obiekt z listy posortowanej po nazwie, 
            # bo binary_search_by_name taką tworzy. Spróbujmy to odtworzyć:
            sorted_by_name = sorted(self.stars, key=lambda s: s.name.lower())
            found_star = sorted_by_name[index_in_sorted_list]

            messagebox.showinfo("Wynik wyszukiwania",
                                f"Znaleziono gwiazdę o nazwie: {found_star.name}\n"
                                f"Odległość: {found_star.distance} ly\n"
                                f"Typ widmowy: {found_star.spectral_type}")



def main():
    root = tk.Tk()
    app = StarsApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
