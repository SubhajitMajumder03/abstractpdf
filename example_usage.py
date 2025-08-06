#!/usr/bin/env python3
"""
Example usage of the PDF Abstract Extractor

This script demonstrates how to use the PDFAbstractExtractor class programmatically.
"""

from pdf_abstract_extractor import PDFAbstractExtractor
import sys
from pathlib import Path


def example_usage():
    """Example of using the PDF Abstract Extractor programmatically."""
    
    # Check if a PDF file was provided as argument
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <path_to_pdf>")
        print("Example: python example_usage.py research_paper.pdf")
        sys.exit(1)
    
    input_pdf = sys.argv[1]
    
    # Validate input file
    if not Path(input_pdf).exists():
        print(f"Error: File '{input_pdf}' not found")
        sys.exit(1)
    
    # Create extractor instance
    extractor = PDFAbstractExtractor()
    
    # Define output path
    output_pdf = f"{Path(input_pdf).stem}_abstract_example.pdf"
    
    print("=== PDF Abstract Extractor Example ===")
    print(f"Input PDF: {input_pdf}")
    print(f"Output PDF: {output_pdf}")
    print()
    
    try:
        # Extract text first (optional - for demonstration)
        print("1. Extracting text from PDF...")
        text = extractor.extract_text_from_pdf(input_pdf)
        print(f"   Extracted {len(text)} characters")
        
        # Find abstract
        print("2. Searching for abstract...")
        abstract = extractor.find_abstract(text)
        
        if abstract:
            print(f"   Abstract found: {len(abstract)} characters")
            print(f"   Preview: {abstract[:150]}...")
            
            # Create PDF with abstract
            print("3. Creating PDF with abstract...")
            extractor.create_abstract_pdf(
                abstract_text=abstract,
                output_path=output_pdf,
                title=f"Abstract from {Path(input_pdf).name}"
            )
            
            print(f"✅ Success! Abstract saved to: {output_pdf}")
            
        else:
            print("❌ No abstract found in the PDF")
            
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        sys.exit(1)


if __name__ == "__main__":
    example_usage()