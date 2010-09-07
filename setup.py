from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import distutils.sysconfig as ds
config = ds.get_config_vars()

setup(
    name="py-wkhtmltox",
    version="0.0.1",
    description="Python bindings for libwkhtmltox",
    author="Matt Reiferson",
    author_email="mreiferson@gmail.com",
    url="http://github.com/mreiferson/py-wkhtmltox",
    cmdclass = {"build_ext": build_ext},
    ext_modules = [Extension("wkhtmltox", ["wkhtmltox.pyx"], libraries=["wkhtmltox"])]
)
