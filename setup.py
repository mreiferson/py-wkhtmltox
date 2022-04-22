from setuptools import setup, Extension

setup(ext_modules=[
    Extension(name="wkhtmltox",
              sources=["wkhtmltox.c"],
              libraries=["wkhtmltox"])])
