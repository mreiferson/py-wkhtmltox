# py-wkhtmltopx
Python bindings for the fabulous `libwkhtmltox` using Cython

Special thanks to antialize for creating [wkhtmltopdf](http://wkhtmltopdf.org)

For parameters and settings (for users familiar with the command line utility)
see: [page settings](http://wkhtmltopdf.org/libwkhtmltox/pagesettings.html)

### Installation
```
pip install -U -r requirements/build.txt
pip install -e .
```
`pip` can create `wkhtmltox.so` and the file conflicts with `tox` (run locally)
unless it's deleted. 
But don't be surprise when `tox` will fail. It is due to dynamic nature of HTML,
your local system can render HTML slightly different so content of converted
PDF will be ok, but not (byte by byte) 100% exactly the same all the time.

### Tests
Due to reason form previous section tests need be executed in container to secure
100% replicteable test environment:
```
docker-compose run tox
```
Note: It can take up to ~8 min for download and build docker container.

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
