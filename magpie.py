#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A tool for converting project source code to and from a flat text file."""

__version__ = "1.0.0"
__author__ = "David RC Dayton"
__copyright__ = "Copyright 2017"
__email__ = "david.rc.dayton@gmail.com"
__license__ = "MIT"

import os
import re
import sys

PACK_STR = '==> %s <==\n%s'
UNPACK_REGEX = re.compile('^==> .* <==')
SEPARATOR = '|'
TRIM_SIZE = 4
BLOCK_SIZE = 1024


def is_binary(file_path):
    """A naive method for determining if a file is binary or plain text. This
    is accomplished by searching for null characters in each block of the file.
    This method is prone to false positives, i.e. when dealing with UTF-16
    encoded files.

    Args:
        file_path: path of the file to check for binary-ness

    Returns:
        True if the file is probably binary, otherwise False
    """
    with open(file_path, 'rb') as input_file:
        while True:
            block = input_file.read(BLOCK_SIZE)
            if '\0' in block:
                return True
            if len(block) < BLOCK_SIZE:
                break
    return False


def list_files(file_path):
    """Recursively walk a root file path, and return a list of all files
    expected to be plain-text.

    Args:
        file_path: root path to recursively walk

    Returns:
        a list of (hopefully) plain-text files
    """
    out_files = []
    for root, _, files in os.walk(file_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            if not is_binary(full_path):
                out_files.append(full_path)
    return out_files


def format_header(file_path):
    """Format a relative path into a operating system agnostic representation of
    itself.

    Args:
        file_path: relative path

    Returns:
        string sutable for packing as a file header
    """
    return file_path.replace(os.path.sep, SEPARATOR)


def create_block(file_path):
    """Convert a file's contents into a block for packing into a flat text file.

    Args:
        file_path: path of the file to be packed

    Returns:
        a string containing info for unpacking, and the file's contents
    """
    lines = []
    with open(file_path, 'r') as input_file:
        lines = [s.rstrip() for s in input_file.readlines()]
    output = PACK_STR % (format_header(file_path), '\n'.join(lines))
    return output.strip() + '\n\n'


def pack(file_path):
    """Pack the contents of a file into a string, along with information for
    unpacking.

    Args:
        file_path: path of the file to be packed

    Returns:
        a string containing the file contents, as well as information for
        unpacking the file
    """
    files = list_files(file_path)
    blocks = [create_block(f) for f in files]
    return ''.join(blocks)


def parse_header(line):
    """Parse the operating system formatted unpack path from a header string.

    Args:
        line: header line

    Returns:
        the relative path of the file contents, formatted using the proper
        separator for the current operating system
    """
    return line.strip()[TRIM_SIZE:-TRIM_SIZE].replace(SEPARATOR, os.path.sep)


def split_contents(lines):
    """Split contents from a flat text file into individual files.

    Args:
        lines: lines of text from the packed file

    Returns:
        a dictionary containing relative path and file contents as keys and
        values, respectively
    """
    blocks = {}
    current_path = ''
    for line in lines:
        if UNPACK_REGEX.match(line):
            current_path = parse_header(line)
            blocks[current_path] = []
            continue
        blocks[current_path].append(line)
    return blocks


def write_contents(blocks):
    """Reconstruct the contents of a packed file into it's original file tree to
    the current working directory.

    Args:
        blocks: a dictionary containing relative paths and file contents
    """
    for full_path in blocks.keys():
        root_path = os.path.dirname(full_path)
        try:
            os.makedirs(root_path)
        except OSError:
            pass
        with open(full_path, 'w') as output_file:
            output_file.write('\n'.join(blocks[full_path]))


def unpack(file_path):
    """Unpack a flat text file to the current working directory.

    Args:
        file_path: path of the file to unpack
    """
    lines = []
    with open(file_path, 'r') as input_file:
        lines = [s.rstrip() for s in input_file.readlines()]
    write_contents(split_contents(lines))


def display_help():
    """Display operating instructions to the console."""
    print """
Magpie: Convert project source code to and from a flat text file.

Note: This script is only intended to work with plain text data, and may have
issues unpacking binary data. While an attempt is made to filter-out binary
data, it's probably best to ensure the root directory you are attempting to pack
only contains plaintext data.


To pack a project's source code, navigate to the directory above project
root and execute the following command:

    magpie --pack {PROJECT_FOLDER} > {OUTPUT_FILE}.txt


To unpack a project's source code, navigate to the desired destination and
execute the following command:

    magpie --unpack {INPUT_FILE}.txt
    """


if __name__ == '__main__':
    try:
        if not 1 < len(sys.argv) < 4:
            raise ValueError
        if sys.argv[1] == '--pack':
            print pack(sys.argv[2]),
        elif sys.argv[1] == '--unpack':
            unpack(sys.argv[2])
    except (IndexError, ValueError):
        display_help()
