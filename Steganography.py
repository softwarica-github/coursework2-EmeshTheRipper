import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image
import tempfile
import os

class SteganographyTool:
    def hide_text(self, image_path, text, output_path):
        try:
            img = Image.open(image_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')

            binary_text = ''.join(format(ord(char), '08b') for char in text)
            if len(binary_text) > img.width * img.height * 4:
                raise ValueError("Text is too long to hide in the image.")

            pixels = list(img.getdata())
            index = 0

            for i in range(len(pixels)):
                r, g, b, a = pixels[i]
                if index < len(binary_text):
                    bit = int(binary_text[index])
                    a = (a & 254) | bit  # Hide bit in least significant bit of alpha channel
                    pixels[i] = (r, g, b, a)
                    index += 1

            img.putdata(pixels)
            img.save(output_path)
            return True
        except Exception as e:
            print(f"Error in hide_text: {e}")
            return False

    def extract_text(self, image_path):
        try:
            img = Image.open(image_path)
            if img.mode != 'RGBA':
                raise ValueError("Image must be in RGBA mode to extract text.")

            pixels = list(img.getdata())
            binary_text = ''

            for pixel in pixels:
                r, g, b, a = pixel
                binary_text += str(a & 1)  # Extract bit from least significant bit of alpha channel

            binary_text = binary_text.rstrip('0')

            text = ''
            for i in range(0, len(binary_text), 8):
                byte = binary_text[i:i + 8]
                text += chr(int(byte, 2))

            return text
        except Exception as e:
            print(f"Error in extract_text: {e}")
            return None

class SteganographyApp:
    def __init__(self, master):
        self.master = master
        master.title("Steganography Tool")

        self.label = tk.Label(master, text="Enter Text to Hide:")
        self.label.pack()

        self.text_entry = tk.Entry(master)
        self.text_entry.pack()

        self.hide_button = tk.Button(master, text="Hide Text", command=self.hide_text)
        self.hide_button.pack()

        self.extract_button = tk.Button(master, text="Extract Text", command=self.extract_text)
        self.extract_button.pack()

        self.result_label = tk.Label(master, text="", wraplength=300)  # Wrap text for better readability
        self.result_label.pack()

        self.output_label = tk.Label(master, text="Extracted Text:")
        self.output_label.pack()

        self.output_text = scrolledtext.ScrolledText(master, width=40, height=10)
        self.output_text.pack()

        self.steg_tool = SteganographyTool()

    def hide_text(self):
        text = self.text_entry.get()
        if not text:
            self.result_label.config(text="Please enter text to hide.")
            return

        image_path = filedialog.askopenfilename(title="Select Image")
        if not image_path:
            self.result_label.config(text="Please select an image.")
            return

        output_path = filedialog.asksaveasfilename(title="Save Image As", defaultextension=".png")
        if not output_path:
            return

        try:
            success = self.steg_tool.hide
