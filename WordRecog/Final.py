import numpy as np
import time

f = open("hmm.txt", 'r', encoding='utf-8')
lines = f.readlines()
phones = []
phone_num = 0
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

    state_num = (len(phones)-1)*3 + 1
    ### f부터 시작 f state1 = 0, state2 = 1, ...
    #m = np.zeros((time_len, state_num))
    #m_prime = np.zeros((time_len, state_num))
    m = [[-100000 for col in range(state_num)] for row in range(time_len)]
    m_prime = [[-100000 for col in range(state_num)] for row in range(time_len)]
    seq = np.zeros(time_len)
    for state in range(state_num):
        phone_num, state_idx = find_phone_num(state)
        state_len = len(phones[phone_num])-2 #f 면 3
        m[0][state] = np.log(find_stateprior(phone_num)) + get_obsprob(e_seq[0], phone_num, state_idx+1)
        m_prime[0][state] = -100000
    for time in range(1,time_len):
        for state in range(state_num):
            for i in range(state_num):
                state_phone_num, state_state_num = find_phone_num(state)
                #print(find_transprob(i, state))
                if find_transprob(i,state) != 0:
                    Mij_prob = m[time-1][i] + (np.log(find_transprob(i, state)) ) + get_obsprob(e_seq[time],state_phone_num,state_state_num+1)
                else:
                    Mij_prob = -1*np.inf
                #print(Mij_prob)
                if m[time][state] < Mij_prob:
                    m[time][state] = Mij_prob
                    m_prime[time][state] = i
                    #print(i)
    seq[time_len-1] = int(np.max(m_prime[time_len-1]))
    for t in range(time_len-2,-1, -1):
        seq[t] = m_prime[t][int(seq[t+1])]
    return seq

def find_stateprior(phone_num):
    global phones
    prob_sum = 0
    total_count = 0
    state_len = len(phones[phone_num])-2
    for keyh in word_hmm.keys():
        count = 0
        count += word_hmm[keyh][0].count(phone_num)
        total_count += count
        prob_sum += count*word_hmm[keyh][2]
    for num in range(state_len):
        string = "state"+str(num+1)
        phones[phone_num][string]['prior'] = prob_sum/total_count if total_count != 0 else 0
    return prob_sum/total_count if total_count != 0 else 0

def find_transprob(i , j):
    is_in_word = False
    is_in_bigram = False
    prob = 0
    i_index = 0
    j_index = 0
    phone_num_i,state_num_i = find_phone_num(i)
    phone_num_j,state_num_j = find_phone_num(j)

    if phone_num_i == phone_num_j and state_num_i != 2 and state_num_j != 0:
        prob = phones[phone_num_i]["TP"][state_num_i+1][state_num_j+1]
        if phone_num_i == 20 and state_num_i == 2 and state_num_j == 0:
            prob = phones[phone_num_i]["TP"][3][4]
        return prob

    for keyh in word_hmm.keys():
        if phone_num_i in word_hmm[keyh][0]:
            i_index = word_hmm[keyh][0].index(phone_num_i)
            if i_index == len(word_hmm[keyh][0])-1:
                ###sp or sil일때
                if phone_num_i == 20 and state_num_j == 0:
                    if phones[phone_num_j]["phone"] in ["ey", "f", "n", "ow", "w", "s", "th", "t", "z","sil"]:
                        prob = find_bigram_num(phone_num_i,phone_num_j)
                elif phone_num_i == 17 and state_num_j == 0:
                    if phones[phone_num_j]["phone"] in ["ey", "f", "n", "ow", "w", "s", "th", "t", "z", "sil"]:
                        prob = phones[phone_num_i]["TP"][1][2]*find_bigram_num(phone_num_i, phone_num_j)
            elif i_index == len(word_hmm[keyh][0])-2 and state_num_i == 2 and state_num_j == 0:
                ###끝 phone에서 sp로 or 끝 phone에서 다음 단어 phone
                if phone_num_j == 17:
                    ## sp일때
                    row = 3*(i_index+1)
                    col = 3*(i_index+1)+1
                    prob = word_hmm[keyh][1][row][col]
                elif phones[phone_num_j]["phone"] in ["ey", "f", "n", "ow", "w", "s", "th", "t", "z","sil"]:

                    prob = phones[17]["TP"][0][2] * phones[phone_num_i]["TP"][3][4] * find_bigram_num(phone_num_i,phone_num_j)


            elif phone_num_j == word_hmm[keyh][0][i_index+1]:
                ###단어 내부 연결부위
                is_in_word =True
                if state_num_i == 2 and state_num_j == 0:
                    row = 3*(i_index+1)
                    col = 3*(i_index+1)+1
                    prob = word_hmm[keyh][1][row][col]
    return prob

def find_phone_num(num):
    if num <= 51:
        return int((num-num%3)/3), num%3
    else:
        return int((num-1-(num-1)%3)/3)+1, (num-1)%3

def find_bigram_num(one,two):
    global bigram_list
    prob_sum = 0
    count = 0
    is_s = True
    is_sp = False
    for keyo in list(word_hmm.keys())[1:]:
        is_s = False
        if one == word_hmm[keyo][0][-2]:
            for keyh in word_hmm.keys():
                if two == word_hmm[keyh][0][0]:
                    for i in range(len(bigram_list)):
                        if keyo == bigram_list[i][0] and keyh == bigram_list[i][1]:
                            prob_sum+= bigram_list[i][2]
                            count+=1
                            break

    if is_s and one == word_hmm["<s>"][0][0]:
        for keyh in word_hmm.keys():
            if two == word_hmm[keyh][0][0]:
                for i in range(11):
                    if keyo == bigram_list[i][0] and keyh == bigram_list[i][1]:
                        prob_sum += bigram_list[i][2]
                        count += 1
                        break

    elif one == 17:
        is_sp = True
    if is_sp:
        for idx, b in enumerate(bigram_list):
            if b[0] != "s":
                prob_sum += b[2]
                count += 1


    return (prob_sum/count) if count !=0 else 0

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
    to_phone = []
    word = []
    for idx,i in enumerate(seq):
        n,_ = find_phone_num(i)
        if idx != 0:
            if n != to_phone[-1]:
                to_phone.append(n)
        else:
            to_phone.append(n)
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
                    word.append(keyl)

    return word

start = time.time()
lines_ref = f_ref.readlines()
f_rec.write("#!MLF!#\n")
for idx, line in enumerate(lines_ref[1:-1]):
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
        f_tst.write(str(seq.astype(int))+"\n")
        word_seq = make_word_seq(seq)
        for jj in word_seq:
            f_rec.write(jj+"\n")
        f_rec.write(".\n")
        print("Finished")

print(start-time.time())

f.close()
f_dic.close()
f_uni.close()
f_bi.close()
f_read.close()
f_ref.close()
f_rec.close()