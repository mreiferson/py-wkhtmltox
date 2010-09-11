import wkhtmltox

pdf = wkhtmltox.Pdf()
pdf.set_global_setting('out', 'test.pdf')
pdf.set_object_setting('page', 'http://www.google.com')
pdf.convert()
