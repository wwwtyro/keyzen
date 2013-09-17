from nltk.corpus import brown
from pprint import pprint
from unipath import Path
import json
import tempfile
import numpy
import time
import tempfile
import urllib2
import os
import sys

# time program execution
start_time = time.time()

# ########################

chars = """ jfkdlsahgyturieowpqbnvmcxz6758493021`-=[]\;',./ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+{}|:"<>?""";

# ########################

# Generate all the patterns we want to count

bigrams = {}
for i in range(len(chars)):
    for j in range(len(chars)):
        bigram = chars[i] + chars[j]
        bigrams[bigram] = 0

# ########################

CORPUS = ''


# ########################

# fetch linux kernal, add all the text files to the Corpus

tempdir = tempfile.mkdtemp()
url = 'https://github.com/torvalds/linux/archive/master.zip'
test_url = 'https://github.com/facebook/libphenom/archive/master.zip'
file_name = url.split('/')[-1]
#u = urllib2.urlopen(url)

import subprocess as sub
import os

# download zipfile with output to console
def clear():  os.system('cls' if os.name=='nt' else 'clear')

wget_out_file = Path(tempdir, file_name)
wget = sub.Popen(['wget', test_url,'-O', wget_out_file], stdout=sub.PIPE, stderr=sub.STDOUT)
while True:
    line = wget.stdout.readline()
    if not line: break
    clear()
    print line
wget.wait()

# unzip
import zipfile
import string, sys

def istext(s):
    text_characters = "".join(map(chr, range(32, 127)) + list("\n\r\t\b"))
    _null_trans = string.maketrans("", "")

    if "\0" in s:
        return 0

    if not s:  # Empty files are considered text
        return 1

    # Get the non-text characters (maps a character to itself then
    # use the 'remove' option to get rid of the text characters.)
    t = s.translate(_null_trans, text_characters)

    # If more than 30% non-text characters, then
    # this is considered a binary file
    if len(t)/len(s) > 0.30:
        return 0
    return 1


zfile = zipfile.ZipFile(wget_out_file.absolute())
for name in zfile.namelist():
    f = zfile.read(name)
    if istext(f):
        CORPUS += f

#meta = u.info()
#file_size = int(meta.getheaders("Content-Length")[0])
#print("Downloading: {0} Bytes: {1}".format(url, file_size))
#
#file_size_dl = 0
#block_sz = 8192
#while True:
#    buffer = u.read(block_sz)
#    if not buffer:
#        break
#
#    file_size_dl += len(buffer)
#    f.write(buffer)
#    p = float(file_size_dl) / file_size
#    status = r"{0}  [{1:.2%}]".format(file_size_dl, p)
#    status = status + chr(8)*(len(status)+1)
#    sys.stdout.write(status)

#f.close()



# ########################

# add words from Brown corpus to our Corpus

n = 100#00000 # number of words to use
CORPUS += ' '.join(brown.words()[:n])
n_chars = len(CORPUS)
import re
CORPUS = re.sub('\s+',' ',CORPUS)
print 'CORPUS length: %s' % len(CORPUS)

for i in range(2, n_chars):
    bigrams[CORPUS[i-2:i]] += 1

# ########################

checksum = 0
not_found = []

for key, value in bigrams.iteritems():
    if value > 0:
        normalised = float(value) / n_chars
        bigrams[key] = normalised
        checksum += normalised
    else:
        not_found.append(key)

print "checksum: %s " % checksum
print '%s out of %s patterns not found' % (len(not_found), len(bigrams))

# save bigram frequencies to file
f = open('genreated_bigrams.json', 'w')
pprint(json.dumps(bigrams), f)
f.close()

print "exection took:", time.time() - start_time, "seconds"
