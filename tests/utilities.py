# -*- coding: utf-8 -*-

import glob
import os
import subprocess
import tempfile
from io import BytesIO

import pytest
from PIL import Image, ImageChops

from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.lib.units import mm as pdf_mm


class ConversionFailed(Exception):
    pass


class PNGDocument(object):
    """Document storing just one PNF file representing just one page."""
    file_format = 'png'

    def __init__(self, content):
        self.content = content

    def get_bytes(self):
        return self.content

    def get_stream(self):
        return BytesIO(self.content)

    def get_pages_count(self):
        return 1


class PDF(object):
    """Scurri wrapper over low level pdf stream.
    """
    file_format = 'pdf'

    # All sizes use point unit.
    # Use this page https://docupub.com/pdfresize/ to find new size
    A4_SIZE = (595, 842)
    LANDSCAPE_A4_SIZE = (842, 595)

    LETTER_SIZE = (612, 792)
    LANDSCAPE_LETTER_SIZE = (792, 612)

    THERMAL_SIZE = (288, 432)
    LANDSCAPE_THERMAL_SIZE = (432, 288)

    FOUR_BY_EIGHT = (288, 576)

    A6_SIZE = (297, 420)
    LANDSCAPE_A6_SIZE = (420, 297)

    mm = pdf_mm

    def __init__(self, pdf):
        """Init.

        Arguments:
            pdf: File like stream object with pdf data. BytesIO is
                preferred.
        """
        self._pdf = pdf

    @classmethod
    def from_bytes(cls, buffer):
        if not isinstance(buffer, bytes):
            raise TypeError("Expected bytes, not %s" % type(buffer))
        return cls(pdf=BytesIO(buffer))

    def get_bytes(self):
        return self.get_stream().getvalue()

    def get_stream(self):
        return self._pdf

    def __str__(self):
        return self.get_bytes()

    @property
    def pdf(self):
        return self.get_stream()

    def _extract_pages_by_size(self, include=None, exclude=None):
        include = include or []
        exclude = exclude or []
        reader = PdfFileReader(self.get_stream())
        writer = PdfFileWriter()
        pages_count = reader.getNumPages()
        pages_extracted = 0
        for page_num in range(pages_count):
            page = reader.getPage(page_num)
            width, height = page.mediaBox.upperRight
            size = (min(width, height), max(width, height))
            if size in include:
                writer.addPage(page)
                pages_extracted += 1
            if exclude and size not in exclude:
                writer.addPage(page)
                pages_extracted += 1
        if not pages_extracted:
            return
        buffer = BytesIO()
        writer.write(buffer)
        return self.__class__(pdf=buffer)

    def extract_a4_pages(self):
        """Extracts all A4 or Letter pages from current PDF document.

        """
        return self._extract_pages_by_size([self.A4_SIZE, self.LETTER_SIZE])

    def extract_thermal_pages(self):
        """Extracts all 4x6 aka thermal pages from current PDF document
        """
        return self._extract_pages_by_size([self.THERMAL_SIZE])

    def extract_non_thermal_pages(self):
        return self._extract_pages_by_size(exclude=[self.THERMAL_SIZE])

    def get_pages_count(self):
        reader = PdfFileReader(self.get_stream())
        return reader.getNumPages()

    def get_all_sizes(self):
        """Returns all page sizes used in the current document"""
        reader = PdfFileReader(self.get_stream())
        sizes = set()
        for page_num in range(reader.getNumPages()):
            page = reader.getPage(page_num)
            width, height = page.mediaBox.upperRight
            size = (min(width, height), max(width, height))
            sizes.add(size)
        return sorted(sizes)

    def split(self):
        """Splits current PDF object into list of pdf objects with one page
        each.

        """
        pages = []
        reader = PdfFileReader(self.get_stream())
        for page_num in range(reader.getNumPages()):
            page = reader.getPage(page_num)
            writer = PdfFileWriter()
            writer.addPage(page)
            out = BytesIO()
            writer.write(out)
            pages.append(self.__class__(pdf=out))
        return pages


