Python bindings for the fabulous `libwkhtmltox` using Cython

Special thanks to antialize for creating [wkhtmltopdf](http://wkhtmltopdf.org)

For parameters and settings (for users familiar with the command line utility) see:

    http://wkhtmltopdf.org/libwkhtmltox/pagesettings.html

### Installation

    $ python setup.py install

Tested on:

 * Mac OSX 10.6.4 Snow Leopard, Python 2.6.1 (32-bit and 64-bit)
 * CentOS 5.5, Python 2.6.4 (32-bit)

### Pre-requisites on all platforms:

 * you need `libwkhtmltox.*` somewhere in your LD path (`/usr/local/lib`)
 * you need the directory `include/wkhtmltox` from `wkhtmltopdf` somewhere on your include path (`/usr/local/include`)

### OSX Notes
If compiling for OSX (64-bit Python/libwkhtmltox only), until [this bug](http://bugreports.qt-project.org/browse/QTBUG-5952) is fixed you need the `qt_menu.nib` directory from the QT source tree in the same directory as your `libwkhtmltox.*` library files.

### Cython
If you want to re-generate C source (or have made changes to the Cython template file, .pyx) you need Cython (tested with 0.13):

    $ easy_install cython