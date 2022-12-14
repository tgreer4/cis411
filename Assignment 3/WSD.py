import sys
import math
import random

senses = {1: {'name': '', 'total': 0}, 2: {'name': '', 'total': 0}}
#sense_num: {name: sense1, total:#, word1:#..}

true_sense = {} #id:actual sense
prob_sense = {} #id:guesssd sense

folds = {1: {}, 2: {}, 3: {}, 4: {}, 5:{}}
#fold_num: { id:[sense, sentence]}

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


def word_bags(fold_list):
    global senses
    sense_i = 0
    for keys in fold_list:
        senseid = fold_list[keys][0]

        if senseid in senses[1].values():
            senses[1]['total'] += 1
            sense_i = 1

        elif senseid in senses[2].values():
            senses[2]['total'] += 1
            sense_i = 2

        elif senses[1]['name'] == '':
            senses[1]['name'] = senseid
            senses[1]['total'] = 1
            sense_i = 1

        else:
            senses[2]['name'] = senseid
            senses[2]['total'] = 1
            sense_i = 2

        temp = fold_list[keys][1].split()
        for i in temp:
            if i.lower() in stop_words:
                temp.remove(i)
                fold_list[keys][1].replace(i, '')
            elif i.startswith("<head>"):
                continue
            else:
                if i.lower() in senses[sense_i]:
                    senses[sense_i][i.lower()] += 1
                else:
                    senses[sense_i][i.lower()] = 1


def five_fold():
    global folds
    temp_test = 0
    for a in range(1,6):
        for train_i in range(1,6): #train data
            if train_i != a:
                word_bags(folds[train_i])
            elif train_i == a: #don't do any testing until training is done
                continue
        wsd(folds[a])


def populate_folds(fold_size, text): #works
    global folds
    size_tracker = fold_size *2
    previous_index = 0
    instance_val = ''

    for key in range(1,len(folds)+1):
        for iterator in range(previous_index, len(text)):

            instance_index = text[iterator].find('.')
            if instance_index > -1 and text[iterator].startswith('<'):
                instance_val = text[iterator][instance_index+1:instance_index+8]

            correct_sense_i = text[iterator].find('%')
            if correct_sense_i > -1 and text[iterator].startswith('<'):
                folds[key][instance_val] = [(text[iterator][correct_sense_i + 1:-3])]
                true_sense[instance_val] = text[iterator][correct_sense_i + 1:-3]

            if iterator + 1 < len(text) and not text[iterator+1].startswith('<'):
                folds[key][instance_val].append(text[iterator+1])

            size_tracker -= 1  # make sure number of instances within a fold are correct

            if size_tracker == 0:
                previous_index = iterator+1 # keep index for next fold
                break
        size_tracker=fold_size*2


def wsd(fold_list): #recieves a fold_list in { id:[sense, sentence]} format
    for keys in fold_list: #keys -> id
        temp = fold_list[keys][1].split()
        for i in temp:
            if i.lower() in stop_words:
                temp.remove(i)
                fold_list[keys][1].replace(i, '')
            elif i.startswith("<head>"):
                continue
            else:
                prob_sense[keys] = predict_sense(i.lower())
    return


def predict_sense(word): #does math of log(c(w,s)+1/c(s)+len(s1) + len(s2))
    global senses
    sense1_length, sense2_length= len(senses[1])-2, len(senses[2])-2
    sum = [0.0, 0.0] #sum0->sense1 sum1-> sense2
    val, count_w_s = 0.0, 0.0,

    for sense_num in range(1,3):
        if senses[sense_num].get(word) != None: #if word not found, None returned
            count_w_s = senses[sense_num].get(word) + 1
        else: # account for laplace smoothing
            count_w_s = 1

        val = count_w_s / (senses[sense_num]['total'] + sense1_length + sense2_length)
        sum[sense_num-1] += math.log2(val)

    if sum[0] > sum[1]: #if max value is sum1
        return(senses[1]['name'])
    else: #if max value is sum2
        return (senses[2]['name'])


def validate(string):
    global true_sense, prob_sense
    num_correct = 0
    total_instances = senses[1]['total'] + senses[2]['total']
    for a in prob_sense:
        if true_sense.get(a) == prob_sense[a]:
            num_correct +=1
    percent = (num_correct / total_instances) * 100

    f = open("tank.wsd.out", "w")
    for key in range(1,len(folds)+1):
        f.write("{}\nFold {}\n".format(string,key))
        for item in folds[key]:
            predict = prob_sense.get(item)
            f.write("tank.{} tank%{}\n".format(item,predict))
        f.write("\n")
    f.write("Percent Correct: {}%".format(percent))
    f.close()
    return percent


while len(sys.argv) > 1:  # so long as arguments include files to open, assume only 1
    file = open(sys.argv[1])
    text = file.readlines()
    text = preprocess(text)
    fold_size = math.ceil((len(text)/2) / 5)
    populate_folds(fold_size, text)
    five_fold()
    correct_percent = validate(sys.argv[1])
    print("The algorithm has a {}% correctness in predicting the right sense.".format(correct_percent))
    break