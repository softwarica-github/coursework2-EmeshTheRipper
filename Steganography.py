import tkinter as tk
from tkinter import filedialog
from PIL import Image

class SteganographyTool:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Steganography Tool")

        # Encryption section
        self.encrypt_frame = tk.Frame(self.root)
        self.encrypt_frame.grid(row=0, column=0, padx=10, pady=10)

        self.file_label = tk.Label(self.encrypt_frame, text="Choose Image:")
        self.file_label.grid(row=0, column=0, padx=5, pady=5)
        self.file_entry = tk.Entry(self.encrypt_frame, width=50)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button = tk.Button(self.encrypt_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.text_label = tk.Label(self.encrypt_frame, text="Enter Text to Hide:")
        self.text_label.grid(row=1, column=0, padx=5, pady=5)
        self.text_entry = tk.Text(self.encrypt_frame, height=4, width=38)
        self.text_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        self.encrypt_button = tk.Button(self.encrypt_frame, text="Encrypt", command=self.encrypt_text)
        self.encrypt_button.grid(row=2, column=1, padx=5, pady=5)

        self.output_label = tk.Label(self.encrypt_frame, text="", fg="green")
        self.output_label.grid(row=3, column=1, padx=5, pady=5)

        # Decryption section
        self.decrypt_frame = tk.Frame(self.root)
        self.decrypt_frame.grid(row=1, column=0, padx=10, pady=10)

        self.file_label_decrypt = tk.Label(self.decrypt_frame, text="Choose Image:")
        self.file_label_decrypt.grid(row=0, column=0, padx=5, pady=5)
        self.file_entry_decrypt = tk.Entry(self.decrypt_frame, width=50)
        self.file_entry_decrypt.grid(row=0, column=1, padx=5, pady=5)
        self.browse_button_decrypt = tk.Button(self.decrypt_frame, text="Browse", command=self.browse_file_decrypt)
        self.browse_button_decrypt.grid(row=0, column=2, padx=5, pady=5)

        self.decrypt_button = tk.Button(self.decrypt_frame, text="Decrypt", command=self.decrypt_text)
        self.decrypt_button.grid(row=1, column=1, padx=5, pady=5)

        self.output_text = tk.Text(self.decrypt_frame, height=4, width=38)
        self.output_text.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        self.output_label_decrypt = tk.Label(self.decrypt_frame, text="", fg="green")
        self.output_label_decrypt.grid(row=3, column=1, padx=5, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(tk.END, file_path)

    def browse_file_decrypt(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        self.file_entry_decrypt.delete(0, tk.END)
        self.file_entry_decrypt.insert(tk.END, file_path)

    def hide_text(self, image_path, text, output_path):
        try:
            img = Image.open(image_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            binary_text = ''.join(format(ord(char), '08b') for char in text)
            if len(binary_text) > img.width * img.height:
                raise ValueError("Text is too long to hide in the image.")
            pixels = list(img.getdata())
            index = 0
            for i in range(len(pixels)):
                r, g, b, a = pixels[i]
                if index < len(binary_text):
                    bit = int(binary_text[index])
                    a = (a & 254) | bit
                    pixels[i] = (r, g, b, a)
                    index += 1
            img.putdata(pixels)
            img.save(output_path)
            return True
        except Exception as e:
            print("Error:", e)
            return False

    def extract_text(self, image_path):
        try:
            img = Image.open(image_path)
            if img.mode != 'RGBA':
                raise ValueError("Image must be in RGBA mode to extract text.")
            pixels = list(img.getdata())
            binary_text = ''
            for pixel in pixels:
                binary_text += str(pixel[3] & 1)
            text = ''
            for i in range(0, len(binary_text), 8):
                byte = binary_text[i:i+8]
                text += chr(int(byte, 2))
            return text
        except Exception as e:
            print("Error:", e)
            return None

    def encrypt_text(self):
        image_path = self.file_entry.get()
        text = self.text_entry.get("1.0", tk.END).strip()
        if image_path and text:
            output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if output_path:
                success = self.hide_text(image_path, text, output_path)
                self.output_label.config(text="Text hidden successfully." if success else "Error hiding text.", fg="green" if success else "red")
            else:
                self.output_label.config(text="Operation canceled.", fg="red")
        else:
            self.output_label.config(text="Please fill all fields.", fg="red")

    def decrypt_text(self):
        image_path = self.file_entry_decrypt.get()
        if image_path:
            try:
                text = self.extract_text(image_path)
                if text:
                    self.output_text.delete(1.0, tk.END)
                    self.output_text.insert(tk.END, text)
                    self.output_label_decrypt.config(text="Text extracted successfully.", fg="green")
                else:
                    self.output_label_decrypt.config(text="Error extracting text.", fg="red")
            except Exception as e:
                self.output_label_decrypt.config(text="Error: " + str(e), fg="red")
        else:
            self.output_label_decrypt.config(text="Please fill all fields.", fg="red")

    def run(self):
        self.root.mainloop()

    # Unit test method for hiding and extracting text
    def unit_test(self):
        test_image_path = "path/to/test_image.png"
        test_text = "This is a test text."
        test_output_path = "path/to/test_output_image.png"

        # Encrypt text
        self.hide_text(test_image_path, test_text, test_output_path)

        # Decrypt text
        decrypted_text = self.extract_text(test_output_path)

        # Check if the decrypted text matches the original text
        assert decrypted_text == test_text, f"Unit test failed: {decrypted_text} != {test_text}"

        print("Unit test passed successfully.")

# Run the SteganographyTool application
if __name__ == "__main__":
    steganography_tool = SteganographyTool()
    steganography_tool.run()

    # Uncomment the following line to run the unit test
    # steganography_tool.unit_test()
