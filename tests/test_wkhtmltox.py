import os
import re


def test_image():
    import wkhtmltox
    img = wkhtmltox.Image()
    test_filename = b'test.jpg'
    img.set_global_setting(b'out', test_filename)
    img.set_global_setting(b'in', b'google.html')
    img.convert()
    assert os.path.isfile(test_filename)
    with open('test_org.jpg', 'rb') as org, open(test_filename, 'rb') as new:
        original = org.read().decode('ISO-8859-1')
        generated = new.read().decode('ISO-8859-1')
    os.remove(test_filename)
    assert original == generated


def test_pdf():
    import wkhtmltox
    pdf = wkhtmltox.Pdf()
    test_filename = b'test.pdf'
    pdf.set_global_setting(b'out', test_filename)
    pdf.add_page({b'page': b'google.html'})
    pdf.convert()

    assert os.path.isfile(test_filename)
    with open('test_org.pdf', 'rb') as org, open(test_filename, 'rb') as new:
        original = org.read().decode('ISO-8859-1')
        generated = re.sub(r"CreationDate \(D:\d{14}\+\d{2}'00",
                           "CreationDate (D:20220426161454+02'00",
                           new.read().decode('ISO-8859-1'))
    os.remove(test_filename)
    assert original == generated
