import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import qrcode
import os

# Ścieżki do plików
LOGO_PATH = "imagines/logo.jpg"
OUTPUT_PATH = "qr_output.png"

def generate_qr_with_logo(data):
    try:
        # Tworzenie kodu QR
        qr = qrcode.QRCode(
            version=4,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Wczytywanie logo
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

def show_qr(path):
    qr_image = Image.open(path)
    qr_image = qr_image.resize((220, 220), Image.LANCZOS)
    qr_photo = ImageTk.PhotoImage(qr_image)
    qr_label.config(image=qr_photo)
    qr_label.image = qr_photo

# === GUI ===
root = tk.Tk()
root.title("QR Generator z Logo")
root.geometry("360x400")
root.resizable(False, False)

tk.Label(root, text="🔗 Podaj link lub tekst:", font=("Arial", 12)).pack(pady=(20, 5))

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(pady=5)

tk.Button(root, text="🎯 Generuj QR Kod", font=("Arial", 12), command=on_generate).pack(pady=10)

qr_label = tk.Label(root)
qr_label.pack(pady=20)

tk.Label(root, text="© KuBa Industries", font=("Arial", 9), fg="gray").pack(side="bottom", pady=10)

root.mainloop()
