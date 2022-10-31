import re
from collections import Counter
from gettext import find
import sys

tag_freq = {}

def tag_max():
    return 0

def dict_vals(dict_line):
    temp_dict = {}
    for a in range(len(dict_line)):
        temp_line = dict_line[a].split("/") # assume that / is always in line
        temp_dict[temp_line[0].lower()] = {temp_line[1]: 1}
        if temp_dict[temp_line[0].lower()][temp_line[1]] in tag_freq:
            tag_freq[temp_line[0].lower()][temp_line[1]] += 1
        else:
            tag_freq[temp_line[0].lower()] = {temp_line[1]: 1}

def preprocess(line):
    unwanted = ('!', '?', '\%', ',', '(', ')', '&', '$')
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
            tag_max()
    print(tag_freq)

    break
