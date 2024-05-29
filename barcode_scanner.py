import tkinter as tk
from tkinter import messagebox
import cv2
from pyzbar.pyzbar import decode, ZBarSymbol
import warnings
from tkinter import ttk
import pygame

warnings.filterwarnings("ignore", message=".*pdf417.c.*")

product_prices = {
    '4801981127207': {'name': 'Sakto Sprite', 'price': 15.00},
    '4801981127177': {'name': 'Sakto Coke', 'price': 15.00},
}


def get_product_info(barcode):
    return product_prices.get(barcode, None)


def start_scanner(treeview, total_label, total_price_label, initial_total_price=0):
    cap = cv2.VideoCapture(0)

    width = 640
    height = 400

    detected_products = []
    total_price = initial_total_price
    product_detected = False

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (width, height))

            decoded_objects = decode(frame, symbols=[ZBarSymbol.EAN13, ZBarSymbol.UPCA])
            for obj in decoded_objects:
                barcode = obj.data.decode('utf-8')
                product_info = get_product_info(barcode)
                if product_info:
                    name = product_info['name']
                    price = product_info['price']
                    total_price += price
                    detected_products.append((name, price))
                    product_detected = True
                    pygame.mixer.Sound('beep.wav').play()
                else:
                    pygame.mixer.Sound('error.mp3').play()

            cv2.imshow('Barcode Scanner', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if product_detected:
                break

    except KeyboardInterrupt:
        pass

    for product in detected_products:
        treeview.insert("", "end", values=product)

    if product_detected:
        cv2.destroyAllWindows()
        cap.release()

    total_label.config(text=f"Total Price: ₱{total_price:.2f}")
    total_price_label.set(total_price)


def clear_products(treeview, total_label):
    treeview.delete(*treeview.get_children())
    total_label.config(text="Total Price: ₱0.00")


def create_gui():
    root = tk.Tk()
    root.title("Barcode Scanner By: Hesim_Gwapo")

    root.geometry("600x400")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=600, height=400, bg='#50C878', highlightthickness=0)
    canvas.pack()

    title_label = tk.Label(root, text="Barcode Scanner", font=("Times New Roman", 20, "bold"), bg="#50C878")
    canvas.create_window(300, 50, window=title_label)

    treeview = ttk.Treeview(root, columns=("Name", "Price"), show="headings", height=10)
    treeview.heading("Name", text="Product Name")
    treeview.heading("Price", text="Price")
    treeview.column("Name", width=300)
    treeview.column("Price", width=100)
    canvas.create_window(300, 200, window=treeview)

    total_price_var = tk.DoubleVar(value=0.00)

    total_label = tk.Label(root, text="Total Price: ₱0.00", font=("Arial", 12), bg="#50C878")
    canvas.create_window(300, 300, window=total_label)

    scanner_button = tk.Button(root, text="Start Scanner",
                               command=lambda: start_scanner(treeview, total_label, total_price_var,
                                                             initial_total_price=total_price_var.get()),
                               font=("Arial", 10, "bold"), bg="#50C878", fg="black")
    canvas.create_window(150, 350, window=scanner_button)

    reset_button = tk.Button(root, text="Reset", command=lambda: clear_products(treeview, total_label),
                             font=("Arial", 10, "bold"), bg="#50C878", fg="black")
    canvas.create_window(450, 350, window=reset_button)

    root.mainloop()


if __name__ == "__main__":
    pygame.mixer.init()
    create_gui()
