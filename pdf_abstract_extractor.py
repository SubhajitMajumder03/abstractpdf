#!/usr/bin/env python3
"""
PDF Abstract Extractor

This script takes a PDF file and extracts abstract content, then creates a new PDF
containing only the abstract content.

Requirements:
- PyPDF2 or PyMuPDF for PDF processing
- reportlab for PDF generation
- re for text pattern matching
"""

import sys
import re
import argparse
from pathlib import Path
from typing import Optional, List

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    try:
        import PyPDF2
        PYMUPDF_AVAILABLE = False
    except ImportError:
        print("Error: Neither PyMuPDF nor PyPDF2 is installed.")
        print("Please install one of them:")
        print("  pip install PyMuPDF")
        print("  pip install PyPDF2")
        sys.exit(1)

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import black
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("Error: reportlab is not installed.")
    print("Please install it:")
    print("  pip install reportlab")
    sys.exit(1)


class PDFAbstractExtractor:
    """Extract abstract content from PDF files and create new PDFs."""
    
    def __init__(self):
        self.abstract_patterns = [
            r'abstract\s*[:.]?\s*(.*?)(?=\n\n|\n[A-Z]|\n\d|$)',
            r'ABSTRACT\s*[:.]?\s*(.*?)(?=\n\n|\n[A-Z]|\n\d|$)',
            r'Abstract\s*[:.]?\s*(.*?)(?=\n\n|\n[A-Z]|\n\d|$)',
            r'Summary\s*[:.]?\s*(.*?)(?=\n\n|\n[A-Z]|\n\d|$)',
            r'SUMMARY\s*[:.]?\s*(.*?)(?=\n\n|\n[A-Z]|\n\d|$)',
            r'Summary\s*[:.]?\s*(.*?)(?=\n\n|\n[A-Z]|\n\d|$)',
        ]
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF using PyMuPDF."""
        if not PYMUPDF_AVAILABLE:
            raise ImportError("PyMuPDF is required for text extraction")
        
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")
    
    def find_abstract(self, text: str) -> Optional[str]:
        """Find abstract content in the extracted text."""
        # Clean the text
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        # Try different patterns to find abstract
        for pattern in self.abstract_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
            if matches:
                abstract = matches[0].strip()
                if len(abstract) > 50:  # Ensure it's substantial
                    return abstract
        
        # If no abstract found with patterns, try to find first substantial paragraph
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if len(para) > 100 and not para.startswith(('©', 'Copyright', 'All rights reserved')):
                return para
        
        return None
    
    def create_abstract_pdf(self, abstract_text: str, output_path: str, title: str = "Abstract") -> None:
        """Create a new PDF containing the abstract content."""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("reportlab is required for PDF generation")
        
        # Create the PDF document
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=1  # Center alignment
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=0,  # Left alignment
            leftIndent=20,
            rightIndent=20
        )
        
        # Add title
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 20))
        
        # Add abstract text
        # Split into paragraphs for better formatting
        paragraphs = abstract_text.split('\n')
        for para in paragraphs:
            para = para.strip()
            if para:
                story.append(Paragraph(para, body_style))
                story.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(story)
    
    def process_pdf(self, input_path: str, output_path: Optional[str] = None) -> str:
        """Main method to process PDF and extract abstract."""
        input_file = Path(input_path)
        
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if not input_file.suffix.lower() == '.pdf':
            raise ValueError("Input file must be a PDF")
        
        # Set output path if not provided
        if output_path is None:
            output_path = input_file.parent / f"{input_file.stem}_abstract.pdf"
        
        # Extract text from PDF
        print(f"Extracting text from {input_file.name}...")
        text = self.extract_text_from_pdf(str(input_file))
        
        # Find abstract
        print("Searching for abstract content...")
        abstract = self.find_abstract(text)
        
        if abstract is None:
            raise ValueError("No abstract content found in the PDF")
        
        # Create new PDF with abstract
        print(f"Creating abstract PDF: {output_path}")
        self.create_abstract_pdf(abstract, str(output_path))
        
        return str(output_path)


def main():
    """Main function to handle command line arguments and run the extractor."""
    parser = argparse.ArgumentParser(
        description="Extract abstract content from PDF and create a new PDF with the abstract"
    )
    parser.add_argument(
        "input_pdf",
        help="Path to the input PDF file"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path for the output PDF file (default: input_abstract.pdf)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    try:
        extractor = PDFAbstractExtractor()
        output_path = extractor.process_pdf(args.input_pdf, args.output)
        
        if args.verbose:
            print(f"Successfully created abstract PDF: {output_path}")
        else:
            print(f"Abstract PDF created: {output_path}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()