import nltk
from nltk.corpus import cmudict
#nltk.download()
dictionary = cmudict.dict()
from nltk.tokenize import word_tokenize
from curses.ascii import isdigit
##print dictionary
#print dictionary['fire']
word1 = "can't"
word2 = "pant"

text = """a woman whose friends called a can't
on a lark when bathing all pant
saw a man come along
and unless we are wrong
you expected this line to be rant"""
text2 = """An exceedingly fat friend of mine,
When asked at what hour he'd dine,
Replied, "At eleven,
At three, five, and seven,
And eight and a quarter past nine"""

text_ = """I had a friend who last name was craney,
studying even if it was rainy,
he used to be on a roll,
NLP assignments took a toll,
completed all because of being brainy"""

def is_rhyme(word1, word2):


    list_1 = dictionary[word1]
    list_2 = dictionary[word2]
    print list_1
    print list_2


    trim_list1 =[]

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
    trim_list2 =[]

    for i in list_2:
        countr = 0
        for j in i:

            countr= countr + 1

            result = ''.join(k for k in j if not k.isdigit())
            result = result[:1]
            if(result in 'AEIOU' and countr == 1):
                trim_list2 = list_2
                break

            else:
                if(not j.isdigit() and j not in 'AEIOU'):
                    trim_list2.append(i[countr:])
                    break
    print trim_list1
    print trim_list2
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
                if (j == i[-sub_len1:]) or (i ==j[-sub_len2:]):
                    return True



    return False



    #print list_1
    #print list_2
def guess_syllable(word):

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
def nsyl(word):
  lowercase = word.lower()
  if lowercase not in dictionary:
     return 1
  else:
      counter = []
      for x in dictionary[lowercase]:

          c = 0
          for y in x:
              if y[-1].isdigit():
                  c = c+1
          counter.append(c)

  return min(i for i in counter)


def apostrophe_tokenize(line):

    nltk.re.sub(r'[^\w\s]','', line)

    return line.split()

def is_limerick(text):
    text = text.strip()
    text = text.replace(',','')
    text = text.replace('"','')
    text = text.replace(".", '')
    arr_lines =[]
    for line in text.split('\n'):
        arr_lines.append(line)
    if len(arr_lines) < 5:
        return False
    else:
        arr_sum_syl_line = []

        for i in range(len(arr_lines)):
            arr_word = apostrophe_tokenize(arr_lines[i])
            num_syl = 0
            arr_word_syll = []

            for i in arr_word:
                arr_word_syll.append(nsyl(i))
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

        if not (abs(arr_sum_syl_line[0] > arr_sum_syl_line[2]) and abs(arr_sum_syl_line[0] > arr_sum_syl_line[3]) and abs(arr_sum_syl_line[1] > arr_sum_syl_line[2]) and abs(arr_sum_syl_line[1] > arr_sum_syl_line[3]) and abs(arr_sum_syl_line[4] > arr_sum_syl_line[2]) and abs(arr_sum_syl_line[4] - arr_sum_syl_line[3])):
            return False

        if min(arr_sum_syl_line) < 4:
            return False
        arr_last_word = []
        for i in range(len(arr_lines)):
            arr_word = apostrophe_tokenize(arr_lines[i])
            arr_last_word.append(arr_word[-1])

        if (is_rhyme(arr_last_word[0], arr_last_word[1]) and is_rhyme(arr_last_word[0], arr_last_word[4])
            and is_rhyme(arr_last_word[1],arr_last_word[4]) and is_rhyme(arr_last_word[2],arr_last_word[3])
            and not is_rhyme(arr_last_word[0],arr_last_word[2]) and not is_rhyme(arr_last_word[0],arr_last_word[3])
            and not is_rhyme(arr_last_word[1],arr_last_word[2]) and not is_rhyme(arr_last_word[1],arr_last_word[3])
            and not is_rhyme(arr_last_word[4],arr_last_word[2]) and not is_rhyme(arr_last_word[4],arr_last_word[3])):
            return True
    return False









#print guess_syllable('Analog')
#print nsyl("Analog")
print is_limerick(text_)
#print is_rhyme(word1, word2)
