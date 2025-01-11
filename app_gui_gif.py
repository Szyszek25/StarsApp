import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
from PIL import Image, ImageTk
from typing import List, Optional


# ======================= LOGIKA (backend) =========================

class Star:
    def __init__(self, name: str, distance: float, spectral_type: str):
        self.name = name
        self.distance = distance
        self.spectral_type = spectral_type

    def __str__(self):
        return f"{self.name} | {self.distance:.2f} ly | {self.spectral_type}"


def merge_sort(stars_list: List["Star"]) -> List["Star"]:
    if len(stars_list) <= 1:
        return stars_list
    mid = len(stars_list) // 2
    left_half = merge_sort(stars_list[:mid])
    right_half = merge_sort(stars_list[mid:])
    return merge(left_half, right_half)


def merge(left: List["Star"], right: List["Star"]) -> List["Star"]:
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


def binary_search_by_name(stars_list: List["Star"], target_name: str) -> Optional[int]:
    sorted_by_name = sorted(stars_list, key=lambda s: s.name.lower())
    left, right = 0, len(sorted_by_name) - 1
    tn_lower = target_name.lower()

    while left <= right:
        mid = (left + right) // 2
        mid_name = sorted_by_name[mid].name.lower()
        if mid_name == tn_lower:
            return mid
        elif mid_name < tn_lower:
            left = mid + 1
        else:
            right = mid - 1
    return None


def load_stars_from_file(filepath: str) -> List[Star]:
    loaded_stars = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
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
            except ValueError:
                continue
            loaded_stars.append(Star(name, distance, spectral))
    return loaded_stars


def save_stars_to_file(filepath: str, stars_list: List[Star]) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        for star in stars_list:
            line = f"{star.name};{star.distance};{star.spectral_type}\n"
            f.write(line)


# =============== Funkcje do animowanego banera GIF 21:9 ===============

def load_animated_gif_frames(filepath: str) -> List[Image.Image]:
    """
    Wczytuje wszystkie klatki z animowanego GIF-a (za pomocą Pillow)
    i zwraca listę obiektów PIL.Image w oryginalnym rozmiarze.
    """
    frames = []
    with Image.open(filepath) as im:
        try:
            while True:
                # Kopia bieżącej klatki
                frames.append(im.copy())
                im.seek(im.tell() + 1)
        except EOFError:
            pass
    return frames


def cover_crop_21x9(image: Image.Image, target_width=768) -> Image.Image:
    """
    Kadruje obraz w stylu 'cover' do proporcji 21:9 o zadanej szerokości (domyślnie 1366).
    """
    # docelowa wysokość:
    target_height = int(target_width * (9 / 45))

    orig_w, orig_h = image.size
    img_ratio = orig_w / orig_h
    desired_w, desired_h = target_width, target_height

    # Sprawdzamy, czy obraz jest "szerszy" czy "wyższy" w stosunku do 21:9
    if img_ratio > (desired_w / desired_h):
        # Obraz za szeroki
        scale = desired_h / orig_h
        new_w = int(orig_w * scale)
        new_h = desired_h
    else:
        # Obraz za wysoki (lub pasuje)
        scale = desired_w / orig_w
        new_w = desired_w
        new_h = int(orig_h * scale)

    resized = image.resize((new_w, new_h), Image.LANCZOS)

    # Kadrujemy środek
    left = (new_w - desired_w) // 2
    top = (new_h - desired_h) // 2
    right = left + desired_w
    bottom = top + desired_h

    cropped = resized.crop((left, top, right, bottom))
    return cropped


# ========================= GŁÓWNA KLASA APLIKACJI =========================

class ModernStarsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Konfiguracja stylu
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Aplikacja: Wyszukiwarka gwiazd w kosmosie ✨")
        self.geometry("950x768")

        # Lista gwiazd
        self.stars: List[Star] = []

        # Ścieżka do aktualnego pliku
        self.current_file_path: str | None = None

        # Kontener główny
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)

        # =============== BANER (animowany GIF) ===============
        self.banner_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        self.banner_frame.pack(side="top", fill="x")

        # Wczytujemy klatki z top_banner.gif (o ile istnieje)
        self.gif_frames = []
        self.gif_index = 0
        self.banner_images: List[ImageTk.PhotoImage] = []

        gif_path = os.path.join(os.path.dirname(__file__), "top_banner.gif")
        if os.path.isfile(gif_path):
            self.gif_frames = load_animated_gif_frames(gif_path)
            # Przygotowujemy kadrowane klatki (21:9, styl cover)
            for frame in self.gif_frames:
                cropped = cover_crop_21x9(frame, target_width=1366)
                # Konwertujemy do PhotoImage (tak, by można było ustawiać w labelu)
                # Ale zrobimy to dynamicznie w trakcie animacji, żeby nie marnować pamięci
                # (opcjonalnie można wstępnie wszystko przerobić).
            self.banner_label = ctk.CTkLabel(self.banner_frame, text="")
            self.banner_label.pack(fill="x")
            # Start animacji
            self.animate_gif_banner()
        else:
            # Brak pliku, wstawiamy "sztywny" label
            lbl = ctk.CTkLabel(self.banner_frame, text="(Brak top_banner.gif)")
            lbl.pack(pady=10)

        # =============== SEKCJA "RESZTY" APLIKACJI (pod banerem) ===============

        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Nagłówek
        self.header_label = ctk.CTkLabel(
            self.content_frame,
            text="Aplikacja: Wyszukiwarka gwiazd w kosmosie ✨",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.header_label.pack(pady=5)

        # Sekcja formularza
        self.form_frame = ctk.CTkFrame(self.content_frame)
        self.form_frame.pack(fill="x", padx=10, pady=5)

        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Nazwa gwiazdy")
        self.name_entry.grid(row=0, column=0, padx=5, pady=5)

        self.distance_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Odległość (ly)")
        self.distance_entry.grid(row=0, column=1, padx=5, pady=5)

        self.spectral_type_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Typ widmowy (np. G2V)")
        self.spectral_type_entry.grid(row=0, column=2, padx=5, pady=5)

        self.add_button = ctk.CTkButton(self.form_frame, text="Dodaj gwiazdę", command=self.add_star)
        self.add_button.grid(row=0, column=3, padx=5, pady=5)

        # Ramka przycisków
        self.buttons_frame = ctk.CTkFrame(self.content_frame)
        self.buttons_frame.pack(fill="x", padx=10, pady=5)

        self.load_button = ctk.CTkButton(self.buttons_frame, text="Wczytaj z pliku", command=self.load_from_file)
        self.load_button.pack(side="left", padx=5)

        self.search_partial_button = ctk.CTkButton(self.buttons_frame, text="Szukaj (częściowe)",
                                                   command=self.search_stars_partial)
        self.search_partial_button.pack(side="left", padx=5)

        self.search_exact_button = ctk.CTkButton(self.buttons_frame, text="Szukaj (dokładne, binarne)",
                                                 command=self.search_star_exact)
        self.search_exact_button.pack(side="left", padx=5)

        self.remove_by_name_button = ctk.CTkButton(self.buttons_frame, text="Usuń po nazwie",
                                                   command=self.remove_by_name)
        self.remove_by_name_button.pack(side="left", padx=5)

        self.remove_selected_button = ctk.CTkButton(self.buttons_frame, text="Usuń zaznaczoną",
                                                    command=self.remove_selected_star)
        self.remove_selected_button.pack(side="left", padx=5)

        self.refresh_button = ctk.CTkButton(self.buttons_frame, text="Odśwież listę", command=self.refresh_list)
        self.refresh_button.pack(side="left", padx=5)

        # Lista gwiazd
        self.list_frame = ctk.CTkFrame(self.content_frame)
        self.list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.star_listbox = tk.Listbox(self.list_frame, height=12, selectmode=tk.SINGLE)
        self.star_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical", command=self.star_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.star_listbox.config(yscrollcommand=self.scrollbar.set)

    # ------------------ ANIMACJA GIF W BANERZE ------------------

    def animate_gif_banner(self):
        """
        Przełącza klatki co ~100ms, tworząc animację.
        """
        if not self.gif_frames:
            return

        # Bierzemy aktualną klatkę
        frame = self.gif_frames[self.gif_index]
        # Kadrujemy w stylu cover 21:9
        cropped = cover_crop_21x9(frame, target_width=1366)
        # Konwertujemy do PhotoImage, zapamiętujemy w liście, by nie zniknęło z pamięci
        photo = ImageTk.PhotoImage(cropped)
        if len(self.banner_images) <= self.gif_index:
            self.banner_images.append(photo)
        else:
            self.banner_images[self.gif_index] = photo

        # Ustawiamy w labelu
        self.banner_label.configure(image=photo)

        # Następna klatka
        self.gif_index = (self.gif_index + 1) % len(self.gif_frames)

        # Po 100ms wywołaj ponownie
        self.after(100, self.animate_gif_banner)

    # ------------------ FUNKCJE ZWIĄZANE Z LOGIKĄ APPKI ------------------

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


def main():
    app = ModernStarsApp()
    app.mainloop()


if __name__ == "__main__":
    main()
