import sys
import math
import random
import re

senses = {1:{'name': ' ', 'total': 0}, 2: {'name': ' ', 'total': 0}}
folds = {1:[], 2: [], 3: [], 4: [], 5: []}
count_instance = 0

stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

unwanted = ['</context>', '</instance>', '<context>']


# for iterator in range(3, len(text), 7): count_instance += 1

# def preprocess(textInput):

    # pattern = '\n'
    # for line in textInput:
    #     line = re.sub(pattern, '', line)
    #     print("line after sub:",line)
    #     if line in unwanted:
    #         line = line.replace(line, '')

    # print("textInput: ",textInput)


def word_bags(fold_list):
    global senses

    for lines in fold_list:
        begin_index = lines.find('%')
        if begin_index > 0:
            senseid = lines[begin_index:-1]
            if senses[1]['name'] == ' ':
                senses[1]['name'] = senseid
                senses[1]['name']['total'] += 1

            elif senses[1]['name'] == senseid: senses[1]['name']['total'] += 1
            elif senses[2]['name'] == ' ':
                senses[2]['name'] = senseid
                senses[2]['name']['total'] += 1
            elif senses[2]['name'] == senseid:
                senses[2]['name']['total'] += 1

        temp = lines.split()


def wsd():
    global folds
    test_vals = [] #use a random num generator and pop it into a list of folds already used for testing
    for a in range(5):
        test_fold = random.randrange(1, 5)
        while test_fold in test_vals and len(test_vals) < 5: #so long as random # isn't already in tested folds and all folds haven't been tested
            test_fold = random.randrange(1, 5)
        test_vals.pop(test_fold)

        if a == test_fold: continue
        else: word_bags(folds[a])


def populate_folds(fold_size,text):
    global folds
    size_tracker = fold_size
    temp_list = []
    previous_index = 0

    for key in range(len(folds)):
        for iterator in range(previous_index, len(text)):
            if size_tracker == 0:
                previous_index = iterator #keep index for next fold
                break

            # fix
            instance_index = text[iterator].find('.') #keeping instance id to use later on
            if instance_index > -1:
                split_text = text[iterator].split()
                instance_index = split_text[0].find('.')
                temp_list.append(split_text[0][instance_index:-1])

            #fix
            instance_sentence = iterator.find('<') #obtaining
            if instance_sentence > -1: temp_list.append(text[iterator])

            correct_sense_i = iterator.find('%')
            if correct_sense_i > -1: temp_list.append(text[iterator][correct_sense_i:-3])

            folds[key].pop(temp_list)

            size_tracker -= 1 #make sure number of instances within a fold are correct

            if (len(text)-iterator) < fold_size:
                size_tracker = len(text)-iterator


while len(sys.argv) > 1:  # so long as arguments include files to open, assume only 1
    file = open(sys.argv[1])
    text = file.readlines()
    # preprocess(text)
    # text.remove('<context>')
    print("text: ",text)
    break

    #
    # fold_size = math.ceil(count_instance / 5)
    # populate_folds(fold_size, text)
