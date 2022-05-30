import os

from .utilities import (
    PDF, assert_images_are_identical, assert_pdf_objects_are_identical
)


def test_convert_to_jpg():
    import wkhtmltox
    img = wkhtmltox.Image()
    test_file = b'test.jpg'
    img.set_global_setting(b'out', test_file)
    img.set_global_setting(b'in', b'tests/simple.html')
    img.convert()

    assert os.path.isfile(test_file)
    try:
        with open('tests/simple.jpg', 'rb') as org, open(test_file, 'rb') as new:
            assert assert_images_are_identical(
                'test_image', org.read(), new.read(), 'jpg')
    finally:
        os.remove(test_file)


def test_convert_to_pdf():
    import wkhtmltox
    pdf = wkhtmltox.Pdf()
    test_file = b'test.pdf'
    pdf.set_global_setting(b'out', test_file)
    pdf.add_page({b'page': b'tests/simple.html'})
    pdf.convert()

    assert os.path.isfile(test_file)
    try:
        with open('tests/simple.pdf', 'rb') as org, open(test_file, 'rb') as new:
            assert_pdf_objects_are_identical(
                'test_pdf',
                PDF.from_bytes(org.read()),
                PDF.from_bytes(new.read())
            )
    finally:
        os.remove(test_file)
