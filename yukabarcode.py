import requests
from bs4 import BeautifulSoup
import barcode
from barcode.writer import ImageWriter
from PIL import ImageTk, Image
import io
import tkinter as tk
from tkinter import messagebox

# Create a Code128 barcode generator
EAN = barcode.get_barcode_class('code128')

def generate_barcode():
    # Get the URL from the entry field
    url = url_entry.get()

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page with Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div containing the b tag with "UPC"
    divs = soup.find_all('div')
    upc_number = None
    for div in divs:
        b = div.find('b')
        if b and 'UPC' in b.get_text():
            upc_number = str(div.contents[-2]).strip()  # Extract the UPC number
            break

    if upc_number is not None:
        # Generate the barcode using the UPC number
        ean = EAN(upc_number, writer=ImageWriter())

        # Save the barcode to a BytesIO object (like a temporary file)
        barcode_data = io.BytesIO()
        ean.write(barcode_data)
        barcode_data.seek(0)

        # Load the barcode image into a Tkinter PhotoImage
        barcode_image = ImageTk.PhotoImage(Image.open(barcode_data))

        # Display the barcode image in the label
        barcode_label.config(image=barcode_image)
        barcode_label.image = barcode_image

        messagebox.showinfo("Success", "Barcode generated successfully")
    else:
        print("UPC number not found")

# Create a Tkinter window
window = tk.Tk()

# Create an entry field for the URL
url_entry = tk.Entry(window)
url_entry.pack()

# Create a button that generates the barcode when clicked
generate_button = tk.Button(window, text="Generate Barcode", command=generate_barcode)
generate_button.pack()

# Create a label to display the barcode image
barcode_label = tk.Label(window)
barcode_label.pack()

# Start the Tkinter event loop (this displays the window)
window.mainloop()
