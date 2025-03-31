# Create start_pdf_splitter.sh
cat > start_pdf_splitter.sh << 'EOF'
#!/bin/bash
echo "Starting PDF Splitter..."

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Run the Python script
if [ -d "$SCRIPT_DIR/venv" ]; then
    # Use the virtual environment if it exists
    if [ -f "$SCRIPT_DIR/venv/bin/python" ]; then
        nohup "$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/pdf_splitter.py" > "$SCRIPT_DIR/pdf_splitter.log" 2>&1 &
    else
        echo "Virtual environment found but Python executable missing. Please run setup.py first."
        exit 1
    fi
else
    # Fall back to system Python
    nohup python3 "$SCRIPT_DIR/pdf_splitter.py" > "$SCRIPT_DIR/pdf_splitter.log" 2>&1 &
fi

echo "PDF Splitter is now running in the background. (PID: $!)"
EOF

# Make the shell script executable
chmod +x start_pdf_splitter.sh