# app_gui.py

import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk, filedialog, messagebox

# Importujemy nasz backend
from logic import Star, merge_sort, binary_search_by_name

class StarsApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Trzymaj tu kolekcję gwiazd (z backendu)
        self.stars = []

        self.configure_style()

        # Przyklad: Duże czcionki i styl banera
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

        # ... tu reszta kodu GUI: LabelFrame, pola Entry, przyciski, listbox itd. ...
        # Dla uproszczenia pokażemy tylko kilka metod

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

        # Listbox do wyświetlania gwiazd
        list_frame = ttk.Frame(self)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.star_listbox = tk.Listbox(list_frame, height=10)
        self.star_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.star_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.star_listbox.config(yscrollcommand=self.scrollbar.set)

        # Przykładowy przycisk do wyszukiwania binarnego
        self.search_exact_button = ttk.Button(self, text="Szukaj (dokładne)", command=self.search_star_exact)
        self.search_exact_button.pack(pady=5)

    def configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Banner.TFrame", background="#305080")
        style.configure("Banner.TLabel", background="#305080", foreground="white", font=("Arial", 18, "bold"))
        style.configure("My.TLabelframe", background="#F0F0F0", padding=10)
        style.configure("My.TLabel", background="#F0F0F0", foreground="#333333", font=("Arial", 10))
        style.configure("My.TButton", font=("Arial", 10, "bold"), padding=5)

    def add_star(self):
        """
        Przykładowa metoda dodawania gwiazdy przy użyciu logiki z backendu.
        """
        from logic import Star, merge_sort  # można importować globalnie lub tutaj
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
        self.stars = merge_sort(self.stars)
        self.refresh_list()

    def refresh_list(self):
        self.star_listbox.delete(0, tk.END)
        for star in self.stars:
            self.star_listbox.insert(tk.END, str(star))

    def search_star_exact(self):
        from logic import binary_search_by_name
        target_name = self.name_entry.get().strip()
        if not target_name:
            messagebox.showerror("Błąd", "Podaj nazwę gwiazdy do wyszukania.")
            return
        index_in_sorted_list = binary_search_by_name(self.stars, target_name)
        if index_in_sorted_list is None:
            messagebox.showinfo("Wynik wyszukiwania", f"Nie znaleziono gwiazdy '{target_name}'.")
        else:
            # ... wyświetl info ...
            messagebox.showinfo("Znaleziono", f"Gwiazda '{target_name}' występuje w zbiorze.")

def main():
    root = tk.Tk()
    root.title("Gwiazdy w Kosmosie (rozdzielony backend/frontend)")
    root.geometry("800x500")
    app = StarsApp(root)
    app.mainloop()

if __name__ == "__main__":
    main()
