import os
import subprocess
import sys
import venv

def main():
    print("Setting up PDF-to-Text Splitter...")
    
    # Create virtual environment
    venv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
    print(f"Creating virtual environment in {venv_dir}")
    venv.create(venv_dir, with_pip=True)
    
    # Determine python executable path
    if os.name == 'nt':  # Windows
        python_executable = os.path.join(venv_dir, "Scripts", "python.exe")
        pip_executable = os.path.join(venv_dir, "Scripts", "pip.exe")
    else:  # Unix/Linux
        python_executable = os.path.join(venv_dir, "bin", "python")
        pip_executable = os.path.join(venv_dir, "bin", "pip")
    
    # Install dependencies
    print("Installing required packages...")
    subprocess.check_call([pip_executable, "install", "PyPDF2", "watchdog", "nltk", "pytesseract", "pdf2image", "pillow"])
    
    # Create required folders
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base_dir, "PDF Split Drop"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "PDF Split Drop", "Split Drop Complete"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "PDF Split Drop", "Original PDF"), exist_ok=True)
    
    # Additional setup instructions for Tesseract OCR
    print("\nIMPORTANT: You need to install Tesseract OCR on your system:")
    if os.name == 'nt':  # Windows
        print("1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install and add to PATH")
        print("3. Default location: C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
    else:  # Unix/Linux
        print("1. For Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("2. For macOS: brew install tesseract")
    
    # Additional setup instructions for Poppler (for pdf2image)
    print("\nYou also need to install Poppler:")
    if os.name == 'nt':  # Windows
        print("1. Download from: https://github.com/oschwartz10612/poppler-windows/releases/")
        print("2. Extract and add bin folder to PATH")
    else:  # Unix/Linux
        print("1. For Ubuntu/Debian: sudo apt-get install poppler-utils")
        print("2. For macOS: brew install poppler")
    
    print("\nSetup complete!")
    print("After installing Tesseract OCR and Poppler, you can:")
    print("1. Run setup_autorun.bat to make the script start automatically on system startup")
    print("2. Or run start_pdf_splitter.bat to start it manually")

if __name__ == "__main__":
    main()
