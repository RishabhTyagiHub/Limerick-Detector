#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        self._pronunciations = nltk.corpus.cmudict.dict()
        dictionary = self._pronunciations
    def nsyl(self,word):
        lowercase = word.lower()

        if lowercase not in self._pronunciations:
            return 1
        else:
            counter = []
            for x in self._pronunciations[lowercase]:

                c = 0
                for y in x:
                    if y[-1].isdigit():
                        c = c + 1
                counter.append(c)

        return min(i for i in counter)

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        return self.nsyl(word)
        # TODO: provide an implementation!

    def is_rhyme(self,word1, word2):

        list_1 = self._pronunciations[word1]
        list_2 = self._pronunciations[word2]
        #print list_1
        #print list_2

        trim_list1 = []

        for i in list_1:
            countr = 0
            for j in i:

                countr = countr + 1

                result = ''.join(k for k in j if not k.isdigit())
                result = result[:1]
                if (result in 'AEIOU' and countr == 1):
                    trim_list1 = list_1
                    break
                else:
                    if (not j.isdigit() and j not in 'AEIOU'):
                        trim_list1.append(i[countr:])

                        break
        trim_list2 = []

        for i in list_2:
            countr = 0
            for j in i:

                countr = countr + 1

                result = ''.join(k for k in j if not k.isdigit())
                result = result[:1]
                if (result in 'AEIOU' and countr == 1):
                    trim_list2 = list_2
                    break

                else:
                    if (not j.isdigit() and j not in 'AEIOU'):
                        trim_list2.append(i[countr:])
                        break
        #print trim_list1
        #print trim_list2
        if len(trim_list1[0]) == len(trim_list2[0]):
            for i in trim_list1:
                for j in trim_list2:
                    if i == j:
                        return True


        else:
            for i in trim_list1:
                for j in trim_list2:
                    sub_len1 = len(j)
                    sub_len2 = len(i)
                    if (j == i[-sub_len1:]) or (i == j[-sub_len2:]):
                        return True

        return False

    def rhymes(self, a, b):
        """
        Returns True if two words (represented as lower-case strings) rhyme,
        False otherwise.
        """
        return self.is_rhyme(a,b)
        # TODO: provide an implementation!


        #Apostrophe Tokenize

    def apostrophe_tokenize(self,line):

        nltk.re.sub(r'[^\w\s]', '', line)

        return line.split()

    def guess_syllable(self,word):

        counters = 0
        vowels = 'aeiouy'
        word = word.lower()
        if word[0] in 'aeiouy':
            counters = counters+1
        for i in range(1, len(word)):
            if word[i] in 'aeiouy' and word[i - 1] not in 'aeiouy':
                counters = counters + 1
        if word.endswith('e'):
            counters = counters - 1
        if word.endswith('le'):
            counters = counters + 1
        if counters == 0:
            counters = counters + 1
        return counters


    def is_limericks(self,text):
        text = text.strip()
        #text = text.replace(',', '')
        #text = text.replace('"', '')
        #text = text.replace(".", '')
        #text = text.replace("!", '')
        #text = text.replace("?", '')
        re.sub('/^[A-z]+$/','',text)
        text = text.replace(',','')
        text = text.replace('.','')

        #text = text.replace("",'')
        arr_lines = []
        for line in text.split('\n'):
            arr_lines.append(line)
        if len(arr_lines) < 5:
            return False
        else:
            arr_sum_syl_line = []
            for i in range(len(arr_lines)):
                arr_word = self.apostrophe_tokenize(arr_lines[i])
                num_syl = 0
                arr_word_syll = []

                for i in arr_word:
                    arr_word_syll.append(self.num_syllables(i))
                sum = 0
                for i in arr_word_syll:
                    sum = sum + i

                arr_sum_syl_line.append(sum)
            if abs(arr_sum_syl_line[0] - arr_sum_syl_line[1]) > 2:
                return False
            elif abs(arr_sum_syl_line[0] - arr_sum_syl_line[4]) > 2:
                return False
            elif abs(arr_sum_syl_line[1] - arr_sum_syl_line[4]) > 2:
                return False
            elif abs(arr_sum_syl_line[2] - arr_sum_syl_line[3]) > 2:
                return False

            if not (abs(arr_sum_syl_line[0] > arr_sum_syl_line[2]) and abs(
                        arr_sum_syl_line[0] > arr_sum_syl_line[3]) and abs(
                        arr_sum_syl_line[1] > arr_sum_syl_line[2]) and abs(
                        arr_sum_syl_line[1] > arr_sum_syl_line[3]) and abs(
                        arr_sum_syl_line[4] > arr_sum_syl_line[2]) and abs(arr_sum_syl_line[4] - arr_sum_syl_line[3])):
                return False

            if min(arr_sum_syl_line) < 4:
                return False
            arr_last_word = []
            for i in range(len(arr_lines)):
                arr_word = self.apostrophe_tokenize(arr_lines[i])
                arr_last_word.append(arr_word[-1])

            if (self.is_rhyme(arr_last_word[0], arr_last_word[1]) and self.is_rhyme(arr_last_word[0], arr_last_word[4])
                and self.is_rhyme(arr_last_word[1], arr_last_word[4]) and self.is_rhyme(arr_last_word[2], arr_last_word[3])
                and not self.is_rhyme(arr_last_word[0], arr_last_word[2]) and not self.is_rhyme(arr_last_word[0],
                                                                                      arr_last_word[3])
                and not self.is_rhyme(arr_last_word[1], arr_last_word[2]) and not self.is_rhyme(arr_last_word[1],
                                                                                      arr_last_word[3])
                and not self.is_rhyme(arr_last_word[4], arr_last_word[2]) and not self.is_rhyme(arr_last_word[4],
                                                                                      arr_last_word[3])):
                return True
        return False

    def is_limerick(self, text):
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        # TODO: provide an implementation!
        return self.is_limericks(text)


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
