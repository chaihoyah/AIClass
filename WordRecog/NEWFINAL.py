import numpy as np
import time

f = open("hmm.txt", 'r', encoding='utf-8')
lines = f.readlines()
phones = []
phone_num = 0
name_word = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "oh", "<s>"]
name_word_zero = ["zero","one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "oh", "<s>"]
minus = [-1, -2, 0, -1, -2, 0, -1, -2, 0, -1, 2]
el = [5, 8, 11, 14, 17, 21, 25, 30, 33, 36, 37]
starting_point = [16,26,33,43,53,63,76,92,99,109,113]
for idx, line in enumerate(lines):
    if line.find("~h") != -1:
        temp = line.split(" ")
        phones.append({"phone": temp[-1][1:-2]})
    elif line.find("<ENDHMM>") != -1: phone_num +=1
    elif line.find("<TRANSP>") != -1:
        tp = []
        length = len(lines[idx+1].split(" "))-1
        for k in range(length):
            temp = lines[idx+k+1].split(" ")
            for j in range(1,length+1):
                if j == length :
                    temp[j] = temp[j][:-1]
                temp[j] = float(temp[j])
            tp.append(temp[1:length+1])
        phones[phone_num]["TP"] = tp
    elif line.find("<STATE>") != -1:
        state_num = int(line.split(" ")[1][0])-1
        weight_one = float(lines[idx+2].split(" ")[2][:-1])
        mean_one = list(map(float,lines[idx+4][:-1].split(" ")[1:]))
        var_one = list(map(float,lines[idx+6][:-1].split(" ")[1:]))
        weight_two = float(lines[idx+7].split(" ")[2][:-1])
        mean_two = list(map(float,lines[idx+9][:-1].split(" ")[1:]))
        var_two = list(map(float,lines[idx+11][:-1].split(" ")[1:]))
        name = "state"+str(state_num)
        phones[phone_num][name] = {"pdf1":[weight_one, mean_one, var_one], "pdf2":[weight_two, mean_two, var_two]}

def get_obsprob(e, phone_num, state_num):
    global phones
    state_str = "state"+str(state_num)
    total_one, total_two = 0, 0
    mult_one, mult_two = 1, 1
    weight_one, weight_two = phones[phone_num][state_str]["pdf1"][0], phones[phone_num][state_str]["pdf2"][0]
    mean_one, mean_two = phones[phone_num][state_str]["pdf1"][1], phones[phone_num][state_str]["pdf2"][1]
    var_one, var_two = phones[phone_num][state_str]["pdf1"][2], phones[phone_num][state_str]["pdf2"][2]

    for idx, evid in enumerate(e):
        total_one += (-1/2)*((evid-mean_one[idx])**2) / (var_one[idx])
        total_two += (-1/2)*((evid-mean_two[idx])**2) / (var_two[idx])
        mult_one *= np.sqrt(var_one[idx])
        mult_two *= np.sqrt(var_two[idx])
    log_g1 = np.log(weight_one) - np.log(((2*np.pi)**(len(e)/2))*mult_one) + total_one
    log_g2 = np.log(weight_two) - np.log(((2*np.pi)**(len(e)/2))*mult_two) + total_two
    return log_g1 + np.log(1+np.exp(log_g2-log_g1))

def make_wordhmm(phone_seq):
    global phones
    trans_num = len(phone_seq)*3 + 2

    tp_matrix = np.zeros((trans_num,trans_num)).astype(float)
    if phone_seq[0] == 20: #<s>는 따로
        for idx, num in enumerate(phone_seq):
            for col in range(0,5):
                for row in range(0,5):
                    tp_matrix[row][col] = phones[num]["TP"][row][col]
        return tp_matrix

    trans_num -= 2 # 나머지
    tp_matrix = np.zeros((trans_num, trans_num)).astype(float)
    for idx, num in enumerate(phone_seq):
        if num == 17: # sp일 경우
            for col in range(3*idx+1, 3*idx+3):
                for row in range(3*idx, 3*idx+3):
                    if col%3 == 1 and row == 3*idx:
                        tp_matrix[row][col] = phones[phone_seq[idx-1]]["TP"][3][4] * phones[num]["TP"][row - 3 * idx][col - 3 * idx]
                    else:
                        tp_matrix[row][col] = phones[num]["TP"][row - 3 * idx][col - 3 * idx]
        else:
            for col in range(idx if idx == 0 else 3 * idx + 1, 3 * idx + 5 if idx == len(phone_seq) else 3 * idx + 4):
                for row in range(3 * idx, 3 * idx + 4):
                    tp_matrix[row][col] = phones[num]["TP"][row - 3 * idx][col - 3 * idx]
                    if idx != 0 and col % 3 == 1 and row == 3*idx:
                        tp_matrix[row][col] = phones[phone_seq[idx - 1]]["TP"][3][4] * phones[num]["TP"][row - 3 * idx][col - 3 * idx]
    return tp_matrix

word_hmm = {}

f_dic = open("dictionary.txt", 'r', encoding='utf-8')
lines_dic = f_dic.readlines()
for idx, line in enumerate(lines_dic):
    temp = line.split("\t")
    temp_two = temp[1].split(" ")
    if idx != 12: temp_two[-1] = temp_two[-1][:-1]
    temp = [temp[0]] + temp_two

    phone_seq = []
    for phone_name in temp_two:
        for num in range(21):
            if phones[num]["phone"] == phone_name:
                phone_seq.append(num)
    if idx != 12:
        word_hmm[temp[0]] =  [phone_seq, make_wordhmm(phone_seq)]
    else:
        word_hmm['zero_two'] = [phone_seq, make_wordhmm(phone_seq)]


f_uni = open("unigram.txt", 'r', encoding='utf-8')
f_bi = open("bigram.txt", 'r', encoding='utf-8')

lines_uni = f_uni.readlines()
for line in lines_uni[:-1]:
    temp = line.split("\t")

    word_hmm[temp[0]].append(float(temp[1][:-1]))
word_hmm["zero"].append(float(lines_uni[-1].split("\t")[1][:-1]))
word_hmm["zero_two"].append(float(lines_uni[-1].split("\t")[1][:-1]))

bigram_list = []
lines_bi = f_bi.readlines()
for line in lines_bi[:-1]:
    temp = line.split("\t")
    temp[2] = float(temp[2][:-1])
    bigram_list.append([temp[0],temp[1],temp[2]])


tot_phone = 0
for key in word_hmm.keys():
    tot_phone += len(word_hmm[key][0])

def viterbi(e_seq):
    global phones

    time_len = len(e_seq)
    state_num = 116

    m = [[-100000 for col in range(state_num)] for row in range(time_len)]
    m_prime = [[-100000 for col in range(state_num)] for row in range(time_len)]
    seq = np.zeros(time_len)
    for state in range(state_num):
        phone_num, state_idx, in_word_name = find_phone_num(state)
        state_len = len(phones[phone_num])-2 #f 면 3
        m[0][state] = np.log(find_stateprior(state)) + get_obsprob(e_seq[0], phone_num, state_idx+1)
        m_prime[0][state] = -10000
    for time in range(1,time_len):
        for state in range(state_num):
            for i in range(state_num):
                state_phone_num, state_state_num,state_word = find_phone_num(state)
                prob = find_transprob(i, state)
                if prob != 0:
                    Mij_prob = m[time-1][i] + np.log(prob) + get_obsprob(e_seq[time],state_phone_num,state_state_num+1)
                else:
                    Mij_prob = -1*np.inf
                if m[time][state] < Mij_prob:
                    m[time][state] = Mij_prob
                    m_prime[time][state] = i
        print("Finished")
    seq[time_len-1] = int(np.max(m_prime[time_len-1]))
    print(seq[time_len-1])
    for t in range(time_len-2,-1, -1):
        seq[t] = m_prime[t][int(seq[t+1])]
    return seq.astype(int)

def find_stateprior(phone_num):
    _, _, n = find_phone_num(phone_num)
    return word_hmm[n][2]

def find_transprob(i , j):
    prob = 0

    phone_num_i,state_num_i,p_word = find_phone_num(i)
    phone_num_j,state_num_j,f_word = find_phone_num(j)

    if phone_num_i == phone_num_j:
        if phone_num_i == 20 and state_num_i == 2 and state_num_j == 0: #sil -> sil
            prob = phones[phone_num_i]["TP"][3][4] * phones[phone_num_i]["TP"][state_num_i+1][state_num_j+1]
        elif (state_num_i!=2 and state_num_j!=0) or (state_num_i==2 and state_num_j==2) or (state_num_i==0 and state_num_j==0):
            prob = phones[phone_num_i]["TP"][state_num_i+1][state_num_j+1]
        return prob

    if state_num_i == 0 or state_num_i == 1:
        if phone_num_i == 17: #sp => 다른 단어 (sil 포함)
            if phones[phone_num_j]["phone"] in ["ey", "f", "n", "ow", "w", "s", "th", "t", "z", "sil"]:
                prob = phones[phone_num_i]["TP"][1][2] * find_bigram_num(i, j)
                return prob
        elif phone_num_i == phone_num_j and state_num_j == state_num_i+1: # 폰 내부
            prob = phones[phone_num_i]["TP"][state_num_i + 1][state_num_j + 1]
            return prob
    else: ##state_num_i가 2 (마지막 state)
        if phone_num_i == 20 and state_num_j==0: #sil -> 0로
            if phones[phone_num_j]["phone"] in ["ey", "f", "n", "ow", "w", "s", "th", "t", "z", "sil"]:  # sil -> 0로
                prob = find_bigram_num(i, j)*phones[phone_num_i]["TP"][3][4]
                return prob
        elif phones[phone_num_i]["phone"] in ["t", "v", "r", "n", "ow", "n", "s", "iy", "uw", "ow"]: #sp 0 -> 2
            if phone_num_j != 17 and state_num_j==0: #sp 0 -> 2
                prob = phones[17]["TP"][0][2] * phones[phone_num_i]["TP"][3][4] * find_bigram_num(i, j)
                return prob
            elif state_num_j==0: #0 -> sp #############################################################
                i_index = word_hmm["zero_two" if i==8 else p_word][0].index(phone_num_i)
                prob = word_hmm["zero_two" if i==8 else p_word][1][3*(i_index+1)][3*(i_index+1)+1]
                return prob
        elif state_num_j ==0: #단어내부

            if phone_num_i != 8 and phone_num_i != 15:
                i_index = word_hmm[p_word][0].index(phone_num_i)
                row = 3 * (i_index + 1)
                col = 3 * (i_index + 1) + 1
                prob = word_hmm[p_word][1][row][col]
            elif (phone_num_i == 8 and phone_num_j == 15) or (phone_num_i == 15 and phone_num_j == 3):
                i_index = word_hmm["zero_two"][0].index(phone_num_i)
                row = 3 * (i_index + 1)
                col = 3 * (i_index + 1) + 1
                prob = word_hmm[p_word][1][row][col]
            return prob
    return prob

def find_phone_num(num):
    global word_hmm
    global name_word
    global minus
    global el
    f_num = 0
    s_num = 0
    word = ""
    if num <= 15:
        mok = int(num/3)
        namuji = num%3
        if mok == 2:
            f_num = 15
            s_num = namuji
            word = "zero"
            return f_num, s_num, word
        elif mok == 3:
            f_num = 3
            s_num = namuji
            word = "zero"
            return f_num, s_num, word
        elif mok == 4:
            f_num = 16
            s_num = namuji
            word = "zero"
            return f_num, s_num, word
        elif num == 15:
            f_num = 17
            s_num = 0
            word = "zero"
            return f_num, s_num, word
        else:
            for i in range(len(word_hmm["zero"][0])):
                if mok == i:
                    f_num = word_hmm["zero"][0][i]
                    s_num = namuji
                    word = "zero"
                    return f_num,s_num,word
    elif 113<=num<=115:
        word ="<s>"
        s_num = (num-2)%3
        f_num = 20
        return f_num,s_num,word

    else:
        for idx,q in enumerate(name_word[:-1]):
            if starting_point[idx] <= num < starting_point[idx+1]:
                mok = int((num + minus[idx]) / 3)-el[idx]
                namuji = (num+minus[idx])%3
                for i in range(len(word_hmm[q][0])):
                    if mok == i:
                        f_num = word_hmm[q][0][i]
                        s_num = namuji
                        return f_num,s_num,q
def find_bigram_num(state_one,state_two):
    global bigram_list
    one_phone,one_state,one_word = find_phone_num(state_one)
    two_phone,two_state,two_word = find_phone_num(state_two)
    for bi in bigram_list:
        if bi[0] == one_word and bi[1] == two_word:
            return bi[2]
    return 0

f_uni = open("unigram.txt", 'r', encoding='utf-8')
f_bi = open("bigram.txt", 'r', encoding='utf-8')

lines_uni = f_uni.readlines()
for line in lines_uni[:-1]:
    temp = line.split("\t")

    word_hmm[temp[0]].append(float(temp[1][:-1]))

f_ref = open("reference.txt", 'r', encoding='utf-8')
f_rec = open("recognized.txt", 'w', encoding='utf-8')
f_tst = open("seq.txt", 'w', encoding='utf-8')
def make_word_seq(seq):
    global  starting_point
    to_phone = []
    word = []
    is_word = False
    wor_seq = []
    arr = np.array([starting_point])
    for idx, i in enumerate(seq[1:]):
        if i in (arr-1):
            wor_seq.append(-1)
            continue
        elif i in (arr-2):
            wor_seq.append(-1)
        n,_,wor = find_phone_num(i)
        index = name_word_zero.index(wor)
        wor_seq.append(index)
    """
    for idx,i in enumerate(seq[1:]):
        print(i)
        n,_,_ = find_phone_num(i)
        if idx != 0:
            if n != to_phone[-1]:
                to_phone.append(n)
        else:
            to_phone.append(n)
    print(to_phone)
    for idx,ph in enumerate(to_phone):
        for keyl in list(word_hmm.keys())[1:]:
            if ph == word_hmm[keyl][0][0]:
                isword = True
                for k in range(len(word_hmm[keyl][0])-1):
                    if idx+k >= len(to_phone):
                        break
                    if to_phone[idx+k] != word_hmm[keyl][0][k]:
                        isword = False
                if isword:
                    word.append(keyl)"""
    print(word)
    return wor_seq


start = time.time()
lines_ref = f_ref.readlines()

f_rec.write("#!MLF!#\n")
for idx, line in enumerate(lines_ref[1:11]):
    if line.find("tst") != -1:
        line = "tst/"+line[1:].split(".")[0]+".txt"
        f_read = open(line, 'r', encoding='utf-8')
        lines_read = f_read.readlines()
        e_seq = []
        for l in lines_read[1:]:
            arr =l.split(" ")
            arr = [x for x in arr if x]
            arr[len(arr)-1] = arr[len(arr)-1][:-1]
            arr = np.asarray(arr).astype("float")
            e_seq.append(arr)
        f_rec.write('"'+line[4:-3]+'.rec"\n')
        seq = viterbi(e_seq)
        f_tst.write(str(seq)+"\n")
        print(seq)
        word_seq = make_word_seq(seq)
        for jj in word_seq:
            f_rec.write(jj+"\n")
        f_rec.write(".\n")

print("time"+str(start-time.time()))

#rint(make_word_seq([-10000,95,26,27,28,28,108,115,115,115,115,115]))
f.close()
f_dic.close()
f_uni.close()
f_bi.close()
#f_read.close()
f_ref.close()
f_rec.close()
#print(find_transprob(115,113))
#print(phones)
#print(word_hmm)
#for i in range(116):
#    print(find_phone_num(i))
#print(find_phone_num(26))
test = "-10000     95     26     27     28     28    108    115    115    115\
    115    115     53     43     43     44     44     45     45     45\
     45     45     45     16     17     17     17     17     17     18\
     18     19     19     19     19     19     20     20     20     20\
     20     20     21     21     22     22     22     22     22     23\
     23     23     24     26     27     27     28     28     97      3\
      3      3      4      4      5     92     93     93     93     93\
     93     93     93     93     93     94     94     94     26     26\
     27     28     63     64     65     65     78     66      4      4\
      4      4      4      5      5      5     56     57     58     58\
      6      6      6      6      6      6      6      6      6      6\
      7      7      7      7      7      7      7      7     41     63\
     63     64     64     64     64     64     64     64     78     79\
     79     80     81     81     59     59     59     59     59     59\
     59     59     60     60     60     61     19     19     20     20\
     21     21     22     22     22     23     23     23     24     24\
    101     76     63     64     78     79     79     80     81     81\
     59     59     59     59     59     59     59     60     60     61\
     61     61     19     19     19     20     20     21     21     22\
     22     22     22     23     23     23     24     24     24    101\
     43     44     44     44     45     46     46     46     47     47\
     47     47     48     48     48      9      9     10     11     51\
     82     60     60     84     95     27     27     27     27     27\
     97      3      4      5      5      5      9      9     10     38\
     56     56     57     58     58     58      6      6      6      6\
      6      6      6      6      6      7      7      7      7      7\
      7      7      8      8      8      8     41    113    113    113\
    113    113    113    113    113    113    113    114    114    114\
    114    114    114    114    114    114    114    114    115"

test = test.split("    ")
print(test)
test = list(map(int,test))
print(make_word_seq(test))
print(np.array(starting_point)-1)