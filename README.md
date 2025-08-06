# PDF Abstract Extractor

A Python script that extracts abstract content from PDF files and creates a new PDF containing only the abstract.

## Features

- **Intelligent Abstract Detection**: Uses multiple pattern matching strategies to find abstracts
- **Multiple Format Support**: Recognizes abstracts labeled as "Abstract", "Summary", or "Overview"
- **Clean Output**: Creates a well-formatted PDF with the extracted abstract
- **Fallback Methods**: Uses keyword-based search if pattern matching fails
- **Command Line Interface**: Easy to use from the command line

## Installation

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

**Note**: Make sure to activate the virtual environment before running the script:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Basic Usage
```bash
python pdf_abstract_extractor.py input_document.pdf
```
This will create `input_document_abstract.pdf` in the same directory.

### Custom Output Path
```bash
python pdf_abstract_extractor.py input_document.pdf -o /path/to/output_abstract.pdf
```

### Help
```bash
python pdf_abstract_extractor.py -h
```

### Convenience Script
For easier usage, you can use the provided shell script that automatically handles the virtual environment:
```bash
./run_extractor.sh input_document.pdf
./run_extractor.sh input_document.pdf custom_output.pdf
```

## How It Works

1. **Text Extraction**: Extracts text from the first 3 pages of the PDF (where abstracts are typically located)
2. **Pattern Matching**: Uses regex patterns to identify abstract sections
3. **Fallback Search**: If patterns fail, searches for keywords like "abstract", "summary", etc.
4. **Text Cleaning**: Removes artifacts and formats the text properly
5. **PDF Creation**: Generates a new, clean PDF with the abstract content

## Supported Abstract Formats

The script can detect abstracts in various formats:
- Traditional academic papers with "Abstract:" headers
- Documents with "Summary:" or "Overview:" sections
- Papers where abstracts are followed by keywords or introduction sections

## Requirements

- Python 3.6+
- PyPDF2 (for PDF reading)
- ReportLab (for PDF creation)

## Error Handling

The script includes comprehensive error handling for:
- Missing or invalid PDF files
- PDFs without extractable text
- Documents without detectable abstracts
- File I/O errors

## Example Output

The generated PDF will include:
- Document title (based on input filename)
- "Abstract" header
- Clean, formatted abstract text
- Professional layout with proper margins and typography

## Limitations

- Works best with text-based PDFs (not scanned images)
- Requires abstracts to be labeled or follow common academic formatting
- May not work with heavily formatted or complex layouts
- Currently processes only the first 3 pages of documents