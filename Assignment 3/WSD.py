import sys
import math
import random

senses = {1: {'name': ' ', 'total': 0}, 2: {'name': ' ', 'total': 0}}
true_sense = {} #id:actual sense
count_instance = 0
folds = {1: {}, 2: {}, 3: {}, 4: {}, 5:{}}

stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out',
              'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into',
              'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the',
              'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me',
              'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both',
              'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and',
              'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over',
              'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too',
              'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my',
              'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

unwanted = ('</context>', '</instance>', '<context>', '<instance id=')

def preprocess(list):
    res = []
    for a in list: res.append(a.replace('\n', ''))

    while ('' in res): res.remove('')

    for a in res[:]:
        if a.startswith(unwanted): res.remove(a)
    return (res)

# fix
def word_bags(fold_list):
    global senses

    for lines in fold_list:
        begin_index = lines.find('%')
        if begin_index > 0:
            senseid = lines[begin_index:-1]
            if senseid in senses.values():
                if senses[1]['name'] == senseid: senses[1]['name']['total'] += 1
                elif senses[2]['name'] == senseid: senses[2]['name']['total'] += 1
            # elif not any(senses.values()):

        temp = lines.split()
        for word in temp:
            if word in stop_words:
                temp.remove(word)

#fix
def wsd():
    global folds
    test_vals = []  # use a random num generator and pop it into a list of folds already used for testing
    for a in range(5):
        test_fold = random.randrange(1, 5)
        while test_fold in test_vals and len(
                test_vals) < 5:  # so long as random # isn't already in tested folds and all folds haven't been tested
            test_fold = random.randrange(1, 5)
        test_vals.pop(test_fold)

        if a == test_fold:
            continue
        else:
            word_bags(folds[a])

def populate_folds(fold_size, text):
    global folds

    size_tracker = fold_size *2
    previous_index = 0
    instance_val = ''
    list = []

    for key in range(1,len(folds)+1):
        for iterator in range(previous_index, len(text)):

            instance_index = text[iterator].find('.')
            if instance_index > -1 and text[iterator].startswith('<'):
                instance_val = text[iterator][instance_index+1:instance_index+8]

            correct_sense_i = text[iterator].find('%')
            if correct_sense_i > -1:
                folds[key][instance_val] = [(text[iterator][correct_sense_i + 1:-3])]
                true_sense[instance_val] = text[iterator][correct_sense_i + 1:-3]

            if iterator+1<len(text) and not text[iterator+1].startswith('<'):
                folds[key][instance_val].append(text[iterator+1])

            size_tracker -= 1  # make sure number of instances within a fold are correct
            list.clear()
            if size_tracker == 0:
                previous_index = iterator+1 # keep index for next fold
                break
        size_tracker=fold_size*2


while len(sys.argv) > 1:  # so long as arguments include files to open, assume only 1
    file = open(sys.argv[1])
    text = file.readlines()

    text = preprocess(text)
    fold_size = math.ceil((len(text)/2) / 5)
    populate_folds(fold_size, text)

    break