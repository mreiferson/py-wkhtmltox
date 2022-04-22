import os

# import pytest


def test_image():
    import wkhtmltox
    img = wkhtmltox.Image()
    test_jpg = b'test.jpg'
    img.set_global_setting(b'out', test_jpg)
    img.set_global_setting(b'in', b'GentooLinux.html')
    img.convert()
    assert os.path.isfile(test_jpg)
    # with open('test1.jpg') as org:
    #     o = org.read()
    # with open('test.jpg') as new:
    #     n = new.read()
    # assert n == o
    os.remove(test_jpg)


def test_pdf():
    import wkhtmltox
    pdf = wkhtmltox.Pdf()
    one_pdf = b'one.pdf'
    pdf.set_global_setting(b'out', one_pdf)
    pdf.add_page({b'page': b'GentooLinux.html'})
    pdf.convert()
    assert os.path.isfile(one_pdf)
    # import difflib
    # with open('one1.pdf') as org:
    #     o = org.read()
    # with open('one.pdf') as new:
    #     n = new.read()
    # print(difflib.SequenceMatcher(a=n, b=o).ratio())
    # for a,b in zip(open('one.pdf').read(), open('one1.pdf').read()):
    #     if not a == b:
    #         print(a,b)
    os.remove(one_pdf)
