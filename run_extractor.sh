#!/bin/bash
"""
Convenience script to run the PDF Abstract Extractor

This script automatically activates the virtual environment and runs the extractor.
Usage: ./run_extractor.sh input.pdf [output.pdf]
"""

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Error: Virtual environment not found at $SCRIPT_DIR/venv"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Check if input file is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <input_pdf> [output_pdf]"
    echo "Example: $0 research_paper.pdf"
    echo "Example: $0 research_paper.pdf abstract_output.pdf"
    exit 1
fi

# Run the extractor
if [ $# -eq 1 ]; then
    # No output file specified
    python "$SCRIPT_DIR/pdf_abstract_extractor.py" "$1"
else
    # Output file specified
    python "$SCRIPT_DIR/pdf_abstract_extractor.py" "$1" -o "$2"
fi