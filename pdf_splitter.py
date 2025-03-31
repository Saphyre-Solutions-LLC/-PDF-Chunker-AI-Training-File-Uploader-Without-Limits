import os
import time
import shutil
import sys
import tempfile  # Added for temporary file handling
from PyPDF2 import PdfReader, PdfWriter
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from datetime import datetime
import argparse
import logging  # Added for better logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pdf_splitter.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("pdf_splitter")

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
        nltk.data.find('corpora/stopwords')
        nltk.data.find('tokenizers/punkt')
        stop_words = set(stopwords.words('english'))
        logger.info("NLTK data already downloaded and available")
        return stop_words
    except LookupError:
        try:
            # Download NLTK data - create a directory for NLTK data in the script's directory
            nltk_data_dir = get_absolute_path("nltk_data")
            os.makedirs(nltk_data_dir, exist_ok=True)
            nltk.data.path.append(nltk_data_dir)
            
            logger.info(f"Downloading NLTK data to {nltk_data_dir}")
            nltk.download('punkt', download_dir=nltk_data_dir)
            nltk.download('stopwords', download_dir=nltk_data_dir)
            
            # Double-check that data is now available
            try:
                stop_words = set(stopwords.words('english'))
                logger.info("NLTK data successfully downloaded and loaded")
                return stop_words
            except LookupError as e:
                logger.error(f"NLTK data still not available after download: {e}")
                raise
        except Exception as e:
            logger.warning(f"Could not download NLTK data: {e}")
            # Fallback with common English stopwords
            logger.info("Using fallback stopwords list")
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
                            'than', 'too', 'very'])
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
        logger.error(f"Error extracting keywords: {e}")
        return []

