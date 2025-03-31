# PDF Splitter

This tool automatically splits PDFs into smaller files (max 27MB) when they are dropped into the "PDF Split Drop" folder.

## Setup

1. Make sure you have Python installed
2. Run `setup.py` to create the virtual environment and install dependencies
3. Run `setup_autorun.bat` to make the script run automatically on startup

## Usage

Simply drop any PDF file into the "PDF Split Drop" folder. The tool will:

1. Automatically detect the new PDF
2. Split it into files under 27MB each
3. Create a new folder with a name based on the PDF content
4. Name each split with a number and content-relevant keywords
5. Move the original PDF to the "Original PDF" folder

All split files will be in the "Split Drop Complete" folder.

## Manual Start

If you don't want the tool to run automatically, you can start it manually by running `start_pdf_splitter.bat`.
