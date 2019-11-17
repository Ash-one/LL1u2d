
FIRST = dict()  # FIRST集
FOLLOW = dict()  # FOLLOW集
Grammar = dict()  # 文法
LL1Table = dict()  # 分析表
VT = set()  # 终结符
ProcessList = dict()


def get_lan():
    num = int(input('请输入文法的个数：'))
    print('输入全部文法（ S->A ）:')
    for i in range(num):
        temp = input()
        splitlist = temp[3:].replace("\n", "").split("|")

        Grammar[temp[0]] = splitlist
    print("文法为：", Grammar)



'''
扫描文法中的每一个产生式，对于产生式右边第一个符号不是非终结符的情况，
把右边非终结符First集中的元素加入到左边非终结符的First集中去
如果右边非终结符的First集中包含空串ε，则应找到该非终结符之后的一个非终结符
把这个非终结符First集中的元素加入到左边非终结符的First集中去，此次类推
'''
def get_first():
    for k in Grammar:
        l = Grammar[k]
        FIRST[k] = list()
        for s in l:
            if not (s[0].isupper()):    #在以终结符开始的文法的集合中加入空串
                FIRST[k].append(s[0])
    for i in range(0, 2):
        for k in Grammar:
            l = Grammar[k]
            for s in l:
                if (s[0].isupper()):
                    if '@' in FIRST[s[0]]:
                        for j in s[1:]:
                            if j.isupper():
                                FIRST[k].extend(FIRST[j])
                                FIRST[k] = list(set(FIRST[k]))  # 去重
                    else:
                        FIRST[k].extend(FIRST[s[0]])
                        FIRST[k] = list(set(FIRST[k]))  # 去重
    print("FIRST集为：", FIRST)


def get_follow():
    condition = lambda t: t != '@'  # 过滤器用于过滤空串
    for k in Grammar:  # 新建list
        FOLLOW[k] = list()
        if k == list(Grammar.keys())[0]:
            FOLLOW[k].append('#')
    for i in range(0,2):
        for k in Grammar:
            l = Grammar[k]
            for s in l:
                if s[len(s) - 1].isupper():                  # 判断本句文法A→αB最后一个字符是否是非终结字符
                    FOLLOW[s[len(s) - 1]].extend(FOLLOW[k])  # 若是则把去除空串的FOLLOW(A)加至FOLLOW(B)中
                    FOLLOW[s[len(s) - 1]] = list(filter(condition, FOLLOW[s[len(s) - 1]]))  # 去除空串
                for index in range(0, len(s) - 1):           # 除开最后一个字符每个字符依次判断
                    if s[index].isupper():
                        if s[index + 1].isupper():  # 若A→αBβ是一个产生式，则把FIRST(β)-{ε}加至FOLLOW(B)中；
                            FOLLOW[s[index]].extend(FIRST[s[index + 1]])
                            FOLLOW[s[index]] = list(filter(condition, FOLLOW[s[index]]))  # 去除空串
                        if not (s[index + 1].isupper()) and (s[index + 1] != '@'):
                            FOLLOW[s[index]].append(s[index + 1])
                        emptyflag = 1
                        for i in range(index + 1, len(s)):
                            if not (s[i].isupper()) or (s[i].isupper() and ('@' not in FIRST[s[i]])):
                                emptyflag = 0
                                break
                        if emptyflag == 1:
                            FOLLOW[s[index]].extend(FOLLOW[k])  # A→αBβ是一个产生式而(即ε属于FIRST(β))，则把FOLLOW(A)加至FOLLOW(B)中
                            FOLLOW[s[index]] = list(filter(condition, FOLLOW[s[index]]))  # 去除空串
    for k in FOLLOW:  # 去重
        FOLLOW[k] = list(set(FOLLOW[k]))
    print('FOLLOW集为：', FOLLOW)

def findFirstVN(l:str):
    for i in range(len(l)):
        if l[i].isupper():
            return i
def findLastVN(l:str):
    if len(l)==1 and l[0].isupper():
        return 0
    for i in range(len(l)-1,0,-1):
        if l[i].isupper():
            return i

