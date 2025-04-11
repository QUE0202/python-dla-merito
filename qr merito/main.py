import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import qrcode
import os

LOGO_PATH = "imagines/logo.jpg"
OUTPUT_PATH = "qr_output.png"
DEFAULT_SIZE = (220, 220)  # Domyślny rozmiar

def generate_qr_with_logo(data):
    try:
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        if os.path.exists(LOGO_PATH):
            logo = Image.open(LOGO_PATH)
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width * 0.25)
            logo = logo.resize((logo_size, logo_size), Image.LANCZOS)
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

        qr_img.save(OUTPUT_PATH)
        return OUTPUT_PATH

    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wygenerować QR:\n{e}")
        return None

def on_generate():
    text = entry.get()
    if not text.strip():
        messagebox.showwarning("Brak danych", "Wprowadź tekst lub link.")
        return

    path = generate_qr_with_logo(text.strip())
    if path:
        show_qr(path)

def show_qr(path, size=DEFAULT_SIZE):
    qr_image = Image.open(path)
    qr_image = qr_image.resize(size, Image.LANCZOS)  # Normalna wielkość
    qr_photo = ImageTk.PhotoImage(qr_image)
    qr_label.config(image=qr_photo)
    qr_label.image = qr_photo
    qr_label.path = path  # Przechowywanie ścieżki do pliku w obiekcie label

def on_zoom_in():
    if hasattr(qr_label, "path"):
        qr_image = Image.open(qr_label.path)
        qr_width, qr_height = qr_image.size
        new_size = (int(qr_width * 1.5), int(qr_height * 1.5))  # Powiększenie o 50%
        show_qr(qr_label.path, size=new_size)

def on_zoom_out():
    if hasattr(qr_label, "path"):
        qr_image = Image.open(qr_label.path)
        qr_width, qr_height = qr_image.size
        new_size = (int(qr_width * 0.75), int(qr_height * 0.75))  # Zmniejszenie o 25%
        show_qr(qr_label.path, size=new_size)

def on_download():
    if hasattr(qr_label, "path"):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Pliki PNG", "*.png")])
        if save_path:
            try:
                qr_image = Image.open(qr_label.path)
                qr_image.save(save_path)
                messagebox.showinfo("Sukces", "QR Kod został zapisany.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się zapisać pliku:\n{e}")

root = tk.Tk()
root.title("QR Generator z Logo")

# Ustawienie aplikacji na tryb pełnoekranowy
root.attributes('-fullscreen', True)
root.resizable(False, False)

# Zwiększone czcionki i odstępy, aby pasowały do większego okna
tk.Label(root, text="Podaj link lub tekst:", font=("Arial", 40)).pack(pady=(100, 20))

entry = tk.Entry(root, width=60, font=("Arial", 28))
entry.pack(pady=10)

tk.Button(root, text="Generuj QR Kod", font=("Arial", 28), command=on_generate).pack(pady=30)

qr_label = tk.Label(root)
qr_label.pack(pady=30)

# Przycisk do powiększania
zoom_in_button = tk.Button(root, text="Powiększ", font=("Arial", 28), command=on_zoom_in)
zoom_in_button.pack(pady=20)

# Przycisk do zmniejszania
zoom_out_button = tk.Button(root, text="Zmniejsz", font=("Arial", 28), command=on_zoom_out)
zoom_out_button.pack(pady=20)

# Przycisk do pobrania
download_button = tk.Button(root, text="Pobierz QR Kod", font=("Arial", 28), command=on_download)
download_button.pack(pady=30)

tk.Label(root, text="© Jakub Troka", font=("Arial", 16), fg="gray").pack(side="bottom", pady=20)

root.mainloop()
