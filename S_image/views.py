import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import base64
import io
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from PIL import Image
from .models import *
def derive_key_from_password(password: str):

    salt = b'some_random_salt'  
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    derived_key = kdf.derive(password.encode())  # This for password encoded into bytes
    return base64.urlsafe_b64encode(derived_key)  # Return as a URL-safe base64-encoded key

# for encode text into the image (LSB Steganography)
def encode_image(image_path, text, password):
   
    key = derive_key_from_password(password)
    cipher = Fernet(key)

    # Encrypt the text using the Fernet cipher
    encrypted_text = cipher.encrypt(text.encode())

    binary_text = ''.join(format(byte, '08b') for byte in encrypted_text)

    # Open the image using PIL
    img = Image.open(image_path)
    pixels = img.load()

    data_index = 0
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(pixels[x, y])
            for i in range(3):  # Modify RGB channels
                if data_index < len(binary_text):
                    pixel[i] = (pixel[i] & 0xFE) | int(binary_text[data_index])  # Modify LSB
                    data_index += 1
            pixels[x, y] = tuple(pixel)

            if data_index >= len(binary_text):
                break
        else:
            continue
        break

    return img, key  

# function for extract encrypted text from the image
def decode_image(image, password):
    key = derive_key_from_password(password)
    cipher = Fernet(key)

    # PIL use
    img = Image.open(image)
    pixels = img.load()

    binary_text = ""
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(pixels[x, y])
            for i in range(3):  # Check RGB channels
                binary_text += str(pixel[i] & 1)  # Extract LSB

    # Convert binary to bytes
    byte_data = bytearray()
    for i in range(0, len(binary_text), 8):
        byte_data.append(int(binary_text[i:i+8], 2))

    # Decrypt the text using the derived password key
    try:
        decrypted_text = cipher.decrypt(bytes(byte_data)).decode()
    except Exception as e:
        return None  # If decryption fails, return None

    return decrypted_text

# Django view to handle image encoding (steganography)

@login_required(login_url='/l_page/')
def encode_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        password = request.POST.get('password')
        image_file = request.FILES.get('image')

        # Ensure 'media' directory exists
        media_dir = os.path.join('media', 'steganographed_images')
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # Save the original image temporarily
        temp_image_path = os.path.join(media_dir, 'temp_image_to_encode.png')
        with open(temp_image_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Encode the image
        modified_image, encryption_key = encode_image(temp_image_path, text, password)

        # Save the modified image to a file
        encoded_image_path = f"steganographed_images/{request.user.username}_encoded.png"
        full_path = os.path.join('media', encoded_image_path)
        modified_image.save(full_path, format='PNG')

        # Save the encoded image in the database
        stego_image = EncryptedHistory.objects.create(user = request.user, E_image = encoded_image_path)
        # Redirect user to the download page
        
        image_path = os.path.join('media', stego_image.E_image.name)
        with open(image_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="{stego_image.user.username}_encoded.png"'
            return response
    return render(request, 'encode.html')

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

# Django view to handle image decoding (extracting hidden message)
@login_required(login_url='/l_page/')
def decode_view(request):
    if request.method == 'POST':
        # Extract image and password from the request
        image_file = request.FILES.get('image')
        password = request.POST.get('password')

        # Ensure 'media' directory exists
        media_dir = os.path.join('media')
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        # Save the uploaded image temporarily
        temp_image_path = os.path.join(media_dir, 'temp_image_to_decode.png')
        with open(temp_image_path, 'wb') as f:
            for chunk in image_file.chunks():
                f.write(chunk)

        # Decode the image with the password
        decoded_text = decode_image(temp_image_path, password)

        if decoded_text is None:
            messages.info(request, "Password is worng")
            return redirect('/decode/')
        else:
            return render(request, 'decode.html',context = {'decoded_text': decoded_text})
        
    return render(request, 'decode.html')