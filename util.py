
input_data = 'data/data-1.txt'
para_data = 'data/para1-1.txt'


def get_elements(sequence):
    element_set = sequence.split('}')
    i = 0
    for element in element_set:
        if len(element) != 0:                           # strip off the brace "{,}"
            element_set[i] = element.split('{')[1]
            i = i+1
        else:                                           # strip off the empty value after "{,}" removing operation
            element_set.remove(element)

    return element_set


def get_items(element):
    item_set = element.split(',')
    return item_set


with open(input_data, "r") as f1:
    trans = f1.read().splitlines()
    i = 0
    for each in trans:
        trans[i] = trans[i].replace('<', '')
        trans[i] = trans[i].replace('>', '')
        i = i + 1
    len_trans = i
    element_set = get_elements(trans[1])
    print(element_set)
    item_set = get_items(element_set[0])
    print(item_set)


# with open(para_data, "r") as f2:
#     parameters = []
#     parameters = f2.read().splitlines()
#     mis = parameters[0:-1]
#     data = [item for item in mis]
#     i = 0;
#     minSupDict = {}
#     MIS = {}
#     for i in range(len(data)):
#         items = list(map(lambda x: x.strip(), data[i].split("=")))
#         reSearch = re.search(r'MIS\(?(\w+)\)?', items[0])
#         key = reSearch.group(1)
#         minSupDict[tuple([key])] = float(items[1])
#         value = minSupDict[tuple([key])]
#         new = {key: value}
#         MIS.update(new)