def run_command(command, cwd=None, shell=False, env=None,
                get_stderr=False):
    """
    Runs the given command in the project base directory, blocking execution
    until it completes

    Args:
        command (list): list of strings that are concatenated together for
            execution.
        cwd (basestring): Current working directory.
        shell (bool): Set to true if shell should be used.
        env (dict): Environment dictionary.
    Returns:
        bool: True if command ran successfully, False otherwise
    """
    print('Executing command {}'.format(command))
    process = subprocess.Popen(
        command, cwd=cwd, shell=shell, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # wait for the process to exit
    stdoutdata, stderrdata = process.communicate()
    is_success = process.returncode == 0
    if not is_success:
        print('Failed to execute command {} stdout={}; stderr={}'.format(
            command, stdoutdata, stderrdata))
    if get_stderr:
        return is_success, stderrdata
    return is_success


def store_images_diff(test_name, ref_png, png, extension='png'):
    diff = compare_images(ref_png, png)
    fname_pattern = "{}_{{}}.{{}}".format(test_name)
    buf = BytesIO()
    diff.save(buf, 'PNG')
    with open('/tmp/' + fname_pattern.format("diff", "png"), 'wb') as f:
        f.write(buf.getvalue())
    with open('/tmp/' + fname_pattern.format("ref", extension), 'wb') as f:
        f.write(ref_png)
    with open('/tmp/' + fname_pattern.format("generated", extension), 'wb') as f:
        f.write(png)
    return fname_pattern


def compare_images(reference_image, image):
    """
    Compare images.
    Args:
        reference_image (bytes): Reference image, what we expect
        image (bytes): Image we would like to test and compare to reference
            image.

    Returns:
        (bool, diff) True if images are the same, and difference image if
            images are different.

    """
    ref_img = Image.open(BytesIO(reference_image))
    img = Image.open(BytesIO(image))
    # Regression test
    diff = ImageChops.difference(ref_img, img)
    return diff


def are_images_identical(image1, image2):
    img1 = Image.open(BytesIO(image1))
    img2 = Image.open(BytesIO(image2))
    return list(img1.getdata()) == list(img2.getdata())


def pdf_to_png(pdf):
    """
    Uses Ghostscript command to convert the PDF data into multiple PNG files

    Args:
        pdf (sculib.pdf.types.PDF):

    Returns:
        list[PNGDocument]: Returns list of PNGDocument.

    """
    with tempfile.NamedTemporaryFile(suffix='.pdf') as temp_handle:
        temp_handle.write(pdf.get_bytes())
        # force flush to disk so conversion works correctly
        temp_handle.flush()
        os.fsync(temp_handle.file)
        return _convert(temp_handle.name)


def _convert(pdf_filename):

    png_count = '%03d'

    # Just generate temporary file name.
    output_handle = tempfile.NamedTemporaryFile(
        suffix='-{0}.png'.format(png_count), delete=True
    )
    output_filename = output_handle.name
    output_handle.close()

    # we assume 300 DPI for all PDF conversion output - leave it to user
    # to scale as needed
    command = ['gs', '-dBATCH', '-dNOPAUSE', '-sDEVICE=pnggray', '-r300',
               '-sOutputFile={0}'.format(output_filename), pdf_filename]
    success, stderr = run_command(command, get_stderr=True)

    if not success:
        raise ConversionFailed('Failed to convert PDF to PNG.')

    if stderr:
        print(
            'Errors during conversion from PDF to PNG using '
            'GhostScript: command - {} error - {}'.format(command, stderr)
        )

    png_glob = output_filename.replace(png_count, '*')
    output_files = [filename for filename in sorted(glob.iglob(png_glob))]
    if not len(output_files):
        raise ConversionFailed('Failed to convert PDF to PNG.')
    result = []
    for path in output_files:
        with open(path, "rb") as f:
            result.append(PNGDocument(f.read()))
        os.remove(path)
    return result


def assert_pdf_objects_are_identical(test_name, ref_pdf, pdf, fail=False):
    reference_pages = ref_pdf.split()
    actual_pages = pdf.split()

    # check if they have the same number of pages
    reference_pages_length = len(reference_pages)
    actual_pages_length = len(actual_pages)

    if not reference_pages_length == actual_pages_length:
        raise AssertionError(
            'PDF files differ in the number of pages. '
            'Reference PDF page number: {}, PDF page number: {}'.format(
                reference_pages_length, actual_pages_length
            )
        )

    # check page by page if a generated pdf file is
    # identical to a reference pdf file
    for ref_page, actual_page in zip(reference_pages, actual_pages):
        ref_png = pdf_to_png(ref_page)
        ref_png = ref_png[0].get_bytes()

        png = pdf_to_png(actual_page)
        png = png[0].get_bytes()

        ref_png_length = len(ref_png)
        png_length = len(png)

        if not ref_png_length == png_length:
            fname_pattern = store_images_diff(test_name, ref_png, png)
            raise AssertionError(
                'PNG files have different lengths. '
                'Reference PNG length: {}, PNG Length: {},'
                'regression: {}'.format(
                    ref_png_length, png_length,
                    fname_pattern.format("*", "png")
                )
            )

        same = are_images_identical(ref_png, png)
        if fail or not same:
            fname_pattern = store_images_diff(test_name, ref_png, png)
            raise AssertionError(
                "PDF to PNG conversion regression: /tmp/{}".format(
                    fname_pattern.format("*", "png"))
            )


def assert_images_are_identical(test_name, ref_img, img, extension='png'):
    same = are_images_identical(ref_img, img)
    if not same:
        ref_img = BytesIO(ref_img).getvalue()
        img = BytesIO(img).getvalue()
        fname_pattern = store_images_diff(test_name, ref_img, img, extension)
        pytest.fail(
            "PNG conversion regression: /tmp/{}".format(
                fname_pattern.format("*", extension))
        )
    return same