def extract_text_from_pdf_range(pdf_path, start_page, end_page, max_chars=2000):
    """Extract text from a range of pages in a PDF."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for i in range(start_page, min(end_page, len(reader.pages))):
            page_text = reader.pages[i].extract_text() or ""
            text += page_text
            if len(text) > max_chars:
                break
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""

def generate_folder_name(pdf_path, stop_words):
    """Generate a folder name based on PDF content."""
    try:
        reader = PdfReader(pdf_path)
        # Extract text from the first few pages
        text = ""
        for i in range(min(5, len(reader.pages))):
            page_text = reader.pages[i].extract_text() or ""
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
        
        # Clean up folder name - remove invalid characters
        folder_name = ''.join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in folder_name)
        return f"{folder_name}_{timestamp}"
    except Exception as e:
        logger.error(f"Error generating folder name: {e}")
        # Fallback to timestamp and filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.splitext(os.path.basename(pdf_path))[0]
        # Clean up filename
        filename = ''.join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in filename)
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
            
        # Clean up file name - remove invalid characters
        split_name = ''.join(c if c.isalnum() or c in [' ', '_', '-'] else '_' for c in split_name)
        return split_name
    except Exception as e:
        logger.error(f"Error generating split name: {e}")
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
        
        if total_pages == 0:
            logger.warning(f"PDF has no pages: {pdf_path}")
            return False
        
        # Estimate average page size
        pdf_size = os.path.getsize(pdf_path)
        avg_page_size = pdf_size / total_pages
        
        # Use a conservative target size (20MB) to ensure we stay under the limit
        target_size_mb = min(20, max_size_mb - 4)
        logger.info(f"Using target size of {target_size_mb}MB to ensure final size is under {max_size_mb}MB")
        
        split_num = 1
        start_page = 0
        
        while start_page < total_pages:
            # Initial estimate of pages per chunk (conservative)
            estimated_pages = max(1, int(target_size_mb * 1024 * 1024 / avg_page_size))
            end_page = min(start_page + estimated_pages, total_pages)
            
            # For very large pages, we might need to include just one page
            if end_page == start_page:
                end_page = start_page + 1
            
            logger.info(f"Creating split {split_num} with pages {start_page+1} to {end_page}")
            
            # Create a temporary writer for the current chunk
            writer = PdfWriter()
            
            # Add pages to the writer
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])
            
            # Create a temporary file to check the actual size
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Write to the temporary file
            with open(temp_path, 'wb') as output_file:
                writer.write(output_file)
            
            # Check the actual file size
            actual_size_mb = os.path.getsize(temp_path) / (1024 * 1024)
            logger.info(f"Split {split_num} actual size: {actual_size_mb:.2f}MB")
            
            # If the file is too large and contains more than one page, reduce the page count
            if actual_size_mb > max_size_mb and end_page - start_page > 1:
                logger.warning(f"Split {split_num} exceeds {max_size_mb}MB ({actual_size_mb:.2f}MB), reducing page count")
                
                # Remove the temporary file
                os.unlink(temp_path)
                
                # Binary search to find the right number of pages
                min_pages = 1
                max_pages = end_page - start_page - 1
                
                while min_pages <= max_pages:
                    mid_pages = (min_pages + max_pages) // 2
                    test_end_page = start_page + mid_pages
                    
                    # Create test writer
                    test_writer = PdfWriter()
                    for page_num in range(start_page, test_end_page):
                        test_writer.add_page(reader.pages[page_num])
                    
                    # Create a temporary file for the test
                    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as test_temp_file:
                        test_temp_path = test_temp_file.name
                    
                    # Write to the test file
                    with open(test_temp_path, 'wb') as test_output_file:
                        test_writer.write(test_output_file)
                    
                    # Check the test file size
                    test_size_mb = os.path.getsize(test_temp_path) / (1024 * 1024)
                    
                    # Clean up the test file
                    os.unlink(test_temp_path)
                    
                    if test_size_mb <= max_size_mb:
                        min_pages = mid_pages + 1
                    else:
                        max_pages = mid_pages - 1
                
                # Use the result of the binary search
                end_page = start_page + max_pages
                
                # If we couldn't reduce enough (e.g., a single page is too large), handle it
                if end_page <= start_page:
                    logger.warning(f"Cannot split page {start_page+1} to be under {max_size_mb}MB")
                    end_page = start_page + 1
                
                # Recreate the writer with the correct page count
                writer = PdfWriter()
                for page_num in range(start_page, end_page):
                    writer.add_page(reader.pages[page_num])
                
                # Create a new temporary file
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                    temp_path = temp_file.name
                
                # Write to the temporary file
                with open(temp_path, 'wb') as output_file:
                    writer.write(output_file)
                
                # Update actual size for logging
                actual_size_mb = os.path.getsize(temp_path) / (1024 * 1024)
                logger.info(f"Adjusted split {split_num} with pages {start_page+1} to {end_page}, size: {actual_size_mb:.2f}MB")
            
            # Generate a name for the split
            split_name = generate_split_name(pdf_path, start_page, end_page, split_num, stop_words)
            output_path = os.path.join(output_folder, f"{split_name}.pdf")
            
            # Move the temporary file to the final location
            shutil.move(temp_path, output_path)
            
            logger.info(f"Created split {split_num}: {output_path} ({actual_size_mb:.2f}MB)")
            
            # Move to the next split
            start_page = end_page
            split_num += 1
        
        # Move the original PDF to the completed folder
        os.makedirs(original_folder, exist_ok=True)
        dest_path = os.path.join(original_folder, os.path.basename(pdf_path))
        
        # If the destination file already exists, add a timestamp
        if os.path.exists(dest_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename, ext = os.path.splitext(os.path.basename(pdf_path))
            dest_path = os.path.join(original_folder, f"{filename}_{timestamp}{ext}")
        
        shutil.move(pdf_path, dest_path)
        logger.info(f"Moved original PDF to: {dest_path}")
        
        return True
    except Exception as e:
        logger.error(f"Error splitting PDF: {e}", exc_info=True)
        return False

class PDFHandler(FileSystemEventHandler):
    def __init__(self, complete_folder, original_folder, stop_words):
        self.complete_folder = complete_folder
        self.original_folder = original_folder
        self.stop_words = stop_words
        
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            logger.info(f"New PDF detected: {event.src_path}")
            
            # Add a small delay to ensure the file is fully written
            time.sleep(2)
            
            # Check if the file is still there (it might have been moved by another process)
            if not os.path.exists(event.src_path):
                logger.warning(f"File no longer exists: {event.src_path}")
                return
            
            # Check if the file is still being written to
            try:
                size1 = os.path.getsize(event.src_path)
                time.sleep(1)
                size2 = os.path.getsize(event.src_path)
                
                if size1 != size2:
                    logger.info(f"File is still being written, waiting...")
                    time.sleep(2)  # Wait a bit longer
            except Exception as e:
                logger.warning(f"Error checking file stability: {e}")
            
            # Process the PDF
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
    setup_autorun_path = get_absolute_path("setup_autorun.bat")
    with open(setup_autorun_path, 'w') as f:
        f.write(batch_content)
    logger.info(f"Created setup_autorun.bat at {setup_autorun_path}")
    
    # Create start script
    start_content = """@echo off
echo Starting PDF Splitter...
"%~dp0venv\\Scripts\\pythonw.exe" "%~dp0pdf_splitter.py"
echo PDF Splitter is running in the background.
"""
    start_pdf_splitter_path = get_absolute_path("start_pdf_splitter.bat")
    with open(start_pdf_splitter_path, 'w') as f:
        f.write(start_content)
    logger.info(f"Created start_pdf_splitter.bat at {start_pdf_splitter_path}")
    
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

## Troubleshooting

If you encounter issues:

1. Check the pdf_splitter.log file for error messages
2. Make sure all folders exist and are accessible
3. Ensure NLTK data is downloaded by running: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`
"""
    readme_path = get_absolute_path("README.md")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    logger.info(f"Created README.md at {readme_path}")
    
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
    
    # Download NLTK data
    print("Downloading NLTK data...")
    subprocess.check_call([
        python_executable, "-c", 
        "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
    ])
    
    print("Setup complete!")
    print("You can now run setup_autorun.bat to make the script start automatically on system startup")
    print("Or run start_pdf_splitter.bat to start it manually")

if __name__ == "__main__":
    main()
"""
    setup_path = get_absolute_path("setup.py")
    with open(setup_path, 'w') as f:
        f.write(setup_content)
    logger.info(f"Created setup.py at {setup_path}")

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
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_arguments()
    
    # Set up logging level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    # Set up the folders
    drop_folder = args.drop_folder
    complete_folder = args.complete_folder
    original_folder = args.original_folder
    max_size = args.max_size
    
    logger.info(f"Starting PDF Splitter with max size: {max_size}MB")
    logger.info(f"Drop folder: {drop_folder}")
    logger.info(f"Complete folder: {complete_folder}")
    logger.info(f"Original folder: {original_folder}")
    
    # Create the folders if they don't exist
    os.makedirs(drop_folder, exist_ok=True)
    os.makedirs(complete_folder, exist_ok=True)
    os.makedirs(original_folder, exist_ok=True)
    
    # Set up NLTK and get stopwords
    try:
        stop_words = setup_nltk()
    except Exception as e:
        logger.error(f"Error setting up NLTK: {e}")
        logger.error("Will attempt to continue with a minimal stopwords list")
        # Basic fallback
        stop_words = set(['a', 'an', 'the', 'and', 'or', 'but', 'if', 'then', 'else', 'when', 'where', 'why', 'how'])
    
    # Create helper scripts for auto-start
    create_autorun_setup()
    
    print(f"PDF Splitter started. Watching for PDFs in: {drop_folder}")
    print(f"Splits will be saved to: {complete_folder}")
    print(f"Original PDFs will be moved to: {original_folder}")
    print(f"Maximum split size: {max_size}MB")
    
    # Set up the file system observer
    event_handler = PDFHandler(complete_folder, original_folder, stop_words)
    observer = Observer()
    observer.schedule(event_handler, drop_folder, recursive=False)
    observer.start()
    
    try:
        # Process any existing PDF files in the drop folder
        for filename in os.listdir(drop_folder):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(drop_folder, filename)
                logger.info(f"Found existing PDF in drop folder: {pdf_path}")
                split_pdf_by_size(pdf_path, complete_folder, original_folder, stop_words, max_size)
        
        # Run indefinitely
        logger.info("Watching for new PDFs...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping PDF Splitter due to keyboard interrupt")
        observer.stop()
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()