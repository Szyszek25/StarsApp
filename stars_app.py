
#JohnSalam

#mój commit HHHHHH
#commit 
#updaet
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional

# ========================
#   Klasa i funkcje logiki
# ========================

class Star:
    def __init__(self, name: str, distance: float, spectral_type: str):
        self.name = name
        self.distance = distance
        self.spectral_type = spectral_type

    def __str__(self):
        return f"{self.name} | {self.distance:.2f} ly | {self.spectral_type}"


def merge_sort(stars_list: List[Star]) -> List[Star]:
    if len(stars_list) <= 1:
        return stars_list
    mid = len(stars_list) // 2
    left_half = merge_sort(stars_list[:mid])
    right_half = merge_sort(stars_list[mid:])
    return merge(left_half, right_half)

def merge(left: List[Star], right: List[Star]) -> List[Star]:
    merged = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i].distance <= right[j].distance:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def binary_search_by_name(stars_list: List[Star], target_name: str) -> Optional[int]:
    # Kopia i sortowanie po nazwie (rosnąco)
    sorted_by_name = sorted(stars_list, key=lambda s: s.name.lower())
    left, right = 0, len(sorted_by_name) - 1
    target_name_lower = target_name.lower()

    while left <= right:
        mid = (left + right) // 2
        mid_name = sorted_by_name[mid].name.lower()
        if mid_name == target_name_lower:
            return mid
        elif mid_name < target_name_lower:
            left = mid + 1
        else:
            right = mid - 1
    return None

# ========================
#    Klasa głównej aplikacji
# ========================

class StarsApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Lista gwiazd
        self.stars: List[Star] = []

        # Konfiguracja stylu
        self.configure_style()

        # Możemy ustawić tło ramki (jeśli używamy klasycznej tk.Frame),
        # ale przy ttk.Frame stylujemy przez Style
        self.pack(fill="both", expand=True)

        # Czcionki (przykład)
        self.big_font = tkFont.Font(family="Arial", size=16, weight="bold")
        self.normal_font = tkFont.Font(family="Arial", size=10)
        self.small_font = tkFont.Font(family="Arial", size=9, slant="italic")

        # Nagłówek / baner
        banner_frame = ttk.Frame(self, style="Banner.TFrame")
        banner_frame.pack(fill="x")

        banner_label = ttk.Label(
            banner_frame,
            text="Aplikacja: Gwiazdy w Kosmosie",
            style="Banner.TLabel",
            anchor="center"
        )
        banner_label.pack(fill="x", padx=10, pady=10)

        # Sekcja "Formularza" do dodawania i wyszukiwania
        form_frame = ttk.LabelFrame(self, text="Dodaj / Wyszukaj gwiazdę", style="My.TLabelframe")
        form_frame.pack(fill="x", padx=10, pady=5)

        # Etykiety i pola
        ttk.Label(form_frame, text="Nazwa:", style="My.TLabel").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.name_entry = ttk.Entry(form_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Odległość (ly):", style="My.TLabel").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.distance_entry = ttk.Entry(form_frame, width=10)
        self.distance_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Typ widmowy:", style="My.TLabel").grid(row=0, column=4, padx=5, pady=5, sticky="e")
        self.spectral_type_entry = ttk.Entry(form_frame, width=10)
        self.spectral_type_entry.grid(row=0, column=5, padx=5, pady=5)

        add_button = ttk.Button(form_frame, text="Dodaj gwiazdę", style="My.TButton", command=self.add_star)
        add_button.grid(row=0, column=6, padx=5, pady=5)

        # Ramka przycisków
        buttons_frame = ttk.Frame(self)
        buttons_frame.pack(fill="x", padx=10, pady=5)

        self.load_button = ttk.Button(buttons_frame, text="Wczytaj z pliku", style="My.TButton", command=self.load_from_file)
        self.load_button.pack(side="left", padx=5)

        self.search_button = ttk.Button(buttons_frame, text="Szukaj (częściowe)", style="My.TButton", command=self.search_stars_partial)
        self.search_button.pack(side="left", padx=5)

        self.search_exact_button = ttk.Button(buttons_frame, text="Szukaj (dokładne, binarne)", style="My.TButton", command=self.search_star_exact)
        self.search_exact_button.pack(side="left", padx=5)

        self.remove_button = ttk.Button(buttons_frame, text="Usuń wybraną", style="My.TButton", command=self.remove_selected)
        self.remove_button.pack(side="left", padx=5)

        self.refresh_button = ttk.Button(buttons_frame, text="Odśwież listę", style="My.TButton", command=self.refresh_list)
        self.refresh_button.pack(side="left", padx=5)

        # Lista gwiazd
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.star_listbox = tk.Listbox(list_frame, height=10, font=self.normal_font)
        self.star_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.star_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.star_listbox.config(yscrollcommand=self.scrollbar.set)

    # ======== Metody funkcjonalności ========

    def configure_style(self):
        """
        Konfiguracja motywu i stylów dla widżetów ttk.
        """
        style = ttk.Style()

        # Sprawdzamy dostępne motywy
        # print(style.theme_names())
        # Zmień na inny, np. "clam", "alt", "default", "classic"
        style.theme_use("clam")

        # Ramka banera
        style.configure("Banner.TFrame", background="#305080")
        style.configure("Banner.TLabel", background="#305080", foreground="white", font=("Arial", 18, "bold"))

        # LabelFrame
        style.configure("My.TLabelframe", background="#F0F0F0", font=("Arial", 11, "bold"), padding=10)

        # Label
        style.configure("My.TLabel", background="#F0F0F0", foreground="#333333", font=("Arial", 10))

        # Button
        style.configure("My.TButton", font=("Arial", 10, "bold"), foreground="#222222", padding=5)

        # Możemy też zmieniać style interaktywne (np. hover), ale to wymaga bardziej
        # zaawansowanej konfiguracji, np. z mapowaniem:
        # style.map("My.TButton",
        #           foreground=[('active', 'blue')],
        #           background=[('active', '#DDDDDD')])

    def add_star(self):
        name = self.name_entry.get().strip()
        distance_str = self.distance_entry.get().strip()
        spectral_type = self.spectral_type_entry.get().strip()

        if not name:
            messagebox.showerror("Błąd", "Nazwa gwiazdy nie może być pusta.")
            return
        try:
            distance = float(distance_str)
            if distance < 0:
                raise ValueError("Odległość nie może być ujemna.")
        except ValueError:
            messagebox.showerror("Błąd", "Odległość musi być liczbą nieujemną (float).")
            return

        star = Star(name, distance, spectral_type)
        self.stars.append(star)

        self.stars = merge_sort(self.stars)
        self.clear_entries()
        self.refresh_list()

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.spectral_type_entry.delete(0, tk.END)

    def remove_selected(self):
        selection = self.star_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Najpierw wybierz gwiazdę z listy.")
            return
        index = selection[0]
        star_to_remove = self.stars[index]
        answer = messagebox.askyesno(
            "Potwierdzenie usunięcia",
            f"Czy na pewno chcesz usunąć gwiazdę?\n\n{star_to_remove}"
        )
        if answer:
            self.stars.pop(index)
            self.refresh_list()

    def refresh_list(self):
        self.stars = merge_sort(self.stars)
        self.star_listbox.delete(0, tk.END)
        for star in self.stars:
            self.star_listbox.insert(tk.END, str(star))

    def load_from_file(self):
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
                    continue
                name, dist_str, spectral = parts
                name = name.strip()
                spectral = spectral.strip()
                try:
                    distance = float(dist_str)
                    if distance < 0:
                        continue
                except ValueError:
                    continue
                star = Star(name, distance, spectral)
                self.stars.append(star)

            self.stars = merge_sort(self.stars)
            self.refresh_list()
            messagebox.showinfo("Sukces", f"Wczytano dane z pliku: {filepath}")

        except FileNotFoundError:
            messagebox.showerror("Błąd", f"Nie znaleziono pliku: {filepath}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać pliku.\n{str(e)}")

    def search_stars_partial(self):
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

        result_window = tk.Toplevel(self)
        result_window.title("Wyniki wyszukiwania (częściowe)")
        result_window.geometry("400x300")

        # Używamy także stylu w tym oknie
        result_frame = ttk.Frame(result_window)
        result_frame.pack(fill="both", expand=True)

        listbox = tk.Listbox(result_frame, height=10, font=self.normal_font)
        listbox.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(result_frame, orient="vertical", command=listbox.yview)
        scroll.pack(side="right", fill="y")

        listbox.config(yscrollcommand=scroll.set)
        for star in matching_stars:
            listbox.insert(tk.END, str(star))

    def search_star_exact(self):
        target_name = self.name_entry.get().strip()
        if not target_name:
            messagebox.showerror("Błąd", "Podaj dokładną nazwę gwiazdy do wyszukania.")
            return
        index_in_sorted_list = binary_search_by_name(self.stars, target_name)
        if index_in_sorted_list is None:
            messagebox.showinfo("Wynik wyszukiwania", f"Gwiazda '{target_name}' nie została znaleziona (binarne).")
        else:
            sorted_by_name = sorted(self.stars, key=lambda s: s.name.lower())
            found_star = sorted_by_name[index_in_sorted_list]
            messagebox.showinfo(
                "Wynik wyszukiwania",
                f"Znaleziono gwiazdę o nazwie: {found_star.name}\n"
                f"Odległość: {found_star.distance} ly\n"
                f"Typ widmowy: {found_star.spectral_type}"
            )

# ==================================
#  Funkcja uruchamiająca aplikację
# ==================================

def main():
    root = tk.Tk()
    root.title("Gwiazdy w Kosmosie (upiększony Tkinter)")
    # Możemy dodać ikonę okna (jeśli mamy plik .ico):
    # root.iconbitmap("ikona.ico")

    # Ustawiamy wymiary początkowe
    root.geometry("800x500")

    # Możemy ustawić minimalny rozmiar okna
    root.minsize(600, 400)

    app = StarsApp(root)
    app.mainloop()

if __name__ == "__main__":
    main()
