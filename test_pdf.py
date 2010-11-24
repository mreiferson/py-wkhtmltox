import wkhtmltox

pdf = wkhtmltox.Pdf()
pdf.set_global_setting('out', 'one.pdf')
pdf.add_page({'page': 'http://www.visionaryrenesis.com'})
pdf.add_page({'page': 'http://www.google.com'})
pdf.convert()

pdf = wkhtmltox.Pdf()
pdf.set_global_setting('out', 'two.pdf')
pdf.add_page({'page': 'http://www.tweakers.net'})
pdf.convert()
