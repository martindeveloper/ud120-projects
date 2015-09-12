#!/usr/bin/python

import sys
from pathlib import Path
import urllib
import tarfile
import os
import importlib

'''
Define hook to show console progress bar
Based on http://stackoverflow.com/a/13895723
'''
def reporthook(blocknum, blocksize, totalsize):
    readsofar = blocknum * blocksize

    if totalsize > 0:
        percent = round(readsofar * 1e2 / totalsize, 1)

        if percent != reporthook.percent:
            reporthook.percent = percent

            print("{0}% ".format(percent), end="")

            if readsofar >= totalsize:
                print("\n")
    else:
        print("read {0} ".format(readsofar), end="")

    sys.stdout.flush() # force to flush IO

reporthook.percent = 0.0

print("1) First we need to check if you have required modules installed")

required_modules = ["nltk", "numpy", "sklearn"]

required_points = (len(required_modules) + 2)
current_points = 0

for module in required_modules:
    print()
    print(" - checking for {0}".format(module))

    try:
        importlib.import_module(module)
        print("  ✓ {0} module found".format(module))
        current_points += 1
    except ImportError:
        print("  ✗ {0} module not found, you should install {0} before continuing".format(module))

print()
print("2) Downloading the Enron dataset (this may take a while)")
print(" - size of dataset is about 423 MB")
print(" - so be patient please and do not stop downloading")
print()

dataset_filename = "../enron_mail_20150507.tgz"
dataset_path = Path(dataset_filename)

if not dataset_path.exists():
    try:
        url = "https://www.cs.cmu.edu/~./enron/enron_mail_20150507.tgz"
        urllib.request.urlretrieve(url, dataset_filename, reporthook)
        current_points += 1

        print(" ✓ Download complete!")
    except urllib.error.URLError:
        print(" ✗ Downloading failed, please check your connection")
else:
    print(" ✓ Dataset found on path '{0}', download is skipped".format(dataset_path))
    current_points += 1

print()
print("3) Unzipping Enron dataset (this may take a while)")
print()

os.chdir("..")
try:
    tfile = tarfile.open("enron_mail_20150507.tgz", "r:gz")
    tfile.extractall(".")
    current_points += 1
except EOFError:
    print(" ✗ Something went wrong while extracting files from archive, try to delete the archive")
except FileNotFoundError:
    print(" ✗ Archive not found on path '{0}', please check if is file downloaded correctly".format(dataset_path))

print()
print()

if current_points == required_points:
    message = "✓ You're ready to go!"
else:
    message = "✗ Some steps emitted warning or failed, please read the errors and try again"

message_length = len(message)

print("-" * message_length)
print(message)
print("-" * message_length)
print()
