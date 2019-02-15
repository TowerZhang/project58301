from collections import Counter
import operator




def get_elements(sequence):
    element_set = sequence.split('}')
    i = 0
    for element in element_set:
        if len(element) != 0:   # strip off the brace "{,}"
            element_set[i] = element.split('{')[1]
            i = i + 1
        else:                   # strip off the empty value after "{,}" removing operation
            element_set.remove(element)

    return element_set


def get_items(element):
    item_set = list(map(lambda x: x.strip(), element.split(',')))
    return item_set


def get_sequence_distinct(sequence):
    sequence_distinct = {}
    for each in range(len(sequence)):
        if each == 0:
            sequence_distinct = set(sequence[each])
        else:
            temp_set = set(sequence[each])
            sequence_distinct.update(temp_set)
    # print(sequence_distinct)
    return sequence_distinct

def get_seq_length(sequence):
    seq_length = 0;
    for each in sequence:
        seq_length += len(each)
    return seq_length


def deep_list_print(list1):
    for elements in list1:
        if isinstance(elements,list) or isinstance(elements, tuple):
            deep_list_print(elements)
        elif isinstance(elements, dict):
            for i in elements.items():
                print(i)
        else:
            print(elements)


def is_deep_list(list1):
    for element in list1:
        if isinstance(element, tuple) or isinstance(element, list):
            return True
    return False


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def lexicgraphic_asc_order(ele1, ele2):
    if is_number(ele1) and is_number(ele2):
        return float(ele2) > float(ele1)
    else:
        return ele2 > ele1


def open_files(input_data, para_data):
    with open(input_data, "r") as f1:
        trans = f1.read().splitlines()
        i = 0
        for each in trans:
            trans[i] = trans[i].replace('<', '')
            trans[i] = trans[i].replace('>', '')
            i = i + 1
        translen = len(trans)
        trans_list = []
        for ele in trans:
            element_set = get_elements(ele)
            element_list = []
            for item in element_set:
                item_list = get_items(item)
                element_list.append(sorted(item_list))
            trans_list.append(element_list)
        # for i in trans_list:
        #     print(i)

    with open(para_data, "r") as f2:
        parameters = f2.read().splitlines()
        mis = parameters[0:-1]
        minSupDict = {}
        MIS = {}
        SDC = 0
        for line in parameters:
            if "SDC" in line:
                SDC = float((line.split("=")[1]).strip())
            elif "MIS" in line:
                temp_var = line.split("=")
                # extract item from 1st token
                key = (temp_var[0][temp_var[0].index('(') + 1:temp_var[0].index(')')]).strip()
                minSupDict[tuple([key])] = float(temp_var[1].strip())
                value = minSupDict[tuple([key])]
                MIS.update({key: value})
        # print(MIS)
        # print(SDC)
    return trans_list, translen, MIS, SDC


def getL(trans, sorted_MIS, translen):

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
        if first <= sup_dict[each]:
            temp_list4.append(each)
            temp_list5.append(sup_dict[each])
    L = dict(zip(temp_list4, temp_list5))
    # print(L)
    return L, sup_dict


def getF1(L, MIS):
    temp_list6 = []
    temp_list7 = []
    for each in L:
        if MIS.get(each) <= L[each]:
            temp_list6.append(each)
            temp_list7.append(L[each])
    F1 = dict(zip(temp_list6, temp_list7))
#     print(F1)
    return F1


def level2_candidate_gen(L, SDC, MIS):
    C2 = {}
    for l in L.keys():
        for h in L.keys():
            if l == h and MIS[l] <= L[l]:
                temp_list = []
                temp_list.append(tuple([l]))
                temp_list.append(tuple([h]))
                C2.update({tuple(temp_list): 0})
            else:
                min_item = l
                max_item = h
                if MIS[l] > MIS[h]:
                    min_item = h
                    max_item = l
                if L[min_item] >= MIS[min_item] and L[max_item] >= MIS[min_item] and abs(L[min_item] - L[max_item]) <= SDC:
                    temp_list = []
                    temp_list.append(tuple([min_item]))
                    temp_list.append(tuple([max_item]))
                    C2.update({tuple(temp_list): 0})
                    temp_list2 = []
                    temp_list2.append(tuple([max_item]))
                    temp_list2.append(tuple([min_item]))
                    C2.update({tuple(temp_list2): 0})
                    if lexicgraphic_asc_order(min_item, max_item):
                        temp_list3 = []
                        temp_list3.append(tuple([min_item, max_item]))
                        C2.update({tuple(temp_list3): 0})
                    else:
                        temp_list4 = []
                        temp_list4.append(tuple([max_item, min_item]))
                        C2.update({tuple(temp_list4): 0})

    return C2


