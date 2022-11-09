import sys
import math

preprocess_data= []
sense, folds = {}, {1:[], 2: [], 3: [], 4: [], 5: []}
count_instance = 0

# def preprocess(list):
#     for lines in list:
        # begin_index = lines.find('%') #find senseid for count of senses
        # if begin_index > 0:
        #     senseid = lines[begin_index:-1]
        #     if senseid in sense: sense[senseid] += 1
        #     else: sense[senseid] = 1


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


# text = [
#     'something', 'something', 'something', 'something', 'something', 'something'
#         0            1              2           3           4           5
# ]
#
# folds = {
#     1: [list[0], list2[1]]
#     2: [list2[2], list2[[3]]]
#     3: [list2[4], list3[5]] }
#
# NOT
#
# folds = {
#     1: [list[0], list2[1]]
#     2: [list2[0], list2[[1]]]
#     3: [list2[0], list3[1]]
# }