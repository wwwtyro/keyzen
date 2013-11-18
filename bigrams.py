from nltk.corpus import brown, gutenberg
from pprint import pprint
from unipath import Path
import json
import tempfile
import re
import numpy
import time
import tempfile
import urllib2
import sys
import subprocess as sub
import os
import zipfile
import string, sys

def download_zipped_corpus():
    tempdir = tempfile.mkdtemp()
    url = 'https://github.com/torvalds/linux/archive/master.zip'
    test_url = 'https://github.com/facebook/libphenom/archive/master.zip'
    file_name = url.split('/')[-1]

    # download zipfile with output to console
    def clear():  os.system('cls' if os.name=='nt' else 'clear')

    wget_out_file = Path(tempdir, file_name)
    wget = sub.Popen(['wget', url,'-O', wget_out_file], stdout=sub.PIPE, stderr=sub.STDOUT)
    while True:
        line = wget.stdout.readline()
        if not line: break
        clear()
        print line
    wget.wait()

    return wget_out_file.absolute()


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


def main(corpus=None):
    # time program execution
    start_time = time.time()

    # ########################

    chars = " jfkdlsahgyturieowpqbnvmcxz6758493021`-=[]\;',./ABCDEFGHIJKLMNOPQRSTUVWXYZ~!@#$%^&*()_+{}|:" + '"<>?';

    # ########################

    # Generate all the patterns we want to count

    bigrams = {}
    for i in range(len(chars)):
        for j in range(len(chars)):
            bigram = chars[i] + chars[j]
            bigrams[bigram] = 1 # add fake data

    # ########################

    CORPUS = ''

    # ########################

    if corpus is None:
        # fetch linux kernal, add all the text files to the Corpus
        corpus = download_zipped_corpus()

    # unzip corpus
    print "unzipping ..."

    zfile = zipfile.ZipFile(corpus.absolute())
    for name in zfile.namelist():
        f = zfile.read(name)
        if istext(f):
            CORPUS += f

    # ########################

    max_size = 100000000

    if len(CORPUS) > max_size:
        CORPUS = CORPUS[:max_size]

    # add words from Brown corpus to our Corpus

    CORPUS += ' '.join(brown.words())
    #CORPUS += gutenberg.raw().replace('\n', ' ').replace('\r', '')

    n_chars = len(CORPUS)
    CORPUS = re.sub('\s+',' ',CORPUS)
    print 'CORPUS length: %s' % len(CORPUS)

    print "adding bigrams..."
    for i in range(2, n_chars):
        try:
            bigrams[CORPUS[i-2:i]] += 1
        except KeyError as e:
            pass
            #print e
    print "finished"

    # ########################

    checksum = 0
    not_found = []

    for key, value in bigrams.iteritems():
        if value > 0:
            normalised = float(value) / n_chars
            bigrams[key] = normalised
            checksum += normalised
        if value == 1: # remember fake data
            not_found.append(key)

    print "checksum: %s " % checksum
    print '%s out of %s patterns not found' % (len(not_found), len(bigrams))

    # save bigram frequencies to file
    f = open('genreated_bigrams.json', 'w')
    f.write(json.dumps(bigrams))
    f.close()

    print "exection took:", time.time() - start_time, "seconds"

if __name__=="__main__":
    if len(sys.argv) > 1:
        main(corpus=Path(sys.argv[1]))
    else:
        main()
