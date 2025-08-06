#!/usr/bin/env python3
"""
Demo script for PDF Abstract Extractor

This script demonstrates the functionality without requiring actual PDF files.
It shows how the abstract detection and PDF generation work.
"""

import tempfile
import os
from pathlib import Path
from pdf_abstract_extractor import PDFAbstractExtractor


def create_sample_pdf():
    """Create a sample PDF with abstract content for demonstration."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        # Create a temporary PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            pdf_path = tmp_file.name
        
        # Create the PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=20,
            alignment=1
        )
        
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )
        
        # Sample content with abstract
        content = [
            ("Research Paper on Machine Learning", title_style),
            ("", body_style),
            ("Abstract: This paper presents a novel approach to machine learning that combines deep neural networks with traditional statistical methods. Our methodology demonstrates significant improvements in accuracy and computational efficiency across multiple benchmark datasets. The results show a 15% improvement in classification accuracy and a 30% reduction in training time compared to existing methods.", body_style),
            ("", body_style),
            ("1. Introduction", title_style),
            ("Machine learning has become an essential tool in modern data analysis. This paper explores the intersection of deep learning and statistical methods.", body_style),
            ("", body_style),
            ("2. Methodology", title_style),
            ("Our approach combines convolutional neural networks with Bayesian inference techniques to achieve better generalization.", body_style),
            ("", body_style),
            ("3. Results", title_style),
            ("Experimental results demonstrate the effectiveness of our proposed method across various datasets.", body_style),
        ]
        
        # Add content to story
        for text, style in content:
            story.append(Paragraph(text, style))
            story.append(Spacer(1, 12))
        
        # Build the PDF
        doc.build(story)
        
        return pdf_path
        
    except ImportError:
        print("reportlab not available. Cannot create sample PDF.")
        return None


def demo_abstract_detection():
    """Demonstrate abstract detection with sample text."""
    print("=== Abstract Detection Demo ===")
    
    extractor = PDFAbstractExtractor()
    
    # Sample text with different abstract formats
    sample_texts = [
        "Abstract: This is a sample abstract that demonstrates the extraction capabilities of our tool.",
        "ABSTRACT: Another example of abstract content that should be detected by the pattern matching.",
        "Summary: This summary section contains important information about the research findings.",
        "This is a regular paragraph without any abstract marker. It should not be detected as an abstract.",
    ]
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\nSample {i}:")
        print(f"Text: {text}")
        abstract = extractor.find_abstract(text)
        if abstract:
            print(f"✓ Abstract found: {abstract}")
        else:
            print("✗ No abstract detected")


def demo_pdf_generation():
    """Demonstrate PDF generation with sample abstract."""
    print("\n=== PDF Generation Demo ===")
    
    extractor = PDFAbstractExtractor()
    
    # Sample abstract text
    sample_abstract = """This research presents a comprehensive analysis of machine learning algorithms in the context of natural language processing. Our study examines the effectiveness of various neural network architectures for text classification tasks. The results demonstrate significant improvements in accuracy and processing speed compared to traditional methods. We also explore the implications of our findings for real-world applications in document analysis and information retrieval systems."""
    
    # Create output PDF
    output_path = "demo_abstract.pdf"
    
    try:
        extractor.create_abstract_pdf(sample_abstract, output_path, "Sample Abstract")
        print(f"✓ Demo PDF created: {output_path}")
        
        # Check file size
        if Path(output_path).exists():
            size = Path(output_path).stat().st_size / 1024  # KB
            print(f"File size: {size:.1f} KB")
        
    except Exception as e:
        print(f"✗ Error creating demo PDF: {e}")


def demo_full_process():
    """Demonstrate the full process with a sample PDF."""
    print("\n=== Full Process Demo ===")
    
    # Create sample PDF
    sample_pdf = create_sample_pdf()
    
    if sample_pdf and Path(sample_pdf).exists():
        print(f"✓ Sample PDF created: {sample_pdf}")
        
        try:
            extractor = PDFAbstractExtractor()
            
            # Process the sample PDF
            output_path = extractor.process_pdf(sample_pdf, "sample_abstract.pdf")
            print(f"✓ Abstract extracted and new PDF created: {output_path}")
            
            # Clean up sample PDF
            os.unlink(sample_pdf)
            print(f"✓ Cleaned up sample PDF")
            
        except Exception as e:
            print(f"✗ Error processing sample PDF: {e}")
            # Clean up on error
            if Path(sample_pdf).exists():
                os.unlink(sample_pdf)
    else:
        print("✗ Could not create sample PDF")


def main():
    """Run all demos."""
    print("PDF Abstract Extractor - Demo")
    print("=" * 40)
    
    # Run demos
    demo_abstract_detection()
    demo_pdf_generation()
    demo_full_process()
    
    print("\n" + "=" * 40)
    print("Demo completed!")
    print("\nTo use with your own PDFs:")
    print("  python3 pdf_abstract_extractor.py your_file.pdf")


if __name__ == "__main__":
    main()