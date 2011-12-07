import os

import packages

files = " ".join(packages.getFiles())
os.system("epydoc --html -o doc " + files)