def gen_Fk(trans_list, Ck, MIS):
    candidate_set = list(Ck.keys())
    for trans in trans_list:
        for c in candidate_set:
            is_exist = False
            if is_deep_list(c):
                start = 0
                count = 0
                for i in c:
                    for t in range(start, len(trans)):
                        if set(trans[t]) & set(i) == set(i):
                            start = t + 1
                            count = count + 1
                            break
                # print(count)
                if count == len(c):
                    is_exist = True
                    # print(trans)
                    # print(c)
            else:
                for t in trans:
                    if set(t) & set(c) == set(c):
                        is_exist = True
                        break
            # print(is_exist)
            if is_exist:
                Ck[c] += 1

    Fk = []
    for c in Ck:
        if is_deep_list(c):
            minMIS = 1
            for i in c:
                for j in i:
                    if MIS[j] <= minMIS:
                        minMIS = MIS[j]

        else:
            minMIS = 1
            for i in c:
                if MIS[i] <= minMIS:
                    minMIS = MIS[i]
        if Ck[c]/len(trans_list) >= minMIS:
            Fk.append(tuple(c))
    # print(len(Fk))
    # print(Fk)
    return Fk


def deep_tuple2list(tuple1):
    alist = []
    for i in tuple1:
        list1 = []
        for j in i:
            list1.append(j)
        alist.append(list1)
    return alist


def deep_list2tutple(list1):
    tuple1 = []
    for i in list1:
        tuple2 = tuple(i)
        tuple1.append(tuple2)
    return tuple(tuple1)


def remove_head(sequence):
    temp_set = deep_tuple2list(sequence)
    if len(temp_set[0]) == 1:
        ele = temp_set[0]
        del temp_set[0]
        status = 0
    else:
        ele = temp_set[0][0]
        del temp_set[0][0]
        status = 1
    # print(type(ele))

    return tuple(temp_set), status, ele


def remove_rear(sequence):
    temp_set = deep_tuple2list(sequence)
    rear_idx = len(temp_set)-1

    if len(temp_set[rear_idx]) == 1:
        ele = temp_set[rear_idx]
        del temp_set[rear_idx]
        status = 0
    else:
        rear_rear = len(temp_set[rear_idx])
        ele = temp_set[rear_idx][rear_rear-1]
        del temp_set[rear_idx][rear_rear-1]
        status = 1
    # print(type(ele))

    return tuple(temp_set),status,ele


def remove_second(sequence):
    temp_set = deep_tuple2list(sequence)
    if len(temp_set[0]) == 1:
        if len(temp_set[1]) == 1:
            ele = temp_set[1]
            del temp_set[1]
        else:
            ele = temp_set[1][0]
            del temp_set[1][0]
    else:
        ele = temp_set[0][1]
        del temp_set[0][1]
    # print(type(ele))
    return tuple(temp_set), ele


def remove_second_last(sequence):
    temp_set = deep_tuple2list(sequence)
    rear_idx = len(sequence)-1
    if len(temp_set[rear_idx]) == 1:
        if len(temp_set[rear_idx-1]) == 1:
            ele = temp_set[rear_idx-1]
            del temp_set[rear_idx-1]
        else:
            rear_rear = len(temp_set[rear_idx-1])-1
            ele = temp_set[rear_idx-1][rear_rear]
            del temp_set[rear_idx-1][rear_rear]
    else:
        rear_rear = len(temp_set[rear_idx])-2
        ele = temp_set[rear_idx][rear_rear]
        del temp_set[rear_idx][rear_rear]
    # print(type(ele))
    return tuple(temp_set), ele


