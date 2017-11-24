# Magpie

A tool for converting project source code to and from a flat text file.

This script requires an installed *Python2* runtime to execute.


## Setup

1) Download the [`magpie.py`](#MAGPIE) script

2) Run `mv magpie.py magpie` to get rid of the extension

3) Run `chmod +x magpie` to make the script executable

4) Add the `magpie` script to your system's `$PATH`


## Use

**Note:** This script is only intended to work with plain text data, and may
have issues unpacking binary data. While an attempt is made to filter-out binary
data, it's probably best to ensure the root directory you are attempting to pack
only contains plaintext data. Issues may be encountered on *UTF-16* encoded
files.


To *pack* a project's source code, navigate to the directory above project's
root and execute the following command:

    magpie --pack {PROJECT_FOLDER} > {OUTPUT_FILE}.txt


To *unpack* a project's source code, navigate to the desired destination and
execute the following command:

    magpie --unpack {INPUT_FILE}.txt


## Development

After cloning the repository, to setup the virtual environment:

1) Enter the project's root directory

2) Execute `chmod +x ./bin/*.sh`

3) Execute `./bin/setup-env.sh`

4) Execute `source ./venv/bin/activate`

To run pylint on the project, execute: `./bin/run-linter.sh`


## License

**The MIT License**

Copyright 2017 David RC Dayton

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
