# Create start_pdf_splitter.bat
cat > start_pdf_splitter.bat << 'EOF'
@echo off
echo Starting PDF Splitter...
start "PDF Splitter" /MIN "%~dp0venv\Scripts\pythonw.exe" "%~dp0pdf_splitter.py"
echo PDF Splitter is now running in the background.
EOF