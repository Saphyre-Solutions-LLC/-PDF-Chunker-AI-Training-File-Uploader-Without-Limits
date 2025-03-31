# Create setup.py
cat > setup.py << 'EOF'
import os
import subprocess
import sys
import venv

def main():
    print("Setting up PDF Splitter...")
    
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
    subprocess.check_call([pip_executable, "install", "PyPDF2", "watchdog", "nltk"])
    
    # Create required folders
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base_dir, "PDF Split Drop"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "PDF Split Drop", "Split Drop Complete"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "PDF Split Drop", "Original PDF"), exist_ok=True)
    
    # Download NLTK data
    print("Downloading NLTK data...")
    try:
        subprocess.check_call([
            python_executable, "-c", 
            "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
        ])
    except Exception as e:
        print(f"Warning: Could not download NLTK data: {e}")
        print("You may need to download manually using: python -c \"import nltk; nltk.download('punkt'); nltk.download('stopwords')\"")
    
    print("Setup complete!")
    print("You can now run setup_autorun.bat to make the script start automatically on system startup")
    print("Or run start_pdf_splitter.bat to start it manually")

if __name__ == "__main__":
    main()
EOF