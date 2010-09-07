from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import distutils.sysconfig as ds
config = ds.get_config_vars()
#config['ARCHFLAGS'] = '-arch i386'
#config['LDFLAGS'] = '-Wl,-F. -arch i386'

setup(
  cmdclass = {"build_ext": build_ext},
  ext_modules = [Extension("wkhtmltox", ["wkhtmltox.pyx"], libraries=["wkhtmltox"])]
)
