# Create setup_autorun.sh
cat > setup_autorun.sh << 'EOF'
#!/bin/bash
echo "Setting up PDF Splitter to run automatically..."

# Determine OS type
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    STARTUP_DIR="$HOME/Library/LaunchAgents"
    mkdir -p "$STARTUP_DIR"
    
    # Create plist file
    cat > "$STARTUP_DIR/com.saphyresolutions.pdfsplitter.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.saphyresolutions.pdfsplitter</string>
    <key>ProgramArguments</key>
    <array>
        <string>$(pwd)/start_pdf_splitter.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$(pwd)</string>
</dict>
</plist>
PLIST
    
    # Load the agent
    launchctl load "$STARTUP_DIR/com.saphyresolutions.pdfsplitter.plist"
    echo "Created startup item. PDF Splitter will now run automatically when you log in."
    
else
    # Linux
    STARTUP_DIR="$HOME/.config/autostart"
    mkdir -p "$STARTUP_DIR"
    
    # Create desktop entry
    cat > "$STARTUP_DIR/pdfsplitter.desktop" << DESKTOP
[Desktop Entry]
Type=Application
Name=PDF Splitter
Exec=$(pwd)/start_pdf_splitter.sh
Terminal=false
X-GNOME-Autostart-enabled=true
DESKTOP
    
    echo "Created startup item. PDF Splitter will now run automatically when you log in."
fi

# Start the script now
$(pwd)/start_pdf_splitter.sh &

echo "PDF Splitter is now running."
EOF

# Make the shell script executable
chmod +x setup_autorun.sh