import os
import time
import shutil
import sys
from PyPDF2 import PdfReader, PdfWriter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from datetime import datetime
import argparse

# Function to get absolute paths relative to the script location
def get_absolute_path(relative_path):
    """Get absolute path relative to the script location."""
    # If the script is frozen (e.g., PyInstaller), use sys._MEIPASS
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # Otherwise, use the directory containing the script
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

# Define default paths relative to script location
DEFAULT_DROP_FOLDER = get_absolute_path("PDF Split Drop")
DEFAULT_COMPLETE_FOLDER = get_absolute_path("PDF Split Drop/Split Drop Complete")
DEFAULT_ORIGINAL_FOLDER = get_absolute_path("PDF Split Drop/Original PDF")

def setup_nltk():
    """Download NLTK data if not already available and return stopwords."""
    try:
        # Try to use existing stopwords first
        stop_words = set(stopwords.words('english'))
    except LookupError:
        try:
            # Download NLTK data - create a directory for NLTK data in the script's directory
            nltk_data_dir = get_absolute_path("nltk_data")
            os.makedirs(nltk_data_dir, exist_ok=True)
            nltk.data.path.append(nltk_data_dir)
            
            nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)
            nltk.download('stopwords', download_dir=nltk_data_dir, quiet=True)
            stop_words = set(stopwords.words('english'))
        except Exception as e:
            print(f"Warning: Could not download NLTK data: {e}")
            # Fallback with common English stopwords
            stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                            "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
                            'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 
                            'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 
                            'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 
                            'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 
                            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 
                            'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 
                            'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
                            'with', 'about', 'against', 'between', 'into', 'through', 'during', 
                            'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 
                            'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 
                            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 
                            'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 
                            'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 
                            'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 
                            "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 
                            've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', 
                            "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 
                            'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 
                            'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', 
                            "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 
                            'wouldn', "wouldn't"])
    return stop_words

def extract_keywords_from_text(text, stop_words, num_keywords=5):
    """Extract relevant keywords from text using frequency analysis."""
    try:
        # Tokenize and filter out stopwords
        word_tokens = word_tokenize(text.lower())
        filtered_words = [w for w in word_tokens if w.isalnum() and len(w) > 3 and w not in stop_words]
        
        # Count word frequency
        word_counter = Counter(filtered_words)
        
        # Get the most common words as keywords
        keywords = [word for word, count in word_counter.most_common(num_keywords)]
        return keywords
    except Exception as e:
        print(f"Error extracting keywords: {e}")
        return []

def extract_text_from_pdf_range(pdf_path, start_page, end_page, max_chars=2000):
    """Extract text from a range of pages in a PDF."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for i in range(start_page, min(end_page, len(reader.pages))):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text
            if len(text) > max_chars:
                break
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def generate_folder_name(pdf_path, stop_words):
    """Generate a folder name based on PDF content."""
    try:
        reader = PdfReader(pdf_path)
        # Extract text from the first few pages
        text = ""
        for i in range(min(5, len(reader.pages))):
            page_text = reader.pages[i].extract_text()
            if page_text:
                text += page_text
            if len(text) > 3000:  # Limit text to analyze
                break
                
        # Extract keywords
        kw = extract_keywords_from_text(text, stop_words)
        
        # Create folder name
        if kw:
            folder_name = '_'.join(kw[:3])  # Use top 3 keywords
        else:
            # Fallback to PDF filename without extension
            folder_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{folder_name}_{timestamp}"
    except Exception as e:
        print(f"Error generating folder name: {e}")
        # Fallback to timestamp and filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.splitext(os.path.basename(pdf_path))[0]
        return f"{filename}_{timestamp}"

def generate_split_name(pdf_path, start_page, end_page, split_num, stop_words):
    """Generate a name for a PDF split based on its content."""
    try:
        # Extract text from this range of pages
        text = extract_text_from_pdf_range(pdf_path, start_page, end_page)
        
        # Extract keywords
        kw = extract_keywords_from_text(text, stop_words, num_keywords=2)
        
        # Create split name
        if kw:
            keywords_text = '_'.join(kw)
            split_name = f"{split_num:02d}_{keywords_text}_p{start_page+1}-p{end_page}"
        else:
            # Fallback to page numbers
            split_name = f"{split_num:02d}_pages_{start_page+1}-{end_page}"
            
        return split_name
    except Exception as e:
        print(f"Error generating split name: {e}")
        # Simple fallback
        return f"{split_num:02d}_pages_{start_page+1}-{end_page}"

def split_pdf_by_size(pdf_path, complete_folder, original_folder, stop_words, max_size_mb=24):
    """Split a PDF into parts, each not exceeding max_size_mb."""
    try:
        # Create a folder for the splits
        folder_name = generate_folder_name(pdf_path, stop_words)
        output_folder = os.path.join(complete_folder, folder_name)
        os.makedirs(output_folder, exist_ok=True)
        
        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        
        # Estimate average page size
        pdf_size = os.path.getsize(pdf_path)
        avg_page_size = pdf_size / total_pages
        
        # Calculate approximate pages per split
        pages_per_split = int(max_size_mb * 1024 * 1024 / avg_page_size)
        
        # Ensure at least one page per split
        pages_per_split = max(1, pages_per_split)
        
        split_num = 1
        for start_page in range(0, total_pages, pages_per_split):
            end_page = min(start_page + pages_per_split, total_pages)
            
            # Create a new PDF writer
            writer = PdfWriter()
            
            # Add pages to the writer
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            # Generate split name
            split_name = generate_split_name(pdf_path, start_page, end_page, split_num, stop_words)
            output_path = os.path.join(output_folder, f"{split_name}.pdf")
            
            # Write the split PDF
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            
            print(f"Created split {split_num}: {output_path}")
            split_num += 1
        
        # Move the original PDF to the completed folder
        os.makedirs(original_folder, exist_ok=True)
        shutil.move(pdf_path, os.path.join(original_folder, os.path.basename(pdf_path)))
        print(f"Moved original PDF to: {original_folder}")
        
        return True
    except Exception as e:
        print(f"Error splitting PDF: {e}")
        return False

class PDFHandler(FileSystemEventHandler):
    def __init__(self, complete_folder, original_folder, stop_words):
        self.complete_folder = complete_folder
        self.original_folder = original_folder
        self.stop_words = stop_words
        
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            print(f"New PDF detected: {event.src_path}")
            # Add a small delay to ensure the file is fully written
            time.sleep(2)
            split_pdf_by_size(event.src_path, self.complete_folder, self.original_folder, self.stop_words)

def create_autorun_setup():
    """Create batch files for autorun setup."""
    # Create autorun.bat for Windows
    batch_content = """@echo off
