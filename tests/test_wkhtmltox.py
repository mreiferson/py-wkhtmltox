# -*- coding: utf-8 -*-

import os
import re

from .utilities import (
    PDF, assert_images_are_identical, assert_pdf_objects_are_identical)


def test_image():
    import wkhtmltox
    img = wkhtmltox.Image()
    test_filename = b'test.jpg'
    img.set_global_setting(b'out', test_filename)
    img.set_global_setting(b'in', b'tests/simple.html')
    img.convert()

    assert os.path.isfile(test_filename)
    try:
        with open('tests/simple.jpg', 'rb') as org, open(test_filename, 'rb') as new:
            assert assert_images_are_identical(
                'test_image', org.read(), new.read(), 'jpg')
    finally:
        os.remove(test_filename)


def test_pdf():
    import wkhtmltox
    pdf = wkhtmltox.Pdf()
    test_filename = b'test.pdf'
    pdf.set_global_setting(b'out', test_filename)
    pdf.add_page({b'page': b'tests/simple.html'})
    pdf.convert()

    assert os.path.isfile(test_filename)
    try:
        with open('tests/simple.pdf', 'rb') as org, open(test_filename, 'rb') as new:
            assert_pdf_objects_are_identical(
                'test_pdf',
                PDF.from_bytes(org.read()), PDF.from_bytes(new.read())
            )
    finally:
        os.remove(test_filename)
