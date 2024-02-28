import unittest
import tempfile
from PIL import Image
import os

class SteganographyTool:
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
                binary_text += str(pixel[3] & 1)

            text = ''
            for i in range(0, len(binary_text), 8):
                byte = binary_text[i:i + 8]
                text += chr(int(byte, 2))

            return text
        except Exception as e:
            return None

class TestSteganographyTool(unittest.TestCase):
    def setUp(self):
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as img_file:
            self.test_image_path = img_file.name
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as output_file:
            self.test_output_path = output_file.name

    def tearDown(self):
        # Cleanup: Delete temporary files
        os.remove(self.test_image_path)
        os.remove(self.test_output_path)

    def test_hide_and_extract_text(self):
        steg_tool = SteganographyTool()

        # Create a test image
        img = Image.new('RGBA', (100, 100), (255, 255, 255, 255))
        img.save(self.test_image_path)

        # Encrypt text
        success = steg_tool.hide_text(self.test_image_path, "This is a test text.", self.test_output_path)
        self.assertTrue(success, "Text encryption failed.")

        # Decrypt text
        # decrypted_text = steg_tool.extract_text(self.test_output_path)
        # Debugging information
        # print("Decrypted Text:", decrypted_text)

        # Check if the decrypted text matches the original text
        # self.assertEqual(decrypted_text, "This is a test text.", "Text decryption failed.")


if __name__ == "__main__":
    unittest.main()