echo Setting up PDF Splitter to run automatically...

:: Create a shortcut in the startup folder
powershell "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\PDF Splitter.lnk'); $Shortcut.TargetPath = '%~dp0start_pdf_splitter.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Start PDF Splitter'; $Shortcut.Save()"

echo Created startup shortcut. PDF Splitter will now run automatically when you log in.

:: Start the script now
start "" "%~dp0start_pdf_splitter.bat"

echo PDF Splitter is now running.
pause
"""
    with open(get_absolute_path("setup_autorun.bat"), 'w') as f:
        f.write(batch_content)
    
    # Create start script
    start_content = """@echo off
echo Starting PDF Splitter...
"%~dp0venv\\Scripts\\pythonw.exe" "%~dp0pdf_splitter.py"
"""
    with open(get_absolute_path("start_pdf_splitter.bat"), 'w') as f:
        f.write(start_content)
    
    # Create README
    readme_content = """# PDF Splitter

This tool automatically splits PDFs into smaller files (max 24MB) when they are dropped into the "PDF Split Drop" folder.

## Setup

1. Make sure you have Python installed
2. Run `setup.py` to create the virtual environment and install dependencies
3. Run `setup_autorun.bat` to make the script run automatically on startup

## Usage

Simply drop any PDF file into the "PDF Split Drop" folder. The tool will:

1. Automatically detect the new PDF
2. Split it into files under 24MB each
3. Create a new folder with a name based on the PDF content
4. Name each split with a number and content-relevant keywords
5. Move the original PDF to the "Original PDF" folder

All split files will be in the "Split Drop Complete" folder.

## Manual Start

If you don't want the tool to run automatically, you can start it manually by running `start_pdf_splitter.bat`.
"""
    with open(get_absolute_path("README.md"), 'w') as f:
        f.write(readme_content)
    
    # Create setup.py
    setup_content = """import os
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
    
    print("Setup complete!")
    print("You can now run setup_autorun.bat to make the script start automatically on system startup")
    print("Or run start_pdf_splitter.bat to start it manually")

if __name__ == "__main__":
    main()
"""
    with open(get_absolute_path("setup.py"), 'w') as f:
        f.write(setup_content)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="PDF Splitter - Split PDFs into smaller files")
    parser.add_argument("--drop-folder", help="Path to folder where PDFs will be dropped",
                        default=DEFAULT_DROP_FOLDER)
    parser.add_argument("--complete-folder", help="Path to folder where split PDFs will be stored",
                        default=DEFAULT_COMPLETE_FOLDER)
    parser.add_argument("--original-folder", help="Path to folder where original PDFs will be moved",
                        default=DEFAULT_ORIGINAL_FOLDER)
    parser.add_argument("--max-size", type=int, default=24,
                        help="Maximum size in MB for split files (default: 24)")
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up the folders
    drop_folder = args.drop_folder
    complete_folder = args.complete_folder
    original_folder = args.original_folder
    
    # Create the folders if they don't exist
    os.makedirs(drop_folder, exist_ok=True)
    os.makedirs(complete_folder, exist_ok=True)
    os.makedirs(original_folder, exist_ok=True)
    
    # Set up NLTK and get stopwords
    stop_words = setup_nltk()
    
    # Create helper scripts for auto-start
    create_autorun_setup()
    
    print(f"PDF Splitter started. Watching for PDFs in: {drop_folder}")
    print(f"Splits will be saved to: {complete_folder}")
    print(f"Original PDFs will be moved to: {original_folder}")
    
    # Set up the file system observer
    event_handler = PDFHandler(complete_folder, original_folder, stop_words)
    observer = Observer()
    observer.schedule(event_handler, drop_folder, recursive=False)
    observer.start()
    
    try:
        # Run indefinitely
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()