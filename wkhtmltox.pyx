cdef extern from "wkhtmltox/pdf.h":
    bint wkhtmltopdf_init(int use_graphics)

def pdf_init(int use_graphics):
    return wkhtmltopdf_init(use_graphics)