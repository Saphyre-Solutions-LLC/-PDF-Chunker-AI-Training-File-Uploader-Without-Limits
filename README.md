# 🚀 PDF Chunker & AI Training Data Generator

## Intelligent PDF-to-Text Conversion with OCR for AI Model Training

![Version](https://img.shields.io/badge/Version-1.1.0-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)

---

## 💡 What This Tool Does

This intelligent system automatically converts PDFs into AI-ready text files, solving common problems with large document processing:

- **Overcomes Size Limitations**: Splits large PDFs that exceed upload limits for AI systems
- **Extracts Text Intelligently**: Uses advanced OCR to handle scanned documents and images
- **Creates AI-Optimized Format**: Produces clean, structured text files perfect for AI training
- **Organizes Content Automatically**: Creates content-aware folder and file naming

Simply drop any PDF into a folder and the system automatically:
1. Detects the document and analyzes its content
2. Extracts all text (even from scanned pages) using OCR when needed
3. Splits the content into logical chunks with intelligent naming
4. Formats the text with clear structure, metadata, and page markers
5. Organizes everything in descriptively named folders
6. Preserves your original PDF

**Zero manual effort required beyond initial setup.**

---

## 📋 Features

- **Text Extraction with OCR**: Automatically extracts text from scanned documents
- **AI-Optimized Text Structure**: Creates perfectly formatted text for AI model training
- **Smart Splitting Logic**: Divides documents at logical boundaries
- **Content-Based Naming**: Uses document content to name files and folders
- **Zero-Click Workflow**: Just drop files and everything happens automatically
- **Original PDF Preservation**: Keeps your source documents intact
- **Metadata Generation**: Adds useful metadata to each text chunk
- **Multi-Platform Support**: Works on Windows, macOS, and Linux

---

## 🖥️ System Requirements

- **Operating System**: Windows 7+, macOS 10.12+, or modern Linux distributions
- **Python**: Version 3.6 or higher
- **RAM**: 4GB+ recommended (8GB+ for very large PDFs)
- **Disk Space**: 100MB for installation + space for PDFs and text files
- **External Dependencies**:
  - Tesseract OCR engine
  - Poppler utilities (for PDF processing)

---

## 📦 Installation Guide

### Step 1: Get the Code

```bash
# Clone the repository
git clone https://github.com/Saphyre-Solutions-LLC/-PDF-Chunker-AI-Training-File-Uploader-Without-Limits.git

# Navigate to the folder
cd -PDF-Chunker-AI-Training-File-Uploader-Without-Limits
```

### Step 2: Install External Dependencies

#### Windows:
1. **Install Tesseract OCR**:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Run the installer and choose to add Tesseract to your PATH
   - Default install location: `C:\Program Files\Tesseract-OCR\`

2. **Install Poppler**:
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases/
   - Extract the files to a folder (e.g., `C:\Program Files\poppler\`)
   - Add the `bin` folder to your PATH:
     - Search for "Environment Variables" in Windows Search
     - Edit the "Path" variable
     - Add the bin folder path (e.g., `C:\Program Files\poppler\bin`)
     - Click OK and restart your terminal/command prompt

#### macOS:
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Tesseract and Poppler
brew install tesseract poppler
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils
```

### Step 3: Set Up Python Environment

```bash
# Run the setup script
python setup.py
```

This script will:
- Create a virtual environment
- Install all Python dependencies
- Create the necessary folder structure

### Step 4: Configure Auto-Start (Optional but Recommended)

#### Windows:
```bash
setup_autorun.bat
```

#### macOS/Linux:
```bash
chmod +x setup_autorun.sh
./setup_autorun.sh
```

These scripts create a startup item so the PDF processor runs automatically when you log in.

### Step 5: Start the Service

If you didn't set up auto-start or want to run it immediately:

#### Windows:
```bash
start_pdf_splitter.bat
```

#### macOS/Linux:
```bash
chmod +x start_pdf_splitter.sh
./start_pdf_splitter.sh
```

---

## 📝 How to Use

1. **Drop PDFs for Processing**:
   - Simply drag and drop any PDF file into the `PDF Split Drop` folder
   - That's it! No further action required

2. **Find Your Processed Files**:
   - Look in `PDF Split Drop/Split Drop Complete`
   - Each PDF gets its own folder with a name based on its content
   - Inside each folder are text files containing the extracted content

3. **Original Files**:
   - Your original PDFs are automatically moved to `PDF Split Drop/Original PDF`
   - Nothing is deleted during processing

4. **Using with AI Tools**:
   - The generated text files are formatted specifically for AI training
   - Upload them directly to Claude or other AI platforms
   - No further processing or formatting is needed

---

## 🧬 Understanding the Output

### Folder Structure

After processing, your files will be organized like this:

```
PDF Split Drop/
├── Split Drop Complete/
│   ├── Financial_Report_2023_20250401_123045/
│   │   ├── 01_executive_summary_p1-p12.txt
│   │   ├── 02_financial_statements_p13-p28.txt
│   │   ├── 03_market_analysis_p29-p45.txt
│   │   ├── 04_future_outlook_p46-p68.txt
│   │   └── _metadata_summary.json
│   │
│   └── Research_Paper_Physics_20250401_145623/
│       ├── 01_abstract_introduction_p1-p8.txt
│       ├── 02_methodology_p9-p24.txt
│       ├── 03_results_discussion_p25-p36.txt
│       └── _metadata_summary.json
│
└── Original PDF/
    ├── Annual_Financial_Report_2023.pdf
    └── Quantum_Physics_Research_Paper.pdf
```

### Text File Structure

Each generated text file follows this format:

```
# DOCUMENT: [Document Title - Part X]

## METADATA
- Source: [Original Filename]
- Pages: [Page Range]
- Date Processed: [Processing Date]
- Content Summary: [Brief Description]

## CONTENT

==== PAGE 1 ====
[Page 1 content...]

==== PAGE 2 ====
[Page 2 content...]

...

## END OF DOCUMENT
```

This structure is optimized for AI training, with clear document boundaries and metadata.

---

## ⚙️ Advanced Configuration

### Command Line Options

The script supports several command-line options:

```bash
python pdf_splitter.py --help
```

Output:
```
usage: pdf_splitter.py [-h] [--drop-folder DROP_FOLDER] [--complete-folder COMPLETE_FOLDER] 
                       [--original-folder ORIGINAL_FOLDER] [--max-size MAX_SIZE] [--no-ocr]

PDF-to-Text Splitter with OCR - Extract text from PDFs for AI training

optional arguments:
  -h, --help                  show this help message and exit
  --drop-folder DROP_FOLDER   Path to folder where PDFs will be dropped
  --complete-folder COMPLETE_FOLDER
                              Path to folder where split text files will be stored
  --original-folder ORIGINAL_FOLDER
                              Path to folder where original PDFs will be moved
  --max-size MAX_SIZE         Maximum size in MB for PDF chunks before conversion to text (default: 27)
  --no-ocr                    Disable OCR for text extraction
```

### Examples:

```bash
# Change maximum chunk size to 15MB
python pdf_splitter.py --max-size 15

# Use custom folders
python pdf_splitter.py --drop-folder "D:\Documents\PDFs" --complete-folder "D:\AI-Training-Data"

# Disable OCR (faster but won't work for scanned documents)
python pdf_splitter.py --no-ocr
```

---

## 📊 Performance Expectations

| Original PDF Size | Processing Time | Output Files | Notes |
|------------------:|----------------:|:------------:|:------|
| 5MB               | 30-60 seconds   | 1 file       | Fast for native text |
| 25MB              | 1-2 minutes     | 1-2 files    | OCR may increase time |
| 50MB              | 2-4 minutes     | 2-3 files    | Good balance of speed/quality |
| 100MB             | 5-10 minutes    | 4-5 files    | OCR becomes significant factor |
| 250MB             | 15-30 minutes   | 8-12 files   | High memory usage |
| 500MB             | 30-60 minutes   | 15-25 files  | Consider running overnight |
| 1GB+              | 1-3 hours       | 30-50 files  | Very large PDFs require patience |

**Note**: OCR processing significantly impacts performance. Times are estimates for documents with mixed text/images on a modern system with 8GB RAM.

---

## ❓ Troubleshooting

### Common Issues and Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| **"OCR error"** | Tesseract not installed or not in PATH | Ensure Tesseract is installed and in your system PATH |
| **"Cannot convert PDF to image"** | Poppler missing or not in PATH | Verify Poppler installation and PATH settings |
| **No text extracted** | Poor quality scanned document | Try increasing image resolution in the code (find `convert_from_path` function) |
| **Processing very slow** | Large PDF with many images | Be patient with OCR - consider using `--no-ocr` flag if text is already selectable |
| **Script won't start** | Python environment issues | Check if virtual environment is properly set up with `pip list` |
| **Files not being detected** | Background service not running | Run the start script manually to see any error messages |

### Advanced Troubleshooting

1. **Check Tesseract Installation**:
   ```bash
   # Windows (Command Prompt)
   tesseract --version
   
   # macOS/Linux
   tesseract --version
   ```

2. **Verify Python Dependencies**:
   ```bash
   # Activate virtual environment first
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   
   # Then check installed packages
   pip list
   ```

3. **Testing OCR Directly**:
   ```python
   # Quick test script to verify OCR is working
   from PIL import Image
   import pytesseract
   print(pytesseract.get_tesseract_version())
   ```

4. **Enable Debug Logging**:
   Add the `--debug` flag when running the script for verbose logs:
   ```bash
   python pdf_splitter.py --debug
   ```

---

## 🔄 Maintenance

### Updating the Tool

```bash
# Pull the latest version
git pull origin main

# Reinstall dependencies
python setup.py
```

### Cleaning Up

If you need to free up disk space, you can safely delete the following:
- Files in the `Original PDF` folder after confirming text extraction is good
- Individual text file folders in `Split Drop Complete` once you've used them for training

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve the tool:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Areas where we'd especially appreciate contributions:
- Improved OCR quality
- Support for more languages
- Performance optimizations
- UI improvements

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

---

## 💬 Support & Contact

Need help? Have questions?

- Create an issue on GitHub: [Report an Issue](https://github.com/Saphyre-Solutions-LLC/-PDF-Chunker-AI-Training-File-Uploader-Without-Limits/issues/new)
- Contact the team: Tim.Spurlin@SaphyreSolutions.com

---

## 🌟 What's Next

Future development plans include:
- GUI interface for easier monitoring
- More OCR language support
- Additional output formats
- Batch processing improvements
- Cloud storage integration

Keep checking back for updates!

---

**Created by [Tim Spurlin](https://github.com/Tim-Spurlin)** - Making AI training data preparation effortless
