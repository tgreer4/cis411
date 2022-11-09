import sys
import math

preprocess_data= []
sense, folds = {}, {1:[], 2: [], 3: [], 4: [], 5: []}
count_instance = 0

def preprocess(list, list2):
    for lines in list:
        begin_index = lines.find('%')

        if begin_index > 0: #counts of senses
            senseid = lines[begin_index:len(lines)]
            if senseid in sense: sense[senseid] += 1
            else: sense[senseid] = 1

        begin_index = lines.find('<context>')
        if begin_index > 0:
            list2.pop(list[begin_index+1]) #

def five_fold(list):
    for lines in list:
        begin_index = lines.find('<context>')
        if begin_index > 0:
            global count_instance
            count_instance += 1
    fold_size =  math.ceill(count_instance / 5)
    temp = fold_size
    global folds
    for key in folds: #setting size of folds
        folds[key] = range(temp)
        remaining = count_instance - fold_size
        if remaining < fold_size:
            temp = remaining


def populate_folds(fold, list2, ):


while len(sys.argv) > 1:  # so long as arguments include files to open, assume only 1
    file = open(sys.argv[1])
    text = file.readlines()
    preprocess(text, preprocess_data)
