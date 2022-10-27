
from cProfile import label
from sklearn import tree
from gettext import find
from re import L, split
import sys

#3 additional features
exclamation, quesion_mark= 0, 0  #automatically count dialogue

#5 core features
l_word, r_word = ' ', ' '
l_length, r_capital, l_capital = 0, 0, 0

def eos(line):
    print("in eos")
    for a in range(len(line)):
        if(line[a].find('.')>0):
            print("in if loop of eos",a, line[a], line[a].find("."))
            if((a-1) >-1):
                l_word = line[a-1] 
                l_length = len(line[a-1])
                l_capital = int(line[a-1][0].isupper())
            else: 
                l_word = ' '
                l_length = -1
                l_capital = -1

            if(a+1 != len(line)): #check for out of bounds error
                r_word = line[a+1]
                r_capital = int(line[a+1][0].isupper())
            else: 
                r_word = ' '
                r_capital = -1
            print("word: {word}, r_word: {rw}, r_cap: {rl}, l_word: {lw}, l_len: {ll}, l_cap: {lc}".format(word=line[a], rw = r_word, rl = r_capital, lw = l_word, ll=l_length, lc=l_capital))

def preprocess(line):
    punct = (',', '\'', '\"', '\n')
    for p in punct:
        line = line.replace(p,'')
    line = line.split(" ")
    return(line)

#clf = tree.DecisionTreeClassifier(randomstate = 0)

while (len(sys.argv) > 1): #so long as arguments include files to open
    for a in range(1,len(sys.argv)): 
        file = open(sys.argv[a])
        for line in file:
            if(line.find('.') > -1):
               line = preprocess(line) 
               print(type(line))
               line = eos(line)
            else: continue
    break


import pandas as pd 
from cProfile import label
from gettext import find
from re import L, split
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier

#3 additional features
count_periods, r_length, l_numb = 0, 0, 0

#5 core features
l_word, r_word = ' ', ' '
l_length, r_capital, l_capital = 0, 0, 0

column_names= ["l_word", "l_length", "l_cap", "l_numb", "r_word", "r_length", "r_cap", "count_periods", "label"]

def find_fts(dataframe):
    #new dataframe to send extracted fts into
    column_names= ["l_word", "l_length", "l_cap", "l_numb", "r_word", "r_length", "r_cap", "count_periods", "label"]
    final_df = pd.DataFrame(columns = column_names)

    #iterate through dataframe extracting fts when needed
    for a in range(len(dataframe)): 
        if((dataframe.loc[a, "word"].find(".")) > -1):
            count_periods = dataframe.loc[a, "word"].count(".")
            label = dataframe.loc[a, "label"]
            l_word = dataframe.iat[a, 1][0:-1] #excludes period
            l_length = 1 if (len(dataframe.iat[a, 1])-1 < 3) else 0
            l_numb = int(dataframe.iat[a, 1][0].isalnum())
            l_cap = int(dataframe.iat[a, 1][0].isupper())

            r_word = dataframe.iat[(a+1), 1] if (a < len       (dataframe) -1) else ' ' #excludes period
            r_cap = int(dataframe.iat[(a+1),1][0].isupper()) if (a < len(dataframe)-1) else  ' '
            r_length = int((len(dataframe.iat[(a+1),1][0]) < 3)) if (a < (len(dataframe)-1)) else  0

            temp = [l_word, l_length, l_cap, l_numb, r_word, r_length, r_cap, count_periods, label]

            final_df.loc[len(final_df)] = temp
            temp.clear()
    
    return(final_df)

def strip_sent(line):
    unwanted = ('\'', '!', '?', '\%', ',', '(', ')', '\"', '&', '$')
    for u in unwanted:
        line[1]=line[1].replace(u, '')
    return(line)

temp = []
while (len(sys.argv) > 1): #so long as arguments include files to open
    for a in range(1,len(sys.argv)): 
        file = open(sys.argv[a])
        for line in file:#preprocessing of file
            line = strip_sent(line.split())
            if(len(line[1]) == 0): continue
            else: temp.append(line)
        data = pd.DataFrame(temp)
        data = data.rename(columns={0:"line num", 1:"word", 2:"label"})
        
        final_df = find_fts(data)

        #Decision Tree
        clf = DecisionTreeClassifier()
        x = final_df.drop('label', axis=1)
        y = final_df['label']
        print("x: ", x, "\ny: ", y)
        
        if(a==1): #training file
            clf = clf.fit(x, y)
        
        elif(a == 2): #testing file
            y_pred = clf.predict(x,y)
    break