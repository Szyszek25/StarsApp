import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from logic import dodaj_gwiazde, wyswietl_gwiazdy, usun_gwiazde, wyszukaj_gwiazde, dodaj_z_pliku
from PIL import Image
import os


def load_image_21x9_cover(image_path: str, target_width=1280):
    """Ładuje obraz z image_path i kadruje go do proporcji 21:9."""
    target_height = int(target_width * (9 / 50))
    img = Image.open(image_path)
    orig_w, orig_h = img.size
    img_ratio = orig_w / orig_h

    # Oblicz skalowanie i rozmiar docelowy
    if img_ratio > (target_width / target_height):
        scale = target_height / orig_h
        new_w = int(orig_w * scale)
        new_h = target_heigh
    else:
        scale = target_width / orig_w
        new_w = target_width
        new_h = int(orig_h * scale)

    # Zmień rozmiar i przytnij do środka
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
        self.geometry("768x768")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Lista gwiazd
        self.stars = []

        # Główna ramka
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # ======================== BANER GÓRNY ===========================
        banner_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        banner_frame.pack(side="top", fill="x")

        banner_path = os.path.join(os.path.dirname(__file__), "top_banner.png")
        if os.path.isfile(banner_path):
            banner_img = load_image_21x9_cover(banner_path, target_width=1366)
            self.top_banner_image = ctk.CTkImage(
                light_image=banner_img,
                dark_image=banner_img,
                size=banner_img.size
            )
            self.top_banner_label = ctk.CTkLabel(
                banner_frame,
                text="",
                image=self.top_banner_image
            )
            self.top_banner_label.pack(fill="x")
        else:
            ctk.CTkLabel(banner_frame, text="Brak pliku top_banner.png").pack(pady=10)

        # ======================== GŁÓWNY UI ============================
        center_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        center_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Nagłówek
        header_label = ctk.CTkLabel(
            center_frame,
            text="Aplikacja: Wyszukiwarka Gwiazd w Kosmosie 🌟",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header_label.pack(pady=10)

        # Sekcja formularza
        form_frame = ctk.CTkFrame(center_frame)
        form_frame.pack(fill="x", padx=10, pady=10)

        self.name_entry = ctk.CTkEntry(form_frame, placeholder_text="Nazwa gwiazdy")
        self.name_entry.grid(row=0, column=0, padx=10, pady=5)

        self.distance_entry = ctk.CTkEntry(form_frame, placeholder_text="Odległość (ly)")
        self.distance_entry.grid(row=0, column=1, padx=10, pady=5)

        self.add_button = ctk.CTkButton(form_frame, text="Dodaj Gwiazdę", command=self.add_star)
        self.add_button.grid(row=0, column=2, padx=10, pady=5)

        # Sekcja przycisków
        button_frame = ctk.CTkFrame(center_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        self.load_button = ctk.CTkButton(button_frame, text="Wczytaj z Pliku", command=self.load_from_file)
        self.load_button.pack(side="left", padx=10)

        self.search_button = ctk.CTkButton(button_frame, text="Szukaj Gwiazdy", command=self.search_star)
        self.search_button.pack(side="left", padx=10)

        self.delete_button = ctk.CTkButton(button_frame, text="Usuń Zaznaczoną", command=self.delete_star)
        self.delete_button.pack(side="left", padx=10)

        self.refresh_button = ctk.CTkButton(button_frame, text="Odśwież Listę", command=self.refresh_list)
        self.refresh_button.pack(side="left", padx=10)

        # Sekcja listy gwiazd
        list_frame = ctk.CTkFrame(center_frame, corner_radius=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.star_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, height=15)
        self.star_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.star_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.star_listbox.config(yscrollcommand=self.scrollbar.set)

    # ====================== FUNKCJE LOGICZNE ==========================
    def add_star(self):
        nazwa = self.name_entry.get().strip()
        odleglosc = self.distance_entry.get().strip()

        if not nazwa or not odleglosc:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione.")
            return

        try:
            odleglosc = float(odleglosc)
            dodaj_gwiazde(nazwa, odleglosc)
            self.refresh_list()
            self.name_entry.delete(0, tk.END)
            self.distance_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Błąd", "Odległość musi być liczbą.")

    def refresh_list(self):
        self.star_listbox.delete(0, tk.END)
        for gwiazda in wyswietl_gwiazdy():
            self.star_listbox.insert(tk.END, gwiazda)

    def delete_star(self):
        selection = self.star_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Wybierz gwiazdę do usunięcia.")
            return

        index = selection[0] + 1
        usun_gwiazde(index)
        self.refresh_list()
    #not working
    def load_from_file(self):
        filepath = filedialog.askopenfilename(
            title="Wybierz plik",
            filetypes=[("Pliki tekstowe", "*.txt")]
        )
        if filepath:
            dodaj_z_pliku(filepath)
            self.refresh_list()

    def search_star(self):
        query = simpledialog.askstring("Szukaj Gwiazdy", "Podaj fragment nazwy gwiazdy:")
        if query:
            wyniki = wyszukaj_gwiazde(query)
            if wyniki:
                result_text = "\n".join(str(wynik) for wynik in wyniki)
                messagebox.showinfo("Wyniki Wyszukiwania", result_text)
            else:
                messagebox.showinfo("Brak wyników", "Nie znaleziono gwiazd.")


if __name__ == "__main__":
    app = ModernStarsApp()
    app.mainloop()
