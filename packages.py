import os
import glob

f = open('packages.manifest', "r")
packages = f.readlines()
f.close()

packages = [package.strip() for package in packages if len(package.strip()) > 0]

def getPackages():
    return packages

def getFiles(extension='py'):
    ext = "*."+extension
    file_list = []
    for package in packages:
        here_dir = os.path.join("src", *package.split("."))
        file_list.extend(glob.glob(os.path.join(here_dir, ext)))
    return file_list

