#!/bin/bash

# PDF Abstract Extractor Setup Script
# This script helps set up the environment for the PDF Abstract Extractor

echo "PDF Abstract Extractor - Setup Script"
echo "===================================="

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 found: $(python3 --version)"
else
    echo "✗ Python 3 not found. Please install Python 3.6 or higher."
    exit 1
fi

# Function to install dependencies
install_dependencies() {
    echo "Installing dependencies..."
    
    # Try different installation methods
    if command -v pip3 &> /dev/null; then
        echo "Using pip3 to install dependencies..."
        pip3 install PyMuPDF reportlab
    elif command -v pip &> /dev/null; then
        echo "Using pip to install dependencies..."
        pip install PyMuPDF reportlab
    else
        echo "pip not found. Trying to install via system packages..."
        
        # Try to install system packages (requires sudo)
        if command -v sudo &> /dev/null; then
            echo "Attempting to install system packages (requires sudo)..."
            sudo apt update
            sudo apt install -y python3-pymupdf python3-reportlab
        else
            echo "sudo not available. Please install dependencies manually:"
            echo "  pip install PyMuPDF reportlab"
            echo "  or"
            echo "  apt install python3-pymupdf python3-reportlab"
        fi
    fi
}

# Function to create virtual environment
create_venv() {
    echo "Creating virtual environment..."
    
    if command -v python3 -m venv &> /dev/null; then
        python3 -m venv venv
        echo "✓ Virtual environment created: venv/"
        echo "To activate: source venv/bin/activate"
        echo "Then install dependencies: pip install -r requirements.txt"
    else
        echo "✗ python3-venv not available. Please install it:"
        echo "  apt install python3-venv"
    fi
}

# Function to test the installation
test_installation() {
    echo "Testing installation..."
    
    python3 -c "
import sys
try:
    import fitz
    print('✓ PyMuPDF installed successfully')
except ImportError:
    print('✗ PyMuPDF not installed')
    sys.exit(1)

try:
    from reportlab.lib.pagesizes import A4
    print('✓ reportlab installed successfully')
except ImportError:
    print('✗ reportlab not installed')
    sys.exit(1)

print('✓ All dependencies are ready!')
"

    if [ $? -eq 0 ]; then
        echo ""
        echo "Setup completed successfully!"
        echo "You can now use the PDF Abstract Extractor:"
        echo "  python3 pdf_abstract_extractor.py input.pdf"
    else
        echo ""
        echo "Setup incomplete. Please install dependencies manually."
    fi
}

# Main setup process
echo "Choose installation method:"
echo "1. Install dependencies globally (requires sudo)"
echo "2. Create virtual environment"
echo "3. Test current installation"
echo "4. Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        install_dependencies
        test_installation
        ;;
    2)
        create_venv
        ;;
    3)
        test_installation
        ;;
    4)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac