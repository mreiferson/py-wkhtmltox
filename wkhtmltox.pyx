cdef extern from "wkhtmltox/pdf.h":
    int wkhtmltopdf_init(int use_graphics)

def my_pdf_init(int use_graphics):
    return wkhtmltopdf_init(use_graphics)