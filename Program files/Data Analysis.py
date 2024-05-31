from AnalysisFunctions import stopword_files, negative_file, positive_file
from AnalysisFunctions import sentiment_analysis, syllables, ComplexCount

def main():
    #creating a list of Stop words
    flist = sorted(glob.glob(os.path.join("C:/Users/Admin/Desktop/20211030 Test Assignment/StopWords", "*.txt")))
    stopwords_list = stopword_files(flist)
    print("Stopword_List = {}\nTotal_Stopwords = {}".format(stopwords_list, len(stopwords_list)))

    #creating a list of Negative words
    neg_filename = open("C:/Users/Admin/Desktop/20211030 Test Assignment/MasterDictionary/negative-words.txt",encoding='latin1')
    negativewords_list = negative_file(neg_filename)
    print ('\nList of negative words not found in stopword list={}\nTotal_negativewords = {}'.format(negativewords_list, len(negativewords_list)))
    neg_filename.close()

    #creating a list of Positive words
    pos_filename = open("C:/Users/Admin/Desktop/20211030 Test Assignment/MasterDictionary/positive-words.txt",encoding='latin1')
    positivewords_list = positive_file(pos_filename)
    print ('\nList of positive words not found in stopword list={}\nTotal_positivewords = {}'.format(positivewords_list, len(positivewords_list)))
    pos_filename.close()

    df1 = pd.read_excel('C:/Users/Admin/Desktop/20211030 Test Assignment/Output Data Structure.xlsx')
    df2 = pd.DataFrame()

    #Creating a list of all Data files
    Data_files = sorted(glob.glob(os.path.join("C:/Users/Admin/Desktop/20211030 Test Assignment/Assignment_Neha_Mundada", "*.txt")))

    for filename in Data_files:
      text, content, tokens, number_of_words, sent_tokens, number_of_sentences, filtered_text, filtered_count = sentiment_analysis(filename)
      #print("Data cleaning = {}\nLength of cleaning data = {}".format(filtered_text,filtered_count))

      #Sentimental Analysis
      #Extracting Derived variables
      #Negative score
      negative_score = 0
      for word in filtered_text:
        if word in negativewords_list:
          negative_score+= 1

      #Positive score
      positive_score = 0
      
      for word in filtered_text:
        if word in positivewords_list:
          positive_score+= 1
      
      #Polarity Score
      polarity_score = float(positive_score - negative_score)/ float((positive_score + negative_score) + 0.000001)

      #Subjective Score
      subjectivity_score = float(positive_score + negative_score)/ float((filtered_count) + 0.000001)
      print("Negative score = {}\t\tPositve score = {}\nPolarity score = {}\tSubjective score = {}".format(negative_score,positive_score,polarity_Score,subjectivity_Score))


      #Analysis of Readability - Gunning Fog Index formula 

      #Syllable Count Per Word
      Count_per_word, Total_count = syllables(tokens)
      print("Syllable count per word = {}\t\tTotal syllables count = {}".format(Count_per_word, Total_count))

      #Complex Word Count
      #Complex words are words in the text that contain more than two syllables.
      number_complex_words = ComplexCount(Count_per_word)
      print("Complex word wount = ",number_complex_words)

      #Average Sentence Length
      avg_sent_length = number_of_words / number_of_sentences

      #Complex Words = words with more than two syllables.
      percentage_complex = (number_complex_words / number_of_words)*100

      #Gunning Fog Index
      Fog_index = 0.4 * (avg_sent_length + percentage_complex)

      print("Average sentence length = {}\nPercentage of complex words = {}\nFog index = {}".format(avg_sent_length,percentage_complex,Fog_index))

      #Average Number of Words Per Sentence
      avg_number_of_words = number_of_words / number_of_sentences
      print("Average Number of Words Per Sentence =",avg_number_of_words)

      #Word count - We count the total cleaned words present in the text 
      print("Word count = ",filtered_count)

      #Personal Pronouns
      Personalpronoun = re.compile(r'\b(I|we|my|ours|(?-i:us))\b',re.I)
      pronouns = Personalpronoun.findall(content)
      Total_pronouns = len(pronouns)
      print("Personal pronouns = {}\nTotal Personal Pronouns = {}".format(pronouns,Total_pronouns))

      #Average Word Length 
      sum = 0
      for word in tokens:
        no_of_letters = len(word)
        sum += no_of_letters

      average = sum / number_of_words
      print("Average Word Length =",average)
      
      # append rows to an empty DataFrame
      df2 = df2.append({'POSITIVE SCORE':positive_score, 'NEGATIVE SCORE':negative_score, 'POLARITY SCORE':polarity_score, 'SUBJECTIVITY SCORE':subjectivity_score, 'AVG SENTENCE LENGTH':avg_sent_length,
                            'PERCENTAGE OF COMPLEX WORDS':percentage_complex, 'FOG INDEX':Fog_index, 'AVG NUMBER OF WORDS PER SENTENCE':avg_number_of_words, 'COMPLEX WORD COUNT':number_complex_words, 
                            'WORD COUNT':filtered_count, 'TOTAL SYLLABLE':Total_count, 'PERSONAL PRONOUNS':Total_pronouns,'AVG WORD LENGTH ':average},ignore_index = True)

    df3 = pd.concat([df1.iloc[:,0:2], df2], axis=1, join='inner')
    print("Final Output =\n",df3)
    #Save output to excel file
    df3.to_excel('C:/Users/Admin/Desktop/20211030 Test Assignment/Assignment_Neha_Mundada/SOutput Data Structure.xlsx', index = False)

if __name__ == '__main__':
    main()
