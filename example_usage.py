#!/usr/bin/env python3
"""
Example usage of PDF Abstract Extractor

This script demonstrates various ways to use the PDFAbstractExtractor class
for different use cases.
"""

import os
from pathlib import Path
from pdf_abstract_extractor import PDFAbstractExtractor


def example_basic_usage():
    """Basic usage example."""
    print("=== Basic Usage Example ===")
    
    # Create extractor instance
    extractor = PDFAbstractExtractor()
    
    # Example: Process a PDF and get the output path
    try:
        # Replace with your actual PDF file
        input_pdf = "sample.pdf"
        
        if Path(input_pdf).exists():
            output_path = extractor.process_pdf(input_pdf)
            print(f"Abstract PDF created: {output_path}")
        else:
            print(f"Sample PDF '{input_pdf}' not found. Please provide a valid PDF file.")
            
    except Exception as e:
        print(f"Error: {e}")


def example_custom_output():
    """Example with custom output path."""
    print("\n=== Custom Output Example ===")
    
    extractor = PDFAbstractExtractor()
    
    try:
        input_pdf = "sample.pdf"
        custom_output = "my_abstract.pdf"
        
        if Path(input_pdf).exists():
            output_path = extractor.process_pdf(input_pdf, custom_output)
            print(f"Abstract PDF created with custom name: {output_path}")
        else:
            print(f"Sample PDF '{input_pdf}' not found.")
            
    except Exception as e:
        print(f"Error: {e}")


def example_batch_processing():
    """Example of processing multiple PDFs in a directory."""
    print("\n=== Batch Processing Example ===")
    
    extractor = PDFAbstractExtractor()
    
    # Directory containing PDFs
    pdf_directory = "pdfs"
    
    if not Path(pdf_directory).exists():
        print(f"Directory '{pdf_directory}' not found. Creating example structure...")
        Path(pdf_directory).mkdir(exist_ok=True)
        print(f"Created directory '{pdf_directory}'. Please add PDF files to it.")
        return
    
    # Find all PDF files in the directory
    pdf_files = list(Path(pdf_directory).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in '{pdf_directory}' directory.")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process:")
    
    for pdf_file in pdf_files:
        try:
            print(f"\nProcessing: {pdf_file.name}")
            output_path = extractor.process_pdf(str(pdf_file))
            print(f"✓ Created: {Path(output_path).name}")
            
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {e}")


def example_extract_text_only():
    """Example of extracting text without creating PDF."""
    print("\n=== Text Extraction Example ===")
    
    extractor = PDFAbstractExtractor()
    
    try:
        input_pdf = "sample.pdf"
        
        if Path(input_pdf).exists():
            # Extract text from PDF
            text = extractor.extract_text_from_pdf(input_pdf)
            print(f"Extracted {len(text)} characters from PDF")
            
            # Find abstract in text
            abstract = extractor.find_abstract(text)
            
            if abstract:
                print(f"Found abstract ({len(abstract)} characters):")
                print("-" * 50)
                print(abstract[:200] + "..." if len(abstract) > 200 else abstract)
                print("-" * 50)
            else:
                print("No abstract found in the text.")
        else:
            print(f"Sample PDF '{input_pdf}' not found.")
            
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all examples."""
    print("PDF Abstract Extractor - Usage Examples")
    print("=" * 50)
    
    # Run examples
    example_basic_usage()
    example_custom_output()
    example_batch_processing()
    example_extract_text_only()
    
    print("\n" + "=" * 50)
    print("Examples completed. Check the generated files!")


if __name__ == "__main__":
    main()