#!/usr/bin/env python3
"""
Test script for PDF Abstract Extractor

This script demonstrates how to use the PDFAbstractExtractor class
and provides a simple way to test the functionality.
"""

import sys
from pathlib import Path
from pdf_abstract_extractor import PDFAbstractExtractor


def test_extractor():
    """Test the PDF abstract extractor with a sample PDF."""
    
    # Check if a PDF file was provided as command line argument
    if len(sys.argv) > 1:
        input_pdf = sys.argv[1]
    else:
        print("Usage: python test_extractor.py <input_pdf>")
        print("Example: python test_extractor.py sample.pdf")
        return
    
    # Check if input file exists
    if not Path(input_pdf).exists():
        print(f"Error: File '{input_pdf}' not found.")
        return
    
    try:
        # Create extractor instance
        extractor = PDFAbstractExtractor()
        
        # Process the PDF
        print(f"Processing PDF: {input_pdf}")
        output_path = extractor.process_pdf(input_pdf)
        
        print(f"✓ Successfully created abstract PDF: {output_path}")
        
        # Show file size information
        input_size = Path(input_pdf).stat().st_size / 1024  # KB
        output_size = Path(output_path).stat().st_size / 1024  # KB
        
        print(f"Input file size: {input_size:.1f} KB")
        print(f"Output file size: {output_size:.1f} KB")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    test_extractor()