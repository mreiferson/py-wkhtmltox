# py-wkhtmltopx
Python bindings for the fabulous `libwkhtmltox` using Cython

Special thanks to antialize for creating [wkhtmltopdf](http://wkhtmltopdf.org)

For parameters and settings (for users familiar with the command line utility)
see: [page settings](http://wkhtmltopdf.org/libwkhtmltox/pagesettings.html)

### Installation
```
pip install -U -r requirements/build.txt
python install -e .
```

Once installed, you can verify it works by running as yourself:
```
tox
```
Tested on:
 * Mac OSX 10.6.4 Snow Leopard, Python 2.6.1 (32-bit and 64-bit)
 * Linux, Python 2.6.18 and 3.4.10 (64-bit)
 * Windows 7, Python 2.7.6 (32-bit)

### Pre-requisites on all platforms:

 * you need `libwkhtmltox.*` somewhere in your LD path (`/usr/local/lib`)
 * you need the directory `include/wkhtmltox` from `wkhtmltopdf` somewhere on your include path (`/usr/local/include`)

### OSX Notes
If compiling for OSX (64-bit Python/libwkhtmltox only), until [this bug](http://bugreports.qt-project.org/browse/QTBUG-5952) is fixed you need the `qt_menu.nib` directory from the QT source tree in the same directory as your `libwkhtmltox.*` library files.

### Windows Notes

You will need Visual Studio 2008 ([VS2008 Express](http://go.microsoft.com/?linkid=7729279)
with [SP1](http://www.microsoft.com/en-us/download/details.aspx?id=10986) and latest updates
from Microsoft Update should work as well). Start a "Visual Studio 2008 Command Prompt" and
run the following (assuming that `wkhmltopdf` is installed in `C:\Program Files\wkhtmltopdf`:

    set INCLUDE=%INCLUDE%C:\Program Files\wkhtmltopdf\include;
    set LIB=%LIB%C:\Program Files\wkhtmltopdf\lib;
    python setup.py bdist_wininst

This would produce an installer in the `dist/` folder which you can install. You will need to
have `C:\Program Files\wkhtmltopdf\bin` in the path or copy `wkhtmltox.dll` along with the
extension.

### Cython
If you want to re-generate C source (or have made changes to the Cython template file, .pyx) you need Cython (tested with 0.29.24):
```
pip install -U Cython==0.29.24
```
