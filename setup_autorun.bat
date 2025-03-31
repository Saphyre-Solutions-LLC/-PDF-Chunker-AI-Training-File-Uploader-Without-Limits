# Create setup_autorun.bat
cat > setup_autorun.bat << 'EOF'
@echo off
echo Setting up PDF Splitter to run automatically...

:: Create a shortcut in the startup folder
powershell "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\PDF Splitter.lnk'); $Shortcut.TargetPath = '%~dp0start_pdf_splitter.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Start PDF Splitter'; $Shortcut.Save()"

echo Created startup shortcut. PDF Splitter will now run automatically when you log in.

:: Start the script now
start "" "%~dp0start_pdf_splitter.bat"

echo PDF Splitter is now running.
pause
EOF