import re
from collections import Counter
# from gettext import find
import sys

word_tag, tag_uni, tag_tag, tag_only, full_test, prob_dict= {}, {}, {}, [], '', {}


def probabilties(dictionary):
    element1, element2 = " ", " "
    for key in dictionary:
        element1, element2 = key[0], key[1]
        prob_dict[key] = find_vals(element2, element1, dictionary) / find_vals(element2, '', tag_uni)


def find_vals(word1, word2, dictionary): #use laplace smoothing
    if word1 != '' and word2 != '': #bigram search
        for keys in dictionary:
            if keys[0] == word1 and keys[1] == word2:
                # print("inside if inside for and if\t keys[{}] == {} and keys[{}] == {} -> {}".format(keys[0], word1, keys[1], word2, keys[0] == word1 and keys[1] == word2))
                return dictionary.get(keys)
            else:
                # print("inside else inside for and if\t keys[{}] == {} and keys[{}] == {} -> {}".format(keys[0], word1, keys[1], word2, keys[0] == word1 and keys[1] == word2))
                return 1

    elif word1 != '' and word2 == '': #unigram search, assume word1 will be searched word
        for keys in dictionary:
            if keys[0] == word1:
                # print("inside if inside for and elif\t keys[{}] == {} and keys[{}] == {} -> {}".format(keys[0], word1, keys[1], word2, keys[0] == word1 and keys[1] == word2))
                return dictionary.get(keys)
            else:
                # print("inside else inside for and elif\t keys[{}] == {} and keys[{}] == {} -> {}".format(keys[0], word1, keys[1], word2,keys[0] == word1 and keys[1] == word2))
                return 1


def viterbi():
    return


def strip_tags(actual_line):
    test_line = ''
    for a in range(len(actual_line)):
        index = actual_line[a].find("/")
        if index > 0: test_line = actual_line[a][0:index]

        global full_test
        full_test += " " + test_line


def preprocess(line_list):
    line_list.insert(0, '<s>')
    for a in range(len(line_list)):
        back_slash = re.findall(r'\\/', line_list[a])
        forward_slash = re.findall(r'/', line_list[a])

        # deal with tag phrases
        if len(back_slash) == 1 and len(forward_slash) == 2: line_list[a] = line_list[a].replace('\\/', ' ', 1)

        elif len(back_slash) == 1: line_list[a] = line_list[a].replace('\\/', '/')


def dict_vals(dict_line):
    for a in range(len(dict_line)):
        temp_line = dict_line[a].split("/") # assume that / is always in line

        if len(temp_line) == 1: # account for beginning of sentence <s> being by itself
            #tag unigram
            if temp_line[0] in tag_uni: tag_uni[temp_line[0]] += 1
            else: tag_uni[temp_line[0]] = 1
            global tag_only
            tag_only.append(temp_line[0])

        elif len(temp_line) == 2:
            if temp_line[1] in tag_uni: tag_uni[temp_line[1]] += 1 # tag unigram
            else: tag_uni[temp_line[1]] = 1

            if tuple(temp_line) in word_tag: word_tag[tuple(temp_line)] += 1 # word and tag bigram
            else: word_tag[tuple(temp_line)] = 1

            #make a string of only tags then make bigram of it
            tag_only.append(temp_line[1])


while len(sys.argv) > 1:  # so long as arguments include files to open
    for a in range(1, len(sys.argv)):
        file = open(sys.argv[a])

        if a == 1: #train
            for line in file:  # preprocessing of file
                line = line.split()
                preprocess(line)
                dict_vals(line)
            probabilties(word_tag)
            probabilties(tag_tag)
            tag_tag = Counter(zip(tag_only, tag_only[1:]))

            # probabilties()

        elif a == 2: #test
            for line in file:  # preprocessing of file
                line = line.split()
                preprocess(line)
                strip_tags(line)
            viterbi(full_test)

    # print("word_tag =\n{} \ntag_uni=\n{} \ntag_tag=\n{}".format(word_tag, tag_uni, tag_tag))
    # print("prob_dict =\n{}".format(prob_dict))
    break
