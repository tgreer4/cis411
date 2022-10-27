import re
from collections import Counter
from gettext import find
import sys

word_uni = {}
word_bi = {}

tag_uni = {}
tag_bi = {}

tag_dict = {}

def dict_vals(line):
    print("line = ", line)
    for a in range(len(line)):
        temp_line = line[a].split("/") #assume that / is always in line
        print("temp_line at {}= {}".format(a, temp_line))
        for b in range(len(temp_line)):
            #word dictionary
            if(line[1].lower() in word_uni): word_uni[line[1].lower()] += 1
            else: word_uni[line[1].lower()] = 1

            #tag dictionary
            if(line[2].lower() in tag_uni): tag_uni[line[2].lower()] =+ 1
            else: tag_uni[line[2].lower()] = 1
            if(a== 5): break


while (len(sys.argv) > 1): #so long as arguments include files to open
    for a in range(1,len(sys.argv)): 
        file = open(sys.argv[a])
        for line in file: #preprocessing of file
            line = line.split()
            dict_vals(line)
    #print("word uni\n",word_uni, "\nword bi\n")
    break


