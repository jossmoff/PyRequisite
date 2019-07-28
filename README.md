
# PyRequisite

<a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.6-green.svg"></a>
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**PyRequisite** allows you to find project prerequisites for Python  modules when you forget to start a virtual enviroment.

## Installation

```bash
# Clone the repo
joss@moff:~$: git clone https://github.com/JossMoff/PyRequisite.git

# Change the working directory to PyRequisite
joss@moff:~$: cd PyRequisite

# Install PyRequisite onto your system
joss@moff:~$: python3 setup.py install
```

> Sometimes the last step will require sudo as you might not has write access to /usr/local/lib/python3.6/dist-packages/

## Usage

```bash
joss@moff:~$ PyRequisite --help
usage: PyRequisite [-h] [-f] [-d] [-o OUTPUT] libraries

PyRequisite: Find library prerequisites for Python

positional arguments:
  libraries             The set of top-level libraries in your
                        project.

optional arguments:
  -h, --help            show this help message and exit
  -f, --file            Specifies whethers libraries is a file.
  -d, --directory       Specifies whethers libraries is a directory to be
                        searched.
  -o OUTPUT, --output OUTPUT
                        Specifies the output name of the file if
                        you wish to output it to one.
```

## Usage with no flags

[![asciicast](https://asciinema.org/a/IaAJlp9gTbm7TNNrCBkHSohtK.svg)](https://asciinema.org/a/IaAJlp9gTbm7TNNrCBkHSohtK)

## Usage with file flag

[![asciicast](https://asciinema.org/a/12uU6o3QjixQcQCG6hmxZfC3a.svg)](https://asciinema.org/a/12uU6o3QjixQcQCG6hmxZfC3a)

## Usage with directory flag

[![asciicast](https://asciinema.org/a/drL0MGbStHCctYs1L2rerV02n.svg)](https://asciinema.org/a/drL0MGbStHCctYs1L2rerV02n)

## Further Improvements

How I plan to extend the quick project:
 -🍎Provide OS X support
 -🐧Provide Windows Support from old code.
 -💻Add extra terminal features
