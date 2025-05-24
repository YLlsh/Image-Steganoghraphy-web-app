# 🖼️ Image Steganography

Image Steganography is the practice of hiding secret data (text) within an image without visibly altering it. This project provides a simple interface to encode and decode hidden messages inside images using basic steganographic techniques.

## 🔐 Features

- Encode text data into an image
- Decode hidden messages from an image
- Support for lossless image formats (e.g., PNG)
- Simple and user-friendly interface 
- Lightweight and efficient implementation

---
### Screenshot ###
**login**
![screenshot](screenshot/Screenshot%20(1).png)
**Registeration**
![screenshot](screenshot/Screenshot%20(2).png)
**Encryption page**
![screenshot](screenshot/Screenshot%20(3).png)
**Decryption page**
![screenshot](screenshot/Screenshot%20(4).png)

## 🚀 Installation and Setup Guide

Follow these steps to download, install, and run the project locally.

### 1. Download the Project ZIP

- Download the ZIP file of this project from your source (e.g., GitHub).
- Save it to your preferred location on your computer.

### 2. Extract the ZIP File

- Right-click the ZIP file and select **Extract All...** (Windows) or use your system’s unzip tool.
- Extract the contents to a folder you can easily access.

### 3. Open Terminal / Command Prompt 


- Navigate to the extracted project directory.
    ```
    cd path/to/extracted-folder

### 5. Install Required Dependencies
    
    pip install django pillow

### 6. Apply Database Migrations
Prepare the database schema for Django:

    python manage.py makemigrations
    python manage.py migrate
### 7. Run the Development Server###
Start the local Django server:
```
python manage.py runserver
