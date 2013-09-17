from nltk.corpus import brown
from pprint import pprint
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

chars = " jfkdlsahgyturieowpqbnvmcxz6758493021`-=[]\\;',./ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+{}|:\"<>?";

# ########################

# Generate all the patterns we want to count

bigrams = {}
for i in range(len(chars)):
    for j in range(len(chars)):
        bigram = chars[i] + chars[j]
        bigrams[bigram] = 0

# ########################

# Count bigrams from the Brown corpus

n = 100#00000 # number of words to use
raw_text = ' '.join(brown.words()[:n])
n_chars = len(raw_text)

for i in range(2, n_chars):
    bigrams[raw_text[i-2:i]] += 1

# ########################

# count bigrams from linux kernal

tempdir = tempfile.mkdtemp()
#repo = Repo.clone_from('https://github.com/torvalds/linux.git', tempdir)
url = 'https://github.com/torvalds/linux/archive/master.zip'
file_name = url.split('/')[-1]
u = urllib2.urlopen(url)
f = open(os.path.join(tempdir, file_name), 'wb')

import subprocess as sub

command = ['wget', url, '-o', os.path.join(tempdir, file_name)]
p = sub.Popen(command, stdout=sub.PIPE)
stdout, stderr = p.communicate()

command = ['unzip', os.path.join(tempdir, file_name)]
p = sub.Popen(command, stdout=sub.PIPE)
stdout, stderr = p.communicate()

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

f.close()




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
