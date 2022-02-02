import wkhtmltox

img = wkhtmltox.Image()
img.set_global_setting(b'out', b'test.jpg')
img.set_global_setting(b'in', b'http://www.google.com')
img.convert()
