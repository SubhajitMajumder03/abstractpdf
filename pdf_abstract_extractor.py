#!/usr/bin/env python3
"""
PDF Abstract Extractor

This script extracts the abstract content from a PDF file and saves it as a new PDF.
It uses pattern matching to identify abstract sections and creates a clean output PDF.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional, List, Tuple

try:
    import PyPDF2
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.colors import black
except ImportError as e:
    print(f"Required library not found: {e}")
    print("Please install required packages using: pip install -r requirements.txt")
    sys.exit(1)


class PDFAbstractExtractor:
    """Class to handle PDF abstract extraction and creation."""
    
    def __init__(self):
        # Common patterns for abstract sections
        self.abstract_patterns = [
            r'abstract[:\s]*(.+?)(?=\n\s*\n|\nkeywords?|\nintroduction|\n1\.|\nbackground)',
            r'summary[:\s]*(.+?)(?=\n\s*\n|\nkeywords?|\nintroduction|\n1\.|\nbackground)',
            r'overview[:\s]*(.+?)(?=\n\s*\n|\nkeywords?|\nintroduction|\n1\.|\nbackground)',
        ]
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract all text from PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                # Extract text from all pages (abstract is usually on first few pages)
                for page_num in range(min(3, len(pdf_reader.pages))):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")
    
    def find_abstract(self, text: str) -> Optional[str]:
        """Find and extract abstract content from text."""
        # Clean up text - remove extra whitespaces and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        text_lower = text.lower()
        
        # Try different abstract patterns
        for pattern in self.abstract_patterns:
            matches = re.search(pattern, text_lower, re.IGNORECASE | re.DOTALL)
            if matches:
                abstract_text = matches.group(1).strip()
                
                # Get the original case text
                start_pos = text_lower.find(abstract_text.lower())
                if start_pos != -1:
                    original_abstract = text[start_pos:start_pos + len(abstract_text)]
                    return self.clean_abstract_text(original_abstract)
        
        # If no pattern matches, try to find abstract by keywords
        return self.find_abstract_by_keywords(text)
    
    def find_abstract_by_keywords(self, text: str) -> Optional[str]:
        """Fallback method to find abstract using keyword search."""
        lines = text.split('\n')
        abstract_start = -1
        abstract_end = -1
        
        # Look for abstract start
        for i, line in enumerate(lines):
            if re.search(r'\babstract\b', line.lower()):
                abstract_start = i
                break
        
        if abstract_start == -1:
            return None
        
        # Look for abstract end (next section)
        end_keywords = ['keywords', 'introduction', 'background', '1.', 'i.']
        for i in range(abstract_start + 1, len(lines)):
            line_lower = lines[i].lower().strip()
            if any(keyword in line_lower for keyword in end_keywords):
                abstract_end = i
                break
        
        if abstract_end == -1:
            # If no end found, take next 10 lines or until empty line
            for i in range(abstract_start + 1, min(abstract_start + 11, len(lines))):
                if lines[i].strip() == '':
                    abstract_end = i
                    break
            else:
                abstract_end = min(abstract_start + 10, len(lines))
        
        # Extract abstract text
        abstract_lines = lines[abstract_start:abstract_end]
        abstract_text = ' '.join(abstract_lines).strip()
        
        # Remove the word "abstract" from the beginning
        abstract_text = re.sub(r'^\s*abstract[:\s]*', '', abstract_text, flags=re.IGNORECASE)
        
        return self.clean_abstract_text(abstract_text) if abstract_text else None
    
    def clean_abstract_text(self, text: str) -> str:
        """Clean and format abstract text."""
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove common artifacts from PDF extraction
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\(\)\-\&]', '', text)
        
        # Ensure proper sentence formatting
        text = re.sub(r'\.(\w)', r'. \1', text)
        
        return text.strip()
    
    def create_abstract_pdf(self, abstract_text: str, output_path: str, title: str = "Extracted Abstract"):
        """Create a new PDF with the abstract content."""
        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Get styles
            styles = getSampleStyleSheet()
            
            # Create custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            
            abstract_style = ParagraphStyle(
                'AbstractText',
                parent=styles['Normal'],
                fontSize=11,
                leading=14,
                spaceAfter=12,
                alignment=4  # Justify alignment
            )
            
            # Build the story (content)
            story = []
            
            # Add title
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 12))
            
            # Add abstract header
            story.append(Paragraph("<b>Abstract</b>", styles['Heading2']))
            story.append(Spacer(1, 12))
            
            # Add abstract content
            story.append(Paragraph(abstract_text, abstract_style))
            
            # Build PDF
            doc.build(story)
            
        except Exception as e:
            raise Exception(f"Error creating PDF: {e}")
    
    def process_pdf(self, input_path: str, output_path: str) -> bool:
        """Main method to process PDF and extract abstract."""
        try:
            # Extract text from PDF
            print(f"Extracting text from: {input_path}")
            text = self.extract_text_from_pdf(input_path)
            
            if not text.strip():
                print("No text found in PDF")
                return False
            
            # Find abstract
            print("Searching for abstract content...")
            abstract = self.find_abstract(text)
            
            if not abstract:
                print("No abstract found in the PDF")
                return False
            
            print(f"Abstract found ({len(abstract)} characters)")
            print(f"Abstract preview: {abstract[:100]}...")
            
            # Create new PDF with abstract
            print(f"Creating abstract PDF: {output_path}")
            
            # Extract title from filename for the PDF
            input_name = Path(input_path).stem
            title = f"Abstract from {input_name}"
            
            self.create_abstract_pdf(abstract, output_path, title)
            
            print(f"Abstract PDF created successfully: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return False


def main():
    """Main function to handle command line arguments and execute extraction."""
    parser = argparse.ArgumentParser(
        description="Extract abstract from PDF and create a new PDF with the abstract content"
    )
    parser.add_argument(
        "input_pdf",
        help="Path to the input PDF file"
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output PDF file path (default: input_filename_abstract.pdf)"
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_pdf)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_pdf}' not found")
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.pdf':
        print(f"Error: Input file must be a PDF")
        sys.exit(1)
    
    # Determine output path
    if args.output:
        output_path = args.output
    else:
        output_path = input_path.parent / f"{input_path.stem}_abstract.pdf"
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Process PDF
    extractor = PDFAbstractExtractor()
    success = extractor.process_pdf(str(input_path), str(output_path))
    
    if success:
        print(f"\n✅ Successfully extracted abstract to: {output_path}")
    else:
        print("\n❌ Failed to extract abstract")
        sys.exit(1)


if __name__ == "__main__":
    main()