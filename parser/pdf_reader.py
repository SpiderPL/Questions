import PyPDF2

def import_data_from_file(file_name):
    """Read file"""
    pdf_file = open(file_name, "rb")
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    lines = []
    for page_now in range(read_pdf.getNumPages()):
        page_content = read_pdf.getPage(page_now).extractText()
        lines.extend(page_content.splitlines())
    return lines