filesort.py
===========

Python script which allows you to select specific files which match with a string 
and optionally extension, and then group them into a folder. Similar functionality
to UNIX `mv` command. Allows reviewing the changes in text editor before
they are committed.

Usage
-----
    $ python filesort.py -s STRING [-h] [-f FOLDER] [-v] [-e EXTENSION] [-o OUTPUT]

### `-s <string>`

String which to group the files by. Supports Unix shell-style wildcards (https://docs.python.org/3/library/fnmatch.html)

### `-f <string>`

OPTIONAL. Origin folder from where to search from. Defaults to current working folder `./`,
and using `.` in folder path is replaced with working directory.

### `-v`

OPTIONAL. Increased verbosity.

### `-e <string>`

OPTIONAL. Extension criteria. Defaults to ignoring extension.

### `-o <string>`

OPTIONAL. Output where to move the matching files. If not specified, by default creates a
folder named `string`. Using `.` in output path is replaced with working directory.

#### Examples

+   This example searches all `.png` files in the `~/Pictures` folder and moves them
    to the output `~/Pictures/Holiday` folder which contain the given string `image`.

        python filesort.py -s image -f ~/Pictures -e .png -o ~/Pictures/Holiday

+   Example with Unix shell-style wildcards. Searches all files which include word
    `picture` anywhere in the filename and ends with `.png`. Using symbols in search
    string forces you to use -o to input output folder. You can use `.` to point to
    working directory.

        python filesort.py -s *picture*.png -o ./pictures

+   Minimal example, only -s provided. Creates a folder named `image` and all files that
    match name `image` are moved into it.

        python filesort.py -s image

Note
----
This is created just for educational purposes and testing git, any code can be reused
without implicit consent.