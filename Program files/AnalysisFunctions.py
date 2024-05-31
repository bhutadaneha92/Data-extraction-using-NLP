import os
import glob
import string
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
nltk.download('punkt')
import pandas as pd


#creating a list of stop words.
def stopword_files(flist):
  
  stopwords_list = []
  for filename in flist:
      with open(filename, 'r', encoding='latin1') as f:
          stopwords_list.extend(f.read().split("\n"))

  return stopwords_list

#creating a list of Negative words.
def negative_file(fname):
  
  negative_words = []
  for line in fname:
    negative_words.append(line.rstrip())
  #print ('\nList of negative words={}\n, Total_Negativewords = {}'.format(negative_words, len(negative_words)))
  
  #add only those words in the list if they are not found in the Stop Words Lists. 
  neg = []
  for negword in negative_words:
    if negword not in stopwords_list:
      neg.append(negword)

  return neg

#creating a list of Positive words.
def positive_file(fname):
  
  positive_words = []
  
  for line in fname:
    positive_words.append(line.rstrip())
  
  #add only those words in the list if they are not found in the Stop Words Lists. 
  pos = []
  for posword in positive_words:
    if posword not in stopwords_list:
      pos.append(posword)
  
  return pos

def sentiment_analysis(filename):
  
  file = open(filename, 'r', encoding='utf-8')
  text = file.read()
  file.close()

  #Data Cleaning
  #Remove punctuation present in text
  content = text.translate(str.maketrans('', '', string.punctuation)) 
  
  #Convert the text into a list of tokens 
  tokens = word_tokenize(content)
  number_of_words = len(tokens)             #Total word count
      
  #Convert the text into a list of sentences
  sent_tokens = sent_tokenize(text)   
  number_of_sentences = len(sent_tokens)    #Total sentence count

  #Removing the stop words from text
  filtered_text = []
    
  for w in tokens:
    if w not in stopwords_list:
      filtered_text.append(w)
  filtered_count = len(filtered_text)

  return text, content, tokens, number_of_words, sent_tokens, number_of_sentences, filtered_text, filtered_count
      
#Syllable Count Per Word
def syllables(Wordlist):
    Totalcount = 0
    Count_per_word = []
    vowels = 'aeiouyAEIOUY'
    for word in Wordlist:
      count = 0
      if word[0] in vowels:
        count +=1
      
      for i in range(1,len(word)):
        if word[i] in vowels and word[i-1] not in vowels:
          count +=1
      if word.endswith('es') or word.endswith('ed'):
        count -= 1
      Count_per_word.append(count)
      Totalcount+=count
    
    return Count_per_word, Totalcount

#Complex Word Count
def ComplexCount(SyllableCount):
  number_complex_words=0
  for Count_per_word in SyllableCount:
    if Count_per_word > 2:
      number_complex_words+=1
  
  return number_complex_words