def ms_candidate_gen(Fk, MIS, sup_dict, SDC):
    # Join Step
    Ck = {}

    for s1 in Fk:
        for s2 in Fk:
            s1_len = get_seq_length(s1)
            if len(s1[len(s1) - 1]) == 1:   # find the last item in s1
                s1_last_ele = s1[len(s1) - 1][0]
            else:
                idx = len(s1[len(s1) - 1])
                s1_last_ele = s1[len(s1) - 1][idx - 1]

            flag1 = True                    # flag in case 1
            minMIS = MIS[s1[0][0]]
            for each in range(len(s1)):     # fist item has the lowest MIS
                for item in range(len(s1[each])):
                    if each == 0 and item == 0:
                        pass
                    else:
                        if minMIS >= MIS[s1[each][item]]:
                            flag1 = False
            if len(s2[len(s2) - 1]) == 1:   # find the last item in s1
                s2_last_ele = s2[len(s2) - 1][0]
            else:
                idx = len(s2[len(s2) - 1])
                s2_last_ele = s2[len(s2) - 1][idx - 1]
            s2_len = get_seq_length(s2)
            flag2 = True
            minMIS_last = MIS[s2_last_ele]

            for each in range(len(s2)):     # last item has the lowest MIS
                for item in range(len(s2[each])):
                    if each == len(s2) - 1 and item == len(s2[each]) - 1:
                        pass
                    else:
                        if minMIS_last >= MIS[s2[each][item]]:
                            flag2 = False
            if flag1:
                # print("flag1")
                temp_set1, ele1 = remove_second(s1)
                if isinstance(ele1, list):
                    second_s1 = ele1[0]
                else:
                    second_s1 = ele1
                temp_set2, status2, ele2 = remove_rear(s2)
                if isinstance(ele2, list):
                    ele2_str = ele2[0]
                else:
                    ele2_str = ele2
                if operator.eq(temp_set1, temp_set2) and MIS[ele2_str] > minMIS and abs(
                        sup_dict[second_s1] - sup_dict[ele2_str]) <= SDC:

                    # Join s1 and s2 when the condition above has been satisfied

                    if status2 == 0:  # 0, separate element
                        temp_set = deep_tuple2list(s1)
                        temp_set.append(ele2)
                        Ck.update({deep_list2tutple(temp_set): 0})  # c1 generated
                        # print("case1-1 : " + str(temp_set) + "\ts1: " + str(s1) + "\ts2:"+ str(s2))

                        if s1_len == 2 and len(s1) == 2 and lexicgraphic_asc_order(s1_last_ele, ele2_str):
                            temp_set2 = deep_tuple2list(s1)
                            temp_set2[len(temp_set2) - 1].append(ele2_str)
                            Ck.update({deep_list2tutple(temp_set2): 0})
                            # print("case1-2 : "+ str(temp_set2) + "\ts1: " + str(s1) + "\ts2:"+ str(s2))

                    else:                                           # not separate element
                        if s1_len > 2 or (s1_len == 2 and len(s1) == 1 and lexicgraphic_asc_order(s1_last_ele ,ele2_str)):
                            temp_set2 = deep_tuple2list(s1)
                            temp_set2[len(temp_set2) - 1].append(ele2_str)
                            Ck.update({deep_list2tutple(temp_set2): 0})
                            # print("case1-3 : " + str(temp_set2) + "\ts1: " + str(s1) + "\ts2:"+ str(s2))
            elif flag2:
                # print("flag2")
                temp_set2, ele2 = remove_second_last(s2)
                temp_set1, status1, ele1 = remove_head(s1)

                if isinstance(ele2, list):
                    second_last_s2 = ele2[0]
                else:
                    second_last_s2 = ele2
                if isinstance(ele1, list):
                    ele1_str = ele1[0]
                else:
                    ele1_str = ele1

                if operator.eq(temp_set1, temp_set2) and MIS[ele1_str] >= minMIS_last and abs(
                        sup_dict[second_last_s2] - sup_dict[ele1_str]) <= SDC:

                    # Join s1 and s2 when the condition above has been satisfied
                    if status1 == 0:
                        temp_set = deep_tuple2list(s2)
                        temp_set.insert(0, ele1)
                        Ck.update({deep_list2tutple(temp_set): 0})
                        # print("case2-1 : " + str(temp_set) + "\ts1: " + str(s1) + "\ts2:" + str(s2))

                        if s2_len == 2 and len(s2) == 2 and lexicgraphic_asc_order(ele1_str, s2[0][0]):
                            temp_set2 = deep_tuple2list(s2)
                            temp_set2[0].insert(0, ele1_str)
                            Ck.update({deep_list2tutple(temp_set2): 0})
                            # print("case2-2 : " + str(temp_set2) + "\ts1: " + str(s1) + "\ts2:"+ str(s2))

                    else:
                        if s2_len > 2 or (s2_len == 2 and len(s2) == 1 and lexicgraphic_asc_order(ele1_str, s2[0][0])):
                            temp_set2 = deep_tuple2list(s2)
                            temp_set2[0].insert(0, ele1_str)
                            Ck.update({deep_list2tutple(temp_set2): 0})
                            # print("case2-3 : " + str(temp_set2) + "\ts1: " + str(s1) + "\ts2:"+ str(s2))
            else:
                # print("flag3")
                temp_set1, status1, ele1 = remove_head(s1)
                temp_set2, status2, ele2 = remove_rear(s2)
                if isinstance(ele1, list):
                    remove_ele1 = ele1[0]
                else:
                    remove_ele1 = ele1
                if isinstance(ele2, list):
                    remove_ele2 = ele2[0]
                else:
                    remove_ele2 = ele2
                if operator.eq(temp_set1, temp_set2) and abs(sup_dict[remove_ele1] - sup_dict[remove_ele2]) <= SDC:
                    temp_set = deep_tuple2list(s1)
                    if status2 == 1:                                # 1, means {2,3}, removing 3
                        temp_set[len(temp_set) - 1].append(ele2)
                    else:                                           # 0, means {2},{3}, removing {3}
                        temp_set.append(ele2)
                    Ck.update({deep_list2tutple(temp_set): 0})
                    # print("case3 : " + str(temp_set) + "\ts1: " + str(s1) + "\ts2:"+ str(s2))


    # Pruning Step
    Ck_pruning = {}
    for each in Ck.keys():
        T = []
        candidate = deep_tuple2list(each)
        minMIS = 1
        for itemset in each:
            for item in itemset:
                if MIS[item] < minMIS:
                    minMIS = MIS[item]
        for i in range(len(candidate)):
            if len(candidate[i]) == 1:
                temp = []
                for j in range(len(candidate)):
                    if i == j:
                        pass
                    else:
                        temp.append(candidate[j])
                T.append(temp)
            else:
                for ii in range(len(candidate[i])):
                    temp_i = []
                    temp = []
                    for jj in range(len(candidate[i])):
                        if ii != jj:
                            temp_i.append(candidate[i][jj])
                    for k in range(len(candidate)):
                        if i == k:
                            temp.append(temp_i)
                        else:
                            temp.append(candidate[k])
                    T.append(temp)
        flag_add = True
        for each_t in T:
            tuple_each = deep_list2tutple(each_t)

            if tuple_each in Fk:
                pass
            else:
                flagEx = True
                for item in tuple_each:
                    for i in item:
                        if MIS[i] == minMIS:
                            flagEx = False
                if not flagEx:
                    flag_add = False
        if flag_add:
            Ck_pruning.update({each: 0})
    return Ck_pruning


def tuple2str_output(Fk):
    output = []
    for sequence in Fk:
        seq_str = "<"
        for itemset in sequence:
            if len(itemset) == 1:
                seq_str = seq_str + "{" + str(itemset[0]) + "}"
            else:
                seq_str = seq_str + "{"
                temp = ""
                for item in itemset:
                    temp = temp + "," + str(item)
                seq_str = seq_str + temp[1:] + "}"
        seq_str = seq_str + ">"
        output.append(seq_str)
    return output

















