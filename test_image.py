import wkhtmltox

img = wkhtmltox.Image()
img.set_global_setting('out', 'test.jpg')
img.set_global_setting('in', 'http://www.google.com')
img.convert()
