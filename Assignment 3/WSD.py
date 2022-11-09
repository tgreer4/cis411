import sys
import math
import random

sense, folds = {}, {1:[], 2: [], 3: [], 4: [], 5: []}
count_instance = 0

# def preprocess(list):
#     for lines in list:
        # begin_index = lines.find('%') #find senseid for count of senses
        # if begin_index > 0:
        #     senseid = lines[begin_index:-1]
        #     if senseid in sense: sense[senseid] += 1
        #     else: sense[senseid] = 1
def wsd():
    test_vals = []
    for a in range(5):
        test_fold = random.randrange(1, 5)
        while test_fold in test_vals: #use a random num generator and pop it into a list of folds already used
            test_fold = random.randrange(1, 5)
        test_vals.pop(test_fold)



def populate_folds(fold_size,text):
    global folds
    size_tracker = fold_size

    for key in range(len(folds)):
        for iterator in range(3, len(text), 7):
            if iterator == 4 and previous_index > (4+fold_size):
                folds[key].pop(text[iterator])
                size_tracker -= 1 #make sure number of instances within a fold are correct
                previous_index = iterator


while len(sys.argv) > 1:  # so long as arguments include files to open, assume only 1
    file = open(sys.argv[1])
    text = file.readlines()
    for iterator in range(3, len(text), 7): count_instance += 1
    fold_size = math.ceil(count_instance / 5)
    populate_folds(fold_size, text)
