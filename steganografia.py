from PIL import Image
import ffmpeg

def encode_text_in_image(image_path, text, output_path):
    image = Image.open(image_path)
    encoded = image.copy()
    width, height = image.size
    
    # Aggiungi un marker per indicare la fine del testo
    text += "#####"
    
    # Converte il testo in una stringa binaria
    binary_text = ''.join([format(ord(char), '08b') for char in text])
    text_index = 0
    
    # Codifica il testo nei pixel dell'immagine
    for y in range(height):
        for x in range(width):
            if text_index < len(binary_text):
                pixel = list(image.getpixel((x, y)))
                original_pixel = pixel[:]
                for n in range(3):
                    if text_index < len(binary_text):
                        pixel[n] = pixel[n] & ~1 | int(binary_text[text_index])
                        text_index += 1
                encoded.putpixel((x, y), tuple(pixel))
                print(f"Pixel {x},{y} changed from {original_pixel} to {pixel}")
                print("Current text_index:", text_index)  
                print("Length of binary_text:", len(binary_text))  
            else:
                break
        if text_index >= len(binary_text):
            break

    
    # Salva l'immagine con il testo nascosto
    encoded.save(output_path)
    print("The text has been successfully hidden in the image!")