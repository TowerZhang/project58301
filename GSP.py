import util as util

input_data = 'data/data-1.txt'
para_data = 'data/para1-1.txt'
output_data = 'data/output.txt'

trans_list, translen, MIS, SDC = util.open_files(input_data, para_data)
sorted_MIS_list = sorted(MIS.items(), key=lambda t: t[1])
sorted_MIS_dict = dict(sorted_MIS_list)


L = util.getL(trans_list, sorted_MIS_dict, translen)
F1 = util.getF1(L, MIS)
k = 2
F_next = F1
write = ""
with open(output_data, "w") as f:
    if len(F1) > 0:
        print("Number of Length " + str(1) + " Frequency Sequences:" + str(len(F1)))
        write += "Number of Length " + str(1) + " Frequency Sequences:" + str(len(F1)) +"\n"
        for i in F1:
            print("\t<{"+str(i)+"}>")
            write += "\t<{"+str(i)+"}>\n"
    while len(F_next) > 0:
        if k == 2:
            Ck = util.level2_candidate_gen(L, SDC, sorted_MIS_list, MIS)
        else:
            Ck = util.ms_candidate_gen(F_next, MIS)
        Fk = util.gen_Fk(trans_list, Ck, MIS)
        if len(Fk) > 0:
            Fk_output = util.tuple2str_output(Fk)
            print("\nNumber of Length "+ str(k) +" Frequency Sequences:"+ str(len(Fk)))
            write += "\nNumber of Length "+ str(k) +" Frequency Sequences:"+ str(len(Fk)) +"\n"
            for each in Fk_output:
                print("\t"+each)
                write += "\t" + each + "\n"

        k += 1
        F_next = Fk
    f.write(write)
    print(f.name)
    f.close()



# C2 = util.level2_candidate_gen(L, SDC, sorted_MIS_list, MIS)
#
# F2 = util.gen_Fk(trans_list, C2, MIS)
#
#
# C3 = util.ms_candidate_gen(F2, MIS)
# F3 = util.gen_Fk(trans_list, C3, MIS)


# C4 = util.ms_candidate_gen(F3, MIS)
# F4 = util.gen_Fk(trans_list, C4, MIS)
# print(C4)
# print("F4")
# print(F4)