#
# CryptoMiniSat
#
# Copyright (c) 2009-2017, Mate Soos. All rights reserved.
# Copyright (c) 2017, Pierre Vignet
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import sys
import os
import platform
from distutils.core import setup, Extension
from distutils import sysconfig
from distutils.cmd import Command

__PACKAGE_VERSION__ = "0.2.0"
__LIBRARY_VERSION__ = "5.6.8"
os.environ["CC"] = "/usr/bin/cc"
os.environ["CXX"] = "/usr/bin/c++"

cconf = """-Wno-unused-result -Wsign-compare -DNDEBUG -g -fwrapv -O2 -Wall -g   -fstack-protector-strong -Wformat -Werror=format-security  -g -fwrapv -O2   """.split(" ")
is_apple = """"""


def cleanup(dat):
    ret = []
    for elem in dat:
        elem = elem.strip()
        #if is_apple != "" and "-ldl" in elem:
            #continue
        if elem != "" and not "flto" in elem:
            ret.append(elem)

    return ret

cconf = cleanup(cconf)
# print "Extra C flags from python-config:", cconf


def _init_posix(init):
    """
    Forces g++ instead of gcc on most systems
    credits to eric jones (eric@enthought.com) (found at Google Groups)
    """
    def wrapper():
        init()

        config_vars = sysconfig.get_config_vars()  # by reference
        if config_vars["MACHDEP"].startswith("sun"):
            # Sun needs forced gcc/g++ compilation
            config_vars['CC'] = 'gcc'
            config_vars['CXX'] = 'g++'

        config_vars['CFLAGS'] = '-g -W -Wall -Wno-deprecated -std=c++11'
        config_vars['OPT'] = '-g -W -Wall -Wno-deprecated -std=c++11'

    return wrapper

sysconfig._init_posix = _init_posix(sysconfig._init_posix)


class TestCommand(Command):
    """Call tests with the custom 'python setup.py test' command."""

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):

        import os
        import glob
        print("our CWD is:", os.getcwd(), "files here: ", glob.glob("*"))
        sys.path.append(os.getcwd())
        path2 = os.path.join(os.getcwd(), "..")
        path2 = os.path.join(path2, "lib")
        path2 = os.path.normpath(path2)
        print("path2 is:", path2)
        sys.path.append(path2)
        print("our sys.path is", sys.path)

        import tests as tp
        return tp.run()


__version__ = '5.6.8'

# needed because Mac doesn't make use of runtime_library_dirs
extra_link_args = []
if platform.system() == 'Darwin':
    extra_link_args.append('-Wl,-rpath,'+"/usr/local/lib")

if platform.system() == 'Windows':
    libname = "cryptominisat5win"
else:
    libname = "cryptominisat5"

modules = dict(
    name = "pycryptosat",
    sources = ["/home/alephnoell/quabs/build/libsolve/src/cmsat-prefix/src/cmsat-build/pycryptosat/src/pycryptosat.cpp"],
    define_macros = [('LIBRARY_VERSION', '"' + __LIBRARY_VERSION__ + '"')],
    extra_compile_args = cconf + ['-I/home/alephnoell/quabs/build/libsolve/src/cmsat-prefix/src/cmsat', '-I/home/alephnoell/quabs/build/libsolve/src/cmsat-prefix/src/cmsat-build/cmsat5-src'],
    extra_link_args = extra_link_args,
    language = "c++",
    library_dirs=['.', '/home/alephnoell/quabs/build/libsolve/src/cmsat-prefix/src/cmsat-build/lib', '/home/alephnoell/quabs/build/libsolve/src/cmsat-prefix/src/cmsat-build/lib/Release'],
    runtime_library_dirs=['/usr/local/lib'],
    libraries = [libname]
)

if platform.system() == 'Windows':
    del modules['runtime_library_dirs']

setup(
    name = "pycryptosat",
    version = __PACKAGE_VERSION__,
    author = "Mate Soos",
    author_email = "soos.mate@gmail.com",
    url = "https://github.com/msoos/cryptominisat",
    license = "MIT",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: C++",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
    ext_modules =  [Extension(**modules)],
    description = "Bindings to CryptoMiniSat {} (a SAT solver)".\
        format(__LIBRARY_VERSION__),
#    py_modules = ['pycryptosat'],
    long_description = open('/home/alephnoell/quabs/build/libsolve/src/cmsat-prefix/src/cmsat/python/README.rst').read(),
    cmdclass={
        'test': TestCommand
    }

)
