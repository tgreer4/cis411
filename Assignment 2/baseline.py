import re
from collections import Counter
from gettext import find
import sys

tag_freq = {}

def tag_max(dictionary):
    for key, value in dictionary.items():
        if(len(value) > 1):
            print(key, '->', value)
    return 0

def dict_vals(dict_line):
    temp_list = []
    for a in range(len(dict_line)):
        temp_line = dict_line[a].split("/") # assume that / is always in line [word, tag]

        if temp_line[0] in tag_freq:
            if tag_freq[temp_line[0]]:
                tag_freq[temp_line[0]][1] += 1
            else:

        else:
            tag_freq[temp_line[0]] = [temp_line[1], 1]
        temp_list.clear()

def preprocess(line):
    unwanted = ('!', '?', '\%', ',', '(', ')', '&', '$', '')
    for a in range(len(line)):
        for u in unwanted: line[a] = line[a].replace(u, '')
        back_slash = re.findall(r'\\/', line[a])
        forward_slash = re.findall(r'/', line[a])

        if len(back_slash) == 1 and len(forward_slash) == 2: # deal with tag phrases
            line[a] = line[a].replace('\\/', ' ', 1)

        elif len(back_slash) == 1:
            line[a] = line[a].replace('\\/', '/')
    return (line)


while len(sys.argv) > 1:  # so long as arguments include files to open
    for a in range(1, len(sys.argv)):
        file = open(sys.argv[a])
        for line in file:
            line = line.split()
            line = preprocess(line)
            dict_vals(line)
            tag_max(tag_freq)
    # print(tag_freq)

    break