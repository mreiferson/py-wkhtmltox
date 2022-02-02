import wkhtmltox

pdf = wkhtmltox.Pdf()
pdf.set_global_setting(b'out', b'one.pdf')
pdf.add_page({b'page': b'http://www.visionaryrenesis.com'})
pdf.add_page({b'page': b'http://www.google.com'})
pdf.convert()

pdf = wkhtmltox.Pdf()
pdf.set_global_setting(b'out', b'two.pdf')
pdf.add_page({b'page': b'http://www.tweakers.net'})
pdf.convert()
