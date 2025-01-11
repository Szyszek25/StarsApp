# app_gui.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinter.font as tkFont

# Importujemy nasz backend z logic.py
from logic import Star, merge_sort, binary_search_by_name, load_stars_from_file

class StarsApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Kolekcja gwiazd w pamięci
        self.stars = []

        # Konfiguracja stylu
        self.configure_style()

        # Duża czcionka (opcjonalnie)
        self.big_font = tkFont.Font(family="Arial", size=16, weight="bold")

        # Baner
        banner_frame = ttk.Frame(self, style="Banner.TFrame")
        banner_frame.pack(fill="x")

        banner_label = ttk.Label(
            banner_frame,
            text="Aplikacja: Gwiazdy w Kosmosie",
            style="Banner.TLabel",
            anchor="center"
        )
        banner_label.pack(fill="x", padx=10, pady=10)

        # Sekcja formularza
        form_frame = ttk.LabelFrame(self, text="Dodaj / Wyszukaj gwiazdę", style="My.TLabelframe")
        form_frame.pack(fill="x", padx=10, pady=5)

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

        load_file_button = ttk.Button(buttons_frame, text="Wczytaj z pliku", style="My.TButton", command=self.load_from_file)
        load_file_button.pack(side="left", padx=5)

        search_partial_button = ttk.Button(buttons_frame, text="Szukaj (częściowe)", style="My.TButton", command=self.search_stars_partial)
        search_partial_button.pack(side="left", padx=5)

        search_exact_button = ttk.Button(buttons_frame, text="Szukaj (dokładne, binarne)", style="My.TButton", command=self.search_star_exact)
        search_exact_button.pack(side="left", padx=5)

        remove_button = ttk.Button(buttons_frame, text="Usuń wybraną", style="My.TButton", command=self.remove_selected)
        remove_button.pack(side="left", padx=5)

        refresh_button = ttk.Button(buttons_frame, text="Odśwież listę", style="My.TButton", command=self.refresh_list)
        refresh_button.pack(side="left", padx=5)

        # Lista gwiazd
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.star_listbox = tk.Listbox(list_frame, height=10)
        self.star_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.star_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.star_listbox.config(yscrollcommand=self.scrollbar.set)

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Banner.TFrame", background="#305080")
        style.configure("Banner.TLabel", background="#305080", foreground="white", font=("Arial", 18, "bold"))
        style.configure("My.TLabelframe", background="#F0F0F0", padding=10)
        style.configure("My.TLabel", background="#F0F0F0", foreground="#333333", font=("Arial", 10))
        style.configure("My.TButton", font=("Arial", 10, "bold"), padding=5)

    def add_star(self):
        """Dodaj nową gwiazdę na podstawie wpisanych danych."""
        name = self.name_entry.get().strip()
        distance_str = self.distance_entry.get().strip()
        spectral_type = self.spectral_type_entry.get().strip()

        if not name:
            messagebox.showerror("Błąd", "Nazwa gwiazdy nie może być pusta.")
            return
        try:
            distance = float(distance_str)
            if distance < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Błąd", "Odległość musi być liczbą nieujemną.")
            return

        star = Star(name, distance, spectral_type)
        self.stars.append(star)

        # Sortujemy gwiazdy po każdej zmianie (merge_sort z logic.py)
        self.stars = merge_sort(self.stars)
        self.refresh_list()

        # Czyszczenie pól
        self.name_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.spectral_type_entry.delete(0, tk.END)

    def remove_selected(self):
        """Usuń wybraną gwiazdę z listy."""
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
        """Odśwież Listbox, aby wyświetlał aktualną, posortowaną listę gwiazd."""
        self.star_listbox.delete(0, tk.END)
        for star in self.stars:
            self.star_listbox.insert(tk.END, str(star))

    def load_from_file(self):
        """Obsługa wczytania danych z pliku przy pomocy funkcji z logic.py."""
        filepath = filedialog.askopenfilename(
            title="Wybierz plik .txt z gwiazdami",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
        )
        if not filepath:
            return
        try:
            # Używamy naszej funkcji z logic.py
            new_stars = load_stars_from_file(filepath)
            # Doklejamy do obecnej listy
            self.stars.extend(new_stars)
            # Sortujemy po odległości i odświeżamy widok
            self.stars = merge_sort(self.stars)
            self.refresh_list()
            messagebox.showinfo("Sukces", f"Wczytano dane z pliku: {filepath}")
        except FileNotFoundError:
            messagebox.showerror("Błąd", f"Plik '{filepath}' nie został odnaleziony.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił problem podczas wczytywania pliku:\n{e}")

    def search_stars_partial(self):
        """Wyszukiwanie cząstkowe – linearne, np. 'Siri' znajdzie 'Sirius'."""
        query = self.name_entry.get().strip().lower()
        if not query:
            messagebox.showerror("Błąd", "Podaj fragment nazwy do wyszukania.")
            return

        matching_stars = []
        for star in self.stars:
            if query in star.name.lower():
                matching_stars.append(star)

        if not matching_stars:
            messagebox.showinfo("Wynik wyszukiwania", "Nie znaleziono gwiazd pasujących do wzorca.")
            return

        # Wyświetlamy wyniki w nowym oknie:
        result_window = tk.Toplevel(self)
        result_window.title("Wyniki wyszukiwania (częściowe)")
        result_window.geometry("400x300")

        lb = tk.Listbox(result_window)
        lb.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(result_window, orient="vertical", command=lb.yview)
        sb.pack(side="right", fill="y")

        lb.config(yscrollcommand=sb.set)

        for star in matching_stars:
            lb.insert(tk.END, str(star))

    def search_star_exact(self):
        """Dokładne wyszukiwanie po nazwie (binary search z logic.py)."""
        target_name = self.name_entry.get().strip()
        if not target_name:
            messagebox.showerror("Błąd", "Podaj dokładną nazwę gwiazdy do wyszukania.")
            return

        index_in_sorted_list = binary_search_by_name(self.stars, target_name)
        if index_in_sorted_list is None:
            messagebox.showinfo("Wynik wyszukiwania", f"Gwiazda '{target_name}' nie została znaleziona.")
        else:
            # Aby pobrać obiekt, sortujemy listę po nazwie tak jak w binary_search_by_name
            sorted_by_name = sorted(self.stars, key=lambda s: s.name.lower())
            found_star = sorted_by_name[index_in_sorted_list]
            messagebox.showinfo(
                "Wynik wyszukiwania",
                f"Znaleziono gwiazdę o nazwie: {found_star.name}\n"
                f"Odległość: {found_star.distance} ly\n"
                f"Typ widmowy: {found_star.spectral_type}"
            )

def main():
    root = tk.Tk()
    root.title("Gwiazdy w Kosmosie – rozdzielony backend i frontend")
    root.geometry("800x500")
    app = StarsApp(root)
    app.mainloop()

if __name__ == "__main__":
    main()
