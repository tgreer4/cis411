import re
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import preprocessing
from sklearn.metrics import accuracy_score

#3 additional features
count_periods, r_length, l_numb = 0, 0, 0

#5 core features
l_word, r_word = ' ', ' '
l_length, r_capital, l_capital = 0, 0, 0

def find_fts(dataframe):
    #new dataframe to send extracted fts into
    column_names= ["l_word", "l_length", "l_cap", "l_numb", "r_word", "r_length", "r_cap", "count_periods", "label"]
    final_df = pd.DataFrame(columns = column_names)

    #iterate through dataframe extracting fts when needed
    for a in range(len(dataframe)): 
        if((dataframe.loc[a, "word"].find(".")) > -1):
            count_periods = dataframe.loc[a, "word"].count(".")
            label = dataframe.loc[a, "label"]
            l_word = dataframe.iat[a, 1][0:-1].lower() #excludes period
            l_length = 1 if (len(dataframe.iat[a, 1])-1 < 3) else 0
            l_numb = int(dataframe.iat[a, 1][0].isalnum())
            l_cap = int(dataframe.iat[a, 1][0].isupper())

            r_word = dataframe.iat[(a+1), 1].lower() if (a < len (dataframe) -1) else '/' #excludes period
            r_cap = int(dataframe.iat[(a+1),1][0].isupper()) if (a < len(dataframe)-1) else  0
            r_length = int((len(dataframe.iat[(a+1),1][0]) < 5)) if (a < (len(dataframe)-1)) else  0

            temp = [l_word, l_length, l_cap, l_numb, r_word, r_length, r_cap, count_periods, label]

            final_df.loc[len(final_df)] = temp
            temp.clear()
    
    return(final_df)

def strip_sent(line):
    unwanted = ('\'', '!', '?', '\%', ',', '(', ')', '\"', '&', '$')
    for u in unwanted:
        line[1]=line[1].replace(u, '')
    return(line)

def label_convert(dataframe): #eos = 1, neos = 0
    for a in range(len(dataframe)):
        if(dataframe.loc[a, "label"].lower() == 'eos'): 
            dataframe.loc[a, "label"] = 1
        elif(dataframe.loc[a, "label"].lower() == 'neos'): 
            dataframe.loc[a, "label"] = 0
        elif(dataframe.loc[a, "label"].lower() == 'tok'): 
            dataframe.loc[a, "label"] = 2
    return(dataframe)
    
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
        final_df = label_convert(final_df)

        le = preprocessing.LabelEncoder()
        final_df["l_word"] = le.fit_transform(final_df["l_word"])
        final_df["r_word"] = le.fit_transform(final_df["r_word"])

        #Decision Tree
        x = final_df.drop('label', axis=1)
        y = final_df

        X_train, X_test, Y_train, Y_test = train_test_split(x, y, random_state=10)
        clf = DecisionTreeClassifier()

        if(a==1): #training file
            clf = clf.fit(X_train, Y_train)
            pred = clf.predict(X_test)
            print("Training File:\n\tThe Accuracy of the this is: ",accuracy_score(Y_test, pred))
        
        elif(a == 2): #testing file
            pred = clf.predict(X_test)
            print("Testing File:\n\tThe Accuracy of this is: ", accuracy_score(Y_test, pred))
    break