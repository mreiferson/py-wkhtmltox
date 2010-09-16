import wkhtmltox

pdf = wkhtmltox.Pdf()
pdf.set_global_setting('out', 'test.pdf')
pdf.add_page({'page': 'http://www.visionaryrenesis.com'})
pdf.add_page({'page': 'http://www.google.com'})
pdf.convert()
