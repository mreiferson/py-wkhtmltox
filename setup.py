from distutils.core import setup
from distutils.extension import Extension

setup(
    name="py-wkhtmltox",
    version="0.2",
    description="Python bindings for libwkhtmltox",
    author="Matt Reiferson",
    author_email="mreiferson@gmail.com",
    url="http://github.com/mreiferson/py-wkhtmltox",
    ext_modules = [Extension("wkhtmltox", ["wkhtmltox.c"], libraries=["wkhtmltox"])]
)
