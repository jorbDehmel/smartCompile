A C++ smart compiler, handling directory structure and compilation.
Only compiles and/or links if it is needed, using file age.
Much like makefile but less complicated.

Flags:
sc (basic run)
sc -pclean (remove all .o and .out files)
sc -dclean (remove entire directory structure, keeping files)

Using a test (in cases where main is defined in multiple cpp files):
sc <filepath> (uses all files in source/ , plus the file at <filepath>)

It's pretty simple and it's python, so its not too hard to read the
source code if you need more details.

To update executable:
`pyinstaller --onefile main.py`
`mv dist/main ./sc`
`rm -f -r dist build`
`sudo cp sc /bin/sc`