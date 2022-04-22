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
    with open('test_org.jpg') as test_org, open(test_filename) as new_jpg:
        original = test_org.read()
        generated = new_jpg.read()
    assert original == generated
    os.remove(test_filename)


def test_pdf():
    import wkhtmltox
    pdf = wkhtmltox.Pdf()
    test_filename = b'test.pdf'
    pdf.set_global_setting(b'out', test_filename)
    pdf.add_page({b'page': b'google.html'})
    pdf.convert()

    assert os.path.isfile(test_filename)
    with open('test_org.pdf') as test_org, open(test_filename) as new_pdf:
        original = test_org.read()
        generated = re.sub(r'CreationDate \(D:\d{14}\+',
                           'CreationDate (D:20220425172518+', new_pdf.read())
    assert original == generated
    os.remove(test_filename)
