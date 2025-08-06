# PDF Abstract Extractor

A Python script that extracts abstract content from PDF files and creates a new PDF containing only the abstract content.

## Features

- Extracts text content from PDF files using PyMuPDF
- Identifies abstract content using multiple pattern matching strategies
- Creates a new PDF with the extracted abstract content
- Supports command-line usage with various options
- Handles different abstract formats and styles

## Requirements

- Python 3.6 or higher
- PyMuPDF (for PDF text extraction)
- reportlab (for PDF generation)

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install PyMuPDF reportlab
```

## Usage

### Command Line Usage

Basic usage:
```bash
python pdf_abstract_extractor.py input.pdf
```

Specify output file:
```bash
python pdf_abstract_extractor.py input.pdf -o output.pdf
```

Verbose output:
```bash
python pdf_abstract_extractor.py input.pdf -v
```

### Python Module Usage

You can also use the script as a Python module:

```python
from pdf_abstract_extractor import PDFAbstractExtractor

extractor = PDFAbstractExtractor()
output_path = extractor.process_pdf("input.pdf", "output.pdf")
print(f"Abstract PDF created: {output_path}")
```

## How It Works

1. **Text Extraction**: The script uses PyMuPDF to extract all text content from the input PDF
2. **Abstract Detection**: It searches for abstract content using multiple regex patterns:
   - "Abstract:", "ABSTRACT:", "Abstract"
   - "Summary:", "SUMMARY:", "Summary"
   - Falls back to the first substantial paragraph if no abstract is found
3. **PDF Generation**: Creates a new PDF using reportlab with proper formatting and styling

## Abstract Detection Patterns

The script looks for abstracts using these patterns:
- `abstract\s*[:.]?\s*(.*?)` (case insensitive)
- `summary\s*[:.]?\s*(.*?)` (case insensitive)
- Falls back to the first substantial paragraph (>100 characters) if no abstract is found

## Output

The generated PDF will contain:
- A centered title "Abstract"
- The extracted abstract text with proper formatting
- Clean typography and spacing

## Error Handling

The script handles various error conditions:
- Missing input file
- Non-PDF input files
- Missing abstract content
- Missing dependencies

## Examples

### Example 1: Basic Usage
```bash
python pdf_abstract_extractor.py research_paper.pdf
# Creates: research_paper_abstract.pdf
```

### Example 2: Custom Output
```bash
python pdf_abstract_extractor.py paper.pdf -o abstract_only.pdf
# Creates: abstract_only.pdf
```

### Example 3: Verbose Output
```bash
python pdf_abstract_extractor.py document.pdf -v
# Shows detailed progress information
```

## Limitations

- Works best with academic papers and research documents
- Abstract detection relies on common formatting patterns
- May not work well with scanned PDFs or heavily formatted documents
- Requires the PDF to have extractable text content

## Troubleshooting

### Common Issues

1. **"No abstract content found"**: The PDF might not have a clearly marked abstract or the text extraction failed
2. **Import errors**: Make sure all dependencies are installed
3. **File not found**: Check that the input PDF path is correct

### Debugging

Use the verbose flag to see detailed output:
```bash
python pdf_abstract_extractor.py input.pdf -v
```

## License

This script is provided as-is for educational and research purposes.