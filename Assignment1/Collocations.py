from cmath import sqrt
from gettext import find
from collections import Counter
import math
import re
import sys

def chi_square(bigram):
    global sum_bigram_vals
    final_bigram = {}
    for key, val in bigram.items():
        both_words = bigram[key]
        sum_not1 = both_words + search_first(key[0], key[1])
        sum_not2 = search_second(key[0], key[1])
        neither_words = sum_bigram_vals -(both_words + sum_not1 + sum_not2)

        for a in range(4):
            sum = 0
            temp_sum = 0
            #1-> (1,1) 2-> (1,2)  3-> (2,1) 4-> (2,2) 
            if(a == 1): #p(w1)p(w2)
                observed = both_words
                expected = (((both_words + sum_not2)/sum_bigram_vals)*((both_words + sum_not1)/sum_bigram_vals))* sum_bigram_vals
                sum += temp_sum

            elif(a == 2): #e = p(w1)p(!w2)
                observed = sum_not2
                expected = (((both_words + sum_not2)/sum_bigram_vals)*((sum_not2 + neither_words)/sum_bigram_vals))* sum_bigram_vals
                temp_sum = (pow((observed - expected),2)) / expected
                sum += temp_sum

            elif(a == 3): #p(!w1)p(w2)
                observed = sum_not1
                expected = (((sum_not1 + neither_words)/sum_bigram_vals)*((both_words + sum_not1)/sum_bigram_vals))* sum_bigram_vals
                temp_sum = (pow((observed - expected),2)) / expected
                sum += temp_sum
            
            elif(a == 4): #p(!w1)p(!w2)
                observed = neither_words
                expected = (((sum_not1 + neither_words)/sum_bigram_vals)*((sum_not2 + neither_words)/sum_bigram_vals))* sum_bigram_vals
                temp_sum = (pow((observed - expected),2)) / expected
                sum += temp_sum
        x=sqrt(sum)
        final_bigram[key] = x
    return(final_bigram)

def search_first(word1, word2): #search is concentrated on w1!= new 
    global bigram
    sum = 0
    for key, val in bigram.items():
        if(key[0] != word1 and key[1]== word2): sum+= bigram[key]
    return(sum)

def search_second(word1, word2): #search is concentrated on w2!= companies
    global bigram
    sum = 0

    for key, val in bigram.items(): 
        if(key[0] == word1 and key[1] != word2): sum+= bigram[key]
    return (sum)

def pmi(bigram):
    final_bigram = {}
    word_prob = float(1)

    for key, val in bigram.items():
        observed = bigram[key] / sum_bigram_vals #numerator
        for i in key: #2 keys
            word_prob =  word_prob * ((find_uni_val(i)) / sum_unigram_vals) #denominator
        word_prob =  observed / word_prob
        
        score = math.log2(word_prob)
        final_bigram[key] = score
        word_prob = 1.0
    return(final_bigram)

def printBi(bigram):
    for key, val in bigram.items():
        print("Bigram: ",key, "\t\tScore: ", val)

def find_uni_val(word):
    global unigram
    if(isinstance(word, str)): word = word.lower()

    if(word in unigram): return(unigram[word])
    else: return(0)

def uni_count(line):
    for word in line:
        if(word.lower() in unigram): unigram[word.lower()] += 1
        else: unigram[word.lower()] = 1

method = str(sys.argv[-1]).lower() #assuming args will be in correct order
unigram ={}
bigram = {}

with open(sys.argv[1], 'r') as file:
    line = re.findall('\w+', file.read())
    uni_count(line)

bigram = Counter(zip(line,line[1:]))
sum_unigram_vals = sum(unigram.values())
sum_bigram_vals = sum(bigram.values())

if(method.find("c")>-1): 
    final_bigram = chi_square(bigram)
    print("Chi-Squared: \n")
    printBi(final_bigram)

elif(method.find("p")>-1): 
    final_bigram = pmi(bigram)
    print("PMI: \n")
    printBi(final_bigram)
