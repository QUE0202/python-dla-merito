import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading


class NasaHackerGallery(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NASA IMAGE DATABASE TERMINAL")
        self.geometry("1400x800")
        self.configure(bg="black")
        self.log_text = None
        self.image_refs = []
        self.create_widgets()

    def create_widgets(self):
        label_style = {"bg": "black", "fg": "#00FF00"}
        entry_style = {"bg": "black", "fg": "#00FF00", "insertbackground": "#00FF00"}

        title = tk.Label(self, text="NASA DATABASE ACCESS PORTAL", **label_style, font=("Courier New", 20, "bold"))
        title.pack(pady=10)

        self.search_entry = tk.Entry(self, width=40, font=("Courier New", 12), **entry_style)
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self, text=">> ACCESS", command=self.search_images, bg="black", fg="#00FF00",
                                       activebackground="black", activeforeground="#00FF00",
                                       font=("Courier New", 12, "bold"))
        self.search_button.pack(pady=5)

        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="black")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="left", fill="y")

        style_scroll = ttk.Style()
        style_scroll.theme_use('clam')
        style_scroll.configure("Vertical.TScrollbar", background="black", troughcolor="black",
                               bordercolor="black", arrowcolor="#00FF00")

        log_frame = tk.Frame(self, bg="black", width=300)
        log_frame.pack(side="right", fill="y")

        log_label = tk.Label(log_frame, text=">> SYSTEM LOG", **label_style, font=("Courier New", 14, "bold"))
        log_label.pack(pady=(10, 0))

        self.log_text = tk.Text(log_frame, height=20, width=40, bg="black", fg="#00FF00",
                                font=("Courier New", 10), state="disabled", wrap="word")
        self.log_text.pack(padx=10, pady=5, fill="both", expand=True)

        log_scroll = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scroll.pack(side="right", fill="y")
        self.log_text['yscrollcommand'] = log_scroll.set

    def log_message(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f">> {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def search_images(self):
        query = self.search_entry.get()
        if not query:
            self.log_message("Empty search query. Aborting.")
            return
        self.log_message(f"Searching for: '{query}'")
        threading.Thread(target=self.fetch_images, args=(query,), daemon=True).start()

    def fetch_images(self, query):
        url = f"https://images-api.nasa.gov/search?q={query}&media_type=image"
        try:
            response = requests.get(url)
            data = response.json()
            items = data.get("collection", {}).get("items", [])[:30]
            if not items:
                self.log_message("No results found.")
                return
            self.log_message(f"Found {len(items)} images.")
            self.display_images(items)
        except Exception as e:
            self.log_message(f"Error: {e}")

    def display_images(self, items):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()

        for index, item in enumerate(items):
            try:
                img_url = item["links"][0]["href"]
                img_data = requests.get(img_url).content
                img = Image.open(BytesIO(img_data))
                img.thumbnail((200, 200))
                tk_img = ImageTk.PhotoImage(img)
                self.image_refs.append(tk_img)

                label = tk.Label(self.scrollable_frame, image=tk_img, bg="black", cursor="hand2")
                label.grid(row=index // 3, column=index % 3, padx=10, pady=10)
                label.bind("<Button-1>", lambda e, url=img_url: self.enlarge_image(url))
            except Exception as e:
                self.log_message(f"Failed to load image: {e}")

    def enlarge_image(self, url):
        self.log_message("Image clicked – enlarging...")
        try:
            img_data = requests.get(url).content
            img = Image.open(BytesIO(img_data))
            img_window = tk.Toplevel(self)
            img_window.title("ENLARGED IMAGE")
            img_window.configure(bg="black")
            img_window.geometry("800x800")

            img.thumbnail((780, 780))
            tk_img = ImageTk.PhotoImage(img)
            label = tk.Label(img_window, image=tk_img, bg="black")
            label.image = tk_img
            label.pack(padx=10, pady=10)
        except Exception as e:
            self.log_message(f"Error enlarging image: {e}")


if __name__ == "__main__":
    NasaHackerGallery().mainloop()
