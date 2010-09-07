import wkhtmltox

pdf = wkhtmltox.Pdf()
pdf.set_global_setting('out', 'test.pdf')
pdf.set_object_setting('path', 'http://www.google.com')
pdf.convert()