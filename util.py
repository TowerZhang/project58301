import re
from collections import Counter, OrderedDict

input_data = 'data/data-1.txt'
para_data = 'data/para1-1.txt'


def get_elements(sequence):
    element_set = sequence.split('}')
    i = 0
    for element in element_set:
        if len(element) != 0:  # strip off the brace "{,}"
            element_set[i] = element.split('{')[1]
            i = i + 1
        else:  # strip off the empty value after "{,}" removing operation
            element_set.remove(element)

    return element_set


def get_items(element):
    item_set = list(map(lambda x: x.strip(), element.split(',')))
    return item_set


def get_sequence_distinct(sequence):
    element_set = get_elements(sequence)
    sequence_distinct = {}
    for each in range(len(element_set)):
        if each == 0:
            sequence_distinct = set(get_items(element_set[each]))
        else:
            temp_set = set(get_items(element_set[each]))
            sequence_distinct.update(temp_set)
    # print(sequence_distinct)
    return sequence_distinct


def open_files(input_data, para_data):
    with open(input_data, "r") as f1:
        trans = f1.read().splitlines()
        i = 0
        for each in trans:
            trans[i] = trans[i].replace('<', '')
            trans[i] = trans[i].replace('>', '')
            i = i + 1
        translen = len(trans)
        # element_set = get_elements(trans[1])
        # item_set = get_items(element_set[0])

    with open(para_data, "r") as f2:
        parameters = f2.read().splitlines()
        mis = parameters[0:-1]
        data = [item for item in mis]
        i = 0
        minSupDict = {}
        MIS = {}
        for i in range(len(data)):
            items = list(map(lambda x: x.strip(), data[i].split("=")))
            reSearch = re.search(r'MIS\(?(\w+)\)?', items[0])
            key = reSearch.group(1)
            minSupDict[tuple([key])] = float(items[1])
            value = minSupDict[tuple([key])]
            new = {key: value}
            MIS.update(new)
        # print(MIS)

        SDC = parameters[-1]
        items1 = SDC.strip()
        items1 = items1.split("=")
        SDC = float(items1[1])
        # print(SDC)
    return trans, translen, MIS, SDC


def getL(trans, sorted_MIS):


    list1 = [x[1] for x in sorted_MIS]
    temp_list = []
    for seq in range(len(trans)):
        element_set = get_sequence_distinct(trans[seq])
        for item in element_set:
            temp_list.append(item)
    counter = Counter(temp_list)
    # print(counter)

    temp_list2 = []
    for each in counter:
        value = counter.get(each)
        sup_count = value/translen
        temp_list2.append(sup_count)
        temp_list3 = list(counter.keys())
    sup_dict = dict(zip(temp_list3, temp_list2))
    # print(sup_dict)

    temp_list4 = []
    temp_list5 = []
    for each in sorted_MIS:
        if sorted_MIS.get(each) <= sup_dict.get(each):
            first = sorted_MIS.get(each)
            break
    # print(first)

    for each in sup_dict:
        if first < sup_dict[each]:
            temp_list4.append(each)
            temp_list5.append(sup_dict[each])
    L = dict(zip(temp_list4, temp_list5))
    # print(L)
    return L


def getF1(L, MIS):
    temp_list6 = []
    temp_list7 = []
    for each in L:
        if MIS.get(each) <= L[each]:
            temp_list6.append(each)
            temp_list7.append(L[each])
    F1 = dict(zip(temp_list6, temp_list7))
    print(F1)
    return F1


trans, translen, MIS, SDC = open_files(input_data, para_data)
sorted_MIS = dict(sorted(MIS.items(), key=lambda t: t[1]))
# print(sorted_MIS)
L = getL(trans, sorted_MIS)
F1 = getF1(L, MIS)
