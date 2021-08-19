from os import replace
import string
import re
import nltk
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
from functools import partial
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

# Stemmer

ps = PorterStemmer()

# Change Hashtags, URLS, and EMOJIS

import preprocessor as p

#Unicode 

from bs4 import BeautifulSoup

# Init the Wordnet Lemmatizer

lemmatizer = WordNetLemmatizer()

#stopwords 

stop_words = set(stopwords.words('english'))

#SpellChecker


from autocorrect import Speller

#slangwords

with open('slang.txt') as file:
    slang_map = dict(map(str.strip, line.partition('\t')[::2])
    for line in file if line.strip())

slang_words = sorted(slang_map, key=len, reverse=True) # longest first for regex
regex = re.compile(r"\b({})\b".format("|".join(map(re.escape, slang_words))))


#Functions


def rm_punctuation(sentence):
    # return sentence.translate(str.maketrans('', '', string.punctuation))

    return ''.join([i for i in sentence if i not in string.punctuation])

def lemmatize(sentence):
    
    return ' '.join([lemmatizer.lemmatize(word) for word in sentence.split(' ')])
        
def rm_stopwords(sentence):

    return ' '.join([word for word in sentence.split(' ') if word not in stop_words])

def rm_numbers(sentence):

    #removes numbers and fixes sentence to have 1 space after each word rather than two or more.
    #Normally this happens: 'Hello 10 world' -> Hello  World
    #What happens now: 'Hello 10 World' -> Hello World -> Gets rid of unnecessary spaces
    
    return re.sub(' +', ' ', sentence.translate(str.maketrans('', '', string.digits)))

def rm_capitalization(sentence):
    
    return sentence.lower() 

def stemming(sentence):
    
    return ' '.join([ps.stem(word) for word in word_tokenize(sentence)])

def rp_twitterHandles(sentence):
    
    return p.tokenize(sentence)

def rm_noise(text):
    rules = [
    {r'>\s+': u'>'},  # remove spaces after a tag opens or closes
    {r'\s+': u' '},  # replace consecutive spaces
    {r'\s*<br\s*/?>\s*': u'\n'},  # newline after a <br>
    {r'</(div)\s*>\s*': u'\n'},  # newline after </p> and </div> and <h1/>...
    {r'</(p|h\d)\s*>\s*': u'\n\n'},  # newline after </p> and </div> and <h1/>...
    {r'<head>.*<\s*(/head|body)[^>]*>': u''},  # remove <head> to </head>
    {r'<a\s+href="([^"]+)"[^>]*>.*</a>': r'\1'},  # show links instead of texts
    {r'[ \t]*<[^<]*?/?>': u''},  # remove remaining tags
    {r'^\s+': u''}  # remove spaces at the beginning
    ]
    for rule in rules:
        for (k, v) in rule.items():
            regex = re.compile(k)
            text = regex.sub(v, text)
        text = text.rstrip()
        return text.lower()

def rp_elongated(sentence):

    """ Replaces an elongated word with its basic form, unless the word exists in the lexicon """

    words = sentence.split(' ')
    
    for index, word in enumerate(words): 
        words[index] = re.sub(r'(.)\1+', r'\1\1', word)

    return ' '.join(words)

def base(sentence):
    return sentence

def contraction(sentence):

    import contractions

    return contractions.fix(sentence)

def rp_slang(sentence):

    slangReplacer = partial(regex.sub, lambda m: slang_map[m.group(1)])
    return slangReplacer(sentence)

def spell_check(sentence):

    #this function was used as a figurehead
    #I used this function seperatly from the rest, since it took to long to process 
    #I create a new dataframe just for spell_check called spell_check.csv

    return sentence



# LAST STEP: INCORPORATE A SPELL CHECK 

# import pkg_resources
# from symspellpy import SymSpell, Verbosity

# count = 0

# for index, item in enumerate(df.POS):
    
    
#     if item == []:
#         continue
#     else:
#         for index2, words in enumerate(item):
            
#             word, pos = words
            
#             if not pos == 'NN':
#             # max edit distance per lookup
#             # (max_edit_distance_lookup <= max_dictionary_edit_distance)
#                 suggestions = sym_spell.lookup(word, Verbosity.TOP,
#                        max_edit_distance=2)
                
#                 for suggestion in suggestions:
#                     if suggestion._distance == 1 and suggestion._count > 1000000000:
#                         df['tokenize'][index][index2] = suggestion._term
#                         count += 1

                    
# print(count)
