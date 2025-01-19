# app_gui.py

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from logic import dodaj_gwiazde, wyswietl_gwiazdy, usun_gwiazde, wyszukaj_gwiazde, dodaj_z_pliku, binary_search
from PIL import Image
import os

def load_cropped_image_21x9(image_path: str, target_width=1280):
    """Ładuje obraz z image_path i kadruje go do proporcji 21:9."""
    target_height = int(target_width * (9 / 50))  # zachowujemy oryginalne proporcje
    img = Image.open(image_path)
    orig_w, orig_h = img.size
    img_ratio = orig_w / orig_h

    if img_ratio > (target_width / target_height):
        scale = target_height / orig_h
        new_w = int(orig_w * scale)
        new_h = target_height
    else:
        scale = target_width / orig_w
        new_w = target_width
        new_h = int(orig_h * scale)

    resized = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_width) // 2
    top = (new_h - target_height) // 2
    right = left + target_width
    bottom = top + target_height
    return resized.crop((left, top, right, bottom))


class ModernStarsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ustawienia główne
        self.title("Gwiazdy w Kosmosie – Pełny Interfejs")
        self.geometry("850x768")  # ustawiłeś idealną rozdzielczość
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Główna ramka
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # ======================== BANER GÓRNY ===========================
        banner_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        banner_frame.pack(side="top", fill="x")

        banner_path = os.path.join(os.path.dirname(__file__), "top_banner.png")
        if os.path.isfile(banner_path):
            banner_img = load_cropped_image_21x9(banner_path, target_width=1366)
            self.top_banner_image = ctk.CTkImage(
                light_image=banner_img,
                dark_image=banner_img,
                size=banner_img.size
            )
            self.top_banner_label = ctk.CTkLabel(banner_frame, text="", image=self.top_banner_image)
            self.top_banner_label.pack(fill="x")
        else:
            ctk.CTkLabel(banner_frame, text="Brak pliku top_banner.png").pack(pady=10)

        # ======================== GŁÓWNY UI ============================
        center_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        center_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # W sekcji GŁÓWNY UI, przed sekcją formularza, nagłówek:
        header_label = ctk.CTkLabel(
            center_frame,
            text="Aplikacja: Wyszukiwarka Gwiazd w Kosmosie 🌟",
            font=ctk.CTkFont(size=24, weight="bold"),
            justify="center"
        )
        header_label.pack(pady=10)


        # =================== SEKCJA FORMULARZA =======================
        # Utwórz ramkę dla pól formularza – chcemy, aby była takiej samej szerokości jak przyciski poniżej.
        self.form_frame = ctk.CTkFrame(center_frame)
        self.form_frame.pack(fill="x", padx=10, pady=10)

        # Pola formularza
        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Wpisz gwiazdę")
        self.distance_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Wpisz odległość (ly)")
        self.add_button = ctk.CTkButton(self.form_frame, text="Dodaj Gwiazdę", command=self.add_star)

        # Zapisujemy widgety formularza do listy, aby móc dynamicznie rozmieszczać
        self.form_widgets = [self.name_entry, self.distance_entry, self.add_button]

        # Bindujemy zdarzenie zmiany rozmiaru dla form_frame, aby widgety mogły się zawijać
        self.form_frame.bind("<Configure>", self.arrange_form)

        # =================== SEKCJA PRZYCISKÓW =======================
        self.button_frame = ctk.CTkFrame(center_frame)
        self.button_frame.pack(fill="x", padx=10, pady=10)

        self.load_button = ctk.CTkButton(self.button_frame, text="Wczytaj z Pliku", command=self.load_from_file)
        self.search_button = ctk.CTkButton(self.button_frame, text="Szukaj Gwiazdy", command=self.search_star)
        self.exact_search_button = ctk.CTkButton(self.button_frame, text="Szukaj Dokładnie", command=self.search_star_exact)
        self.delete_button = ctk.CTkButton(self.button_frame, text="Usuń Zaznaczoną", command=self.delete_star)
        self.refresh_button = ctk.CTkButton(self.button_frame, text="Odśwież Listę", command=self.refresh_list)

        self.buttons = [
            self.load_button,
            self.search_button,
            self.exact_search_button,
            self.delete_button,
            self.refresh_button
        ]

        self.button_frame.bind("<Configure>", self.arrange_buttons)

        # =================== SEKCJA LISTY GWIAZD =======================
        list_frame = ctk.CTkFrame(center_frame, corner_radius=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.star_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, height=15)
        self.star_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.star_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.star_listbox.config(yscrollcommand=self.scrollbar.set)

    # Metoda do dynamicznego rozmieszczania widgetów formularza
    def arrange_form(self, event):
        available_width = event.width
        # Ustalamy minimalną szerokość widgetu - można dostosować tę wartość
        min_widget_width = 200  
        padding = 10
        columns = max(1, available_width // (min_widget_width + padding))

        # Usuń poprzednie rozmieszczenie widgetów
        for widget in self.form_widgets:
            widget.grid_forget()

        # Rozmieść widgety na podstawie obliczonej liczby kolumn
        for index, widget in enumerate(self.form_widgets):
            row = index // columns
            col = index % columns
            widget.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        # Ustaw konfigurację kolumn w ramce
        for col in range(columns):
            self.form_frame.grid_columnconfigure(col, weight=1)

    # Metoda do dynamicznego rozmieszczania przycisków
    def arrange_buttons(self, event):
        available_width = event.width
        min_button_width = 150
        padding = 10
        columns = max(1, available_width // (min_button_width + padding))

        for btn in self.buttons:
            btn.grid_forget()

        for index, btn in enumerate(self.buttons):
            row = index // columns
            col = index % columns
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="w")

        for col in range(columns):
            self.button_frame.grid_columnconfigure(col, weight=1)

    # ====================== FUNKCJE LOGICZNE ==========================
    def add_star(self):
        nazwa = self.name_entry.get().strip()
        odleglosc = self.distance_entry.get().strip()

        if not nazwa or not odleglosc:
            tk.messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione.")
            return

        try:
            odleglosc = float(odleglosc)
            dodaj_gwiazde(nazwa, odleglosc)
            self.refresh_list()
            self.name_entry.delete(0, tk.END)
            self.distance_entry.delete(0, tk.END)
        except ValueError:
            tk.messagebox.showerror("Błąd", "Odległość musi być liczbą.")

    def refresh_list(self):
        self.star_listbox.delete(0, tk.END)
        lista_gwiazd = wyswietl_gwiazdy()
        if lista_gwiazd:
            for idx, gwiazda in enumerate(lista_gwiazd, start=1):
                self.star_listbox.insert(tk.END, f"{idx}. {gwiazda}")

    def delete_star(self):
        selection = self.star_listbox.curselection()
        if not selection:
            tk.messagebox.showinfo("Info", "Wybierz gwiazdę do usunięcia.")
            return

        index = selection[0]
        usun_gwiazde(index)
        self.refresh_list()

    def load_from_file(self):
        filepath = tk.filedialog.askopenfilename(
            title="Wybierz plik",
            filetypes=[("Pliki tekstowe", "*.txt")]
        )
        if filepath:
            try:
                dodane = dodaj_z_pliku(filepath)
                self.refresh_list()
                tk.messagebox.showinfo("Wczytywanie z pliku", f"Dodano gwiazdy: {dodane}")
            except Exception as e:
                tk.messagebox.showerror("Błąd", f"Nie udało się dodać gwiazd\n{e}")

    def search_star(self):
        query = tk.simpledialog.askstring("Szukaj Gwiazdy", "Podaj fragment nazwy gwiazdy:")
        if query:
            wyniki = wyszukaj_gwiazde(query)
            if wyniki:
                result_text = "\n".join(str(wynik) for wynik in wyniki)
                tk.messagebox.showinfo("Wyniki Wyszukiwania", result_text)
            else:
                tk.messagebox.showinfo("Brak wyników", "Nie znaleziono gwiazd.")

    def search_star_exact(self):
        query = tk.simpledialog.askstring("Szukaj Dokładnie", "Podaj **dokładną** nazwę gwiazdy:")
        if query:
            lista_gwiazd = wyswietl_gwiazdy()  # lista jest sortowana przez merge_sort
            index = binary_search(lista_gwiazd, query)
            if index != -1:
                tk.messagebox.showinfo("Wynik Wyszukiwania", f"Znaleziono: {lista_gwiazd[index]}")
                self.star_listbox.selection_clear(0, tk.END)
                self.star_listbox.selection_set(index)
                self.star_listbox.activate(index)
            else:
                tk.messagebox.showinfo("Brak wyników", "Nie znaleziono gwiazdy o podanej nazwie.")


if __name__ == "__main__":
    app = ModernStarsApp()
    app.mainloop()
