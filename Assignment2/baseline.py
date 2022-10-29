import re
from collections import Counter
from gettext import find
import sys

word_tag = {}

tag_uni = {}
tag_tag = {}

tag_only = []

def viterbi(line):
    return


def strip_tags(actual_line):
    test_line = ''
    pattern =
    for a in range(len(actual_line)):


    viterbi(test_line)

def preprocess(line_list):
    line_list.insert(0, '<s>')
    for a in range(len(line_list)):
        back_slash = re.findall(r'\\/', line_list[a])
        forward_slash = re.findall(r'/', line_list[a])

        # deal with tag phrases
        if len(back_slash) == 1 and len(forward_slash) == 2:
            line_list[a] = line_list[a].replace('\\/', ' ', 1)

        elif len(back_slash) == 1:
            line_list[a] = line_list[a].replace('\\/', '/')
    dict_vals(line_list)


def dict_vals(dict_line):
    for a in range(len(dict_line)):
        # assume that / is always in line
        temp_line = dict_line[a].split("/")

        # account for beginning of sentence <s> being by itself
        if len(temp_line) == 1:
            #tag unigram
            if temp_line[0] in tag_uni:
                tag_uni[temp_line[0]] += 1
            else:
                tag_uni[temp_line[0]] = 1
            global tag_only
            tag_only.append(temp_line[0])

        elif len(temp_line) == 2:
            # tag unigram
            if temp_line[1] in tag_uni:
                tag_uni[temp_line[1]] += 1
            else:
                tag_uni[temp_line[1]] = 1

            # word and tag bigram
            if tuple(temp_line) in word_tag:
                word_tag[tuple(temp_line)] += 1
            else:
                word_tag[tuple(temp_line)] = 1

            #make a string of only tags then make bigram of it
            tag_only.append(temp_line[1])


while len(sys.argv) > 1:  # so long as arguments include files to open
    for a in range(1, len(sys.argv)):
        file = open(sys.argv[a])

        if a == 1: #train
            for line in file:  # preprocessing of file
                line = line.split()
                preprocess(line)
            tag_tag = Counter(zip(tag_only, tag_only[1:]))

        elif a == 2: #test
            preprocess(line)
            strip_tags(line)

    break
