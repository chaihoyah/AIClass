num = []
liney = []

f = open('recognized.txt', 'r', encoding='utf-8')
lines = f.readlines()
for idx,line in enumerate(lines):
    if line.find("tst") != -1:
        st = line[:-6]+'rec"\n'
        lines[idx] = st
        num.append(idx)
        liney.append(st)
    if line.find("zero_two") != -1:
        lines[idx] = "zero\n"
f.close()
f = open("recognized.txt", 'w')
f.writelines(lines)
print(lines)

