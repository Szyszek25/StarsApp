import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List
import os
from PIL import Image

# Import backend
from logic import (
    Star,
    merge_sort,
    binary_search_by_name,
    load_stars_from_file,
    save_stars_to_file
)

def load_image_21x9_cover(image_path: str, target_width=1280):
    """
    Ładuje obraz z image_path, kadruje w proporcji 21:9 w stylu "cover" i zwraca obiekt PIL.Image.
    """
    target_height = int(target_width * (9/50))
    img = Image.open(image_path)
    orig_w, orig_h = img.size
    img_ratio = orig_w / orig_h
    desired_w = target_width
    desired_h = target_height

    if img_ratio > (desired_w / desired_h):
        scale = desired_h / orig_h
        new_w = int(orig_w * scale)
        new_h = desired_h
    else:
        scale = desired_w / orig_w
        new_w = desired_w
        new_h = int(orig_h * scale)

    resized = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - desired_w) // 2
    top = (new_h - desired_h) // 2
    right = left + desired_w
    bottom = top + desired_h
    cropped = resized.crop((left, top, right, bottom))
    return cropped

class ModernStarsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ustawienia stylu
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Rozmiar okna (16:9)
        self.title("Gwiazdy w Kosmosie – baner u góry 21:9")
        self.geometry("768x768")

        # Lista gwiazd
        self.stars: List[Star] = []

        # Ścieżka do pliku
        self.current_file_path: str | None = None

        # ============ Główny kontener ============
        self.container_frame = ctk.CTkFrame(self, corner_radius=0)
        self.container_frame.pack(fill="both", expand=True)

        # ============ BANER GÓRNY ============
        banner_frame = ctk.CTkFrame(self.container_frame, corner_radius=0)
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
            lbl = ctk.CTkLabel(banner_frame, text="Brak top_banner.png")
            lbl.pack()

        # ============ Centrum (UI) ============
        self.center_frame = ctk.CTkFrame(self.container_frame, corner_radius=10)
        self.center_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Nagłówek
        self.header_label = ctk.CTkLabel(
            self.center_frame, 
            text="Aplikacja: Wyszukiwarka gwiazd w kosmosie ✨",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.header_label.pack(pady=10)

        # Sekcja formularza
        self.form_frame = ctk.CTkFrame(self.center_frame)
        self.form_frame.pack(fill="x", padx=10, pady=5)

        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Nazwa gwiazdy")
        self.name_entry.grid(row=0, column=0, padx=10, pady=5)

        self.distance_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Odległość (ly)")
        self.distance_entry.grid(row=0, column=1, padx=10, pady=5)

        self.spectral_type_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Typ widmowy (np. G2V)")
        self.spectral_type_entry.grid(row=0, column=2, padx=10, pady=5)

        self.add_button = ctk.CTkButton(self.form_frame, text="Dodaj gwiazdę", command=self.add_star)
        self.add_button.grid(row=0, column=3, padx=10, pady=5)

        # Ramka przycisków
        self.buttons_frame = ctk.CTkFrame(self.center_frame)
        self.buttons_frame.pack(fill="x", padx=10, pady=5)

        self.load_button = ctk.CTkButton(self.buttons_frame, text="Wczytaj z pliku", command=self.load_from_file)
        self.load_button.pack(side="left", padx=5)

        self.search_partial_button = ctk.CTkButton(self.buttons_frame, text="Szukaj (częściowe)", command=self.search_stars_partial)
        self.search_partial_button.pack(side="left", padx=5)

        self.search_exact_button = ctk.CTkButton(self.buttons_frame, text="Szukaj (dokładne, binarne)", command=self.search_star_exact)
        self.search_exact_button.pack(side="left", padx=5)

        self.remove_by_name_button = ctk.CTkButton(self.buttons_frame, text="Usuń po nazwie", command=self.remove_by_name)
        self.remove_by_name_button.pack(side="left", padx=5)

        self.remove_selected_button = ctk.CTkButton(self.buttons_frame, text="Usuń zaznaczoną", command=self.remove_selected_star)
        self.remove_selected_button.pack(side="left", padx=5)

        self.refresh_button = ctk.CTkButton(self.buttons_frame, text="Odśwież listę", command=self.refresh_list)
        self.refresh_button.pack(side="left", padx=5)

        # Lista gwiazd
        self.list_frame = ctk.CTkFrame(self.center_frame)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.star_listbox = tk.Listbox(self.list_frame, height=12, selectmode=tk.SINGLE)
        self.star_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.star_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.star_listbox.config(yscrollcommand=self.scrollbar.set)

    # =========================== FUNKCJE LOGICZNE ===========================

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
                raise ValueError
        except ValueError:
            messagebox.showerror("Błąd", "Odległość musi być liczbą nieujemną (float).")
            return

        new_star = Star(name, distance, spectral_type)
        self.stars.append(new_star)
        self.stars = merge_sort(self.stars)
        self.clear_form_fields()
        self.refresh_list()
        self.save_current_file()

    def clear_form_fields(self):
        self.name_entry.delete(0, "end")
        self.distance_entry.delete(0, "end")
        self.spectral_type_entry.delete(0, "end")

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
            loaded_stars = load_stars_from_file(filepath)
            self.stars = merge_sort(loaded_stars)
            self.current_file_path = filepath
            self.refresh_list()
            messagebox.showinfo("Sukces", f"Wczytano dane z pliku: {filepath}")
        except FileNotFoundError:
            messagebox.showerror("Błąd", f"Plik '{filepath}' nie został odnaleziony.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wczytać pliku.\n{e}")

    def remove_by_name(self):
        import tkinter.simpledialog as sd
        target_name = sd.askstring("Usuń gwiazdę po nazwie", "Podaj dokładną nazwę gwiazdy do usunięcia:")
        if not target_name:
            return

        found_star = None
        for star in self.stars:
            if star.name.lower() == target_name.lower():
                found_star = star
                break

        if not found_star:
            messagebox.showinfo("Info", f"Nie znaleziono gwiazdy o nazwie '{target_name}'.")
            return

        ans = messagebox.askyesno("Potwierdzenie usunięcia", f"Czy na pewno usunąć: {found_star}?")
        if ans:
            self.stars.remove(found_star)
            self.refresh_list()
            self.save_current_file()

    def remove_selected_star(self):
        selection = self.star_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Najpierw wybierz gwiazdę z listy (klikając).")
            return

        index = selection[0]
        star_to_remove = self.stars[index]

        ans = messagebox.askyesno("Potwierdzenie usunięcia", f"Czy na pewno usunąć: {star_to_remove}?")
        if ans:
            self.stars.pop(index)
            self.refresh_list()
            self.save_current_file()

    def search_stars_partial(self):
        import tkinter.simpledialog as sd
        query = sd.askstring("Wyszukiwanie częściowe", "Podaj fragment nazwy gwiazdy:")
        if not query:
            return
        query_lower = query.lower()

        matching = [s for s in self.stars if query_lower in s.name.lower()]
        if not matching:
            messagebox.showinfo("Wynik", "Nie znaleziono gwiazd pasujących do wzorca.")
            return

        results_win = ctk.CTkToplevel(self)
        results_win.title("Wyniki wyszukiwania (częściowe)")
        results_win.geometry("400x300")

        info_label = ctk.CTkLabel(results_win, text=f"Znaleziono {len(matching)} gwiazd:")
        info_label.pack(pady=10)

        lb = tk.Listbox(results_win)
        lb.pack(side="left", fill="both", expand=True)

        sb = tk.Scrollbar(results_win, orient="vertical", command=lb.yview)
        sb.pack(side="right", fill="y")

        lb.config(yscrollcommand=sb.set)

        for star in matching:
            lb.insert(tk.END, str(star))

    def search_star_exact(self):
        import tkinter.simpledialog as sd
        target_name = sd.askstring("Wyszukiwanie binarne", "Podaj dokładną nazwę gwiazdy:")
        if not target_name:
            return

        index_in_sorted = binary_search_by_name(self.stars, target_name)
        if index_in_sorted is None:
            messagebox.showinfo("Wynik", f"Nie znaleziono gwiazdy '{target_name}'.")
        else:
            sorted_by_name = sorted(self.stars, key=lambda s: s.name.lower())
            found_star = sorted_by_name[index_in_sorted]
            messagebox.showinfo(
                "Wynik", 
                f"Znaleziono gwiazdę:\n\n"
                f"Nazwa: {found_star.name}\n"
                f"Odległość: {found_star.distance} ly\n"
                f"Typ widmowy: {found_star.spectral_type}"
            )

    def save_current_file(self):
        if self.current_file_path:
            try:
                save_stars_to_file(self.current_file_path, self.stars)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać do pliku.\n{e}")
        else:
            pass  # brak pliku = brak zapisu

def main():
    app = ModernStarsApp()
    app.mainloop()

if __name__ == "__main__":
    main()