'''
扫描文法的每一个产生式，
把第一个非终结符的Follow集去除空串ε加入到最后一个非终结符的Follow集中去     
如果最后一个非终结符的First集中有空串ε，
则把第一个非终结符的Follow集去除空串ε加入到倒数第二个非终结符的FOllow集中去，依次类推
'''
def get_follow2():
    get_VT()
    condition = lambda t: t != '@'  # 过滤器用于过滤空串
    for k in Grammar:  # 新建list
        FOLLOW[k] = list()
        if k == list(Grammar.keys())[0]:
            FOLLOW[k].append('#')
    for i in range(0,2):
        for k in Grammar:
            l = Grammar[k]
            for s in l:
                if s not in VT and s!='@':
                    if '@' in FIRST[s[findLastVN(s)]]:
                        try:
                            _list = FOLLOW[s[findFirstVN(s)]].remove('@')
                        except:
                            _list = FOLLOW[s[findFirstVN(s)]]
                        _part = s[:findLastVN(s)]
                        _part2 = s[findLastVN(_part)]
                        print(_part,_part2,_list)
                        FOLLOW[_part2].extend(_list)
                    else:
                        FOLLOW[s[findLastVN(s)]].extend(FOLLOW[s[findFirstVN(s)]])
    print('FOLLOW集为：', FOLLOW)

def get_VT():
    VT.add('#')
    for l in Grammar.values():
        for s in l:
            for c in s:
                if not (c.isupper()) and (c != '@'):
                    VT.add(c)
    print('终结符有：', VT)


def generate_table():
    get_VT()
    for k in Grammar:  # 初始化分析表
        LL1Table[k] = dict()
        for e in VT:
            LL1Table[k][e] = None
    for k in Grammar:
        l = Grammar[k]
        for s in l:
            if s[0].isupper():
                for e in VT:
                    if e in FIRST[s[0]]: LL1Table[k][e] = s
            if s[0] in VT:
                LL1Table[k][s[0]] = s
            if (s[0].isupper() and ('@' in FIRST[s[0]])) or (s == '@'):
                for c in FOLLOW[k]:
                    LL1Table[k][c] = s
    print('分析表为：', LL1Table)


def analyze():
    temp = input('输入句子')
    global a
    inputstr = '#' + temp + '#'
    inputstr = inputstr[1:]
    inputstr = list(inputstr[::-1])
    print(inputstr)
    process = list()
    process.append('#')  # "#"入栈
    process.append(list(Grammar.keys())[0])  # 开始符入栈
    errorflag = 0  # 出错标识
    count = 0  # 插入列表时的索引
    ProcessList.clear()
    ProcessList[count] = (''.join(process), ''.join(inputstr), '\t', 'init')
    while True:
        count += 1
        current = process.pop()
        if current == inputstr[-1] == '#':  # 分析成功结束
            ProcessList[count] = ('句子', '接受', '', '')
            break

        if current in VT and (current == inputstr[-1]):  # 遇到终结符
            inputstr.pop()
            ProcessList[count] = (''.join(process), ''.join(inputstr), '\t', '读取下一个')
            continue

        if inputstr[-1] in VT:  # 判断是不是终结符
            new = LL1Table[current][inputstr[-1]]
        else:
            errorflag = 1
            ProcessList[count] = (''.join(process), ''.join(inputstr), '\t', 'Error:输入不合法！')
            break

        if new == None:  # 没有找到对应产生式
            errorflag = 1
            ProcessList[count] = (''.join(process), ''.join(inputstr), '\t', 'Error:没有找到对应产生式!')
            break

        if new == '@':  # 产生式为空串
            ProcessList[count] = (''.join(process), ''.join(inputstr), current + '->@', '出栈')
            continue

        for c in reversed(new):  # 将产生式入栈
            process.append(c)
        ProcessList[count] = (''.join(process), ''.join(inputstr), current + '->' + ''.join(new), '出栈、入栈')

    if errorflag == 0:
        print("分析成功！")
    else:
        print("分析失败！")

    items = list(ProcessList.items())
    for i in range(len(items)):
        print(items[i][0], end='\t')
        for j in range(len(items[i][1])):
            print(items[i][1][j], end='\t')
        print('\t')
    # print(items)








get_lan()  # 得到文法
get_first()  # 得到FIRST集


get_follow()  # 得到FOLLOW集
generate_table()  # 得到分析表

while 1:
    analyze()  # 对输入字符串进行分析



'''
E->TM
M->+TM|@
T->FN
N->*FN|@
F->i|(E)
'''

'''
(i+i)*i+i*i+i*(i+i)*i*i+i+i*i+(i*i)+(i+i)*i+i*i+i*(i+i)*i*i+i+i*i+(i*i)*(i+i)*i+i*i+i*(i+i)*i*i+i+i*i+(i*i)
'''