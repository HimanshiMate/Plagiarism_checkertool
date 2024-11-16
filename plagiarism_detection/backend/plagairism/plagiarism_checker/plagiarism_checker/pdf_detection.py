import PyPDF2
from .text_detection import detect_text_plagiarism

# import PyPDF2

def extract_text_from_pdf(pdf_file):
    text = ''
    
    try:
        # Check if the input is a valid PDF file
        if not pdf_file.name.endswith('.pdf'):
            raise ValueError("The provided file is not a PDF.")
        
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        
        # Check if the PDF file is encrypted
        if pdf_reader.isEncrypted:
            # Attempt to decrypt with an empty password
            if not pdf_reader.decrypt(''):
                raise ValueError("The PDF file is encrypted and requires a password.")
        
        # Extract text from each page
        for page in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page].extract_text()
            if page_text:  # Only append if text extraction was successful
                text += page_text

    except PyPDF2.utils.PdfReadError:
        raise ValueError("Error reading PDF file. It may be corrupted or not a valid PDF.")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

    return text.strip()  # Return the extracted text, stripped of leading/trailing whitespace



def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page).extract_text()
    return text

def detect_pdf_plagiarism(pdf_file1, pdf_file2):
    text1 = extract_text_from_pdf(pdf_file1)
    text2 = extract_text_from_pdf(pdf_file2)
    return detect_text_plagiarism(text1, text2)
