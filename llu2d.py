
class LL1u2d():
    def __init__(self):
        self.Grammar = {}  # 文法
        self.FIRST = {}  # FIRST集
        self.FOLLOW = {}  # FOLLOW集

        self.AnalyzeTable = {}  # 分析表
        self.VT = set()  # 终结符
        self.steps = {}

        self.get_GRAMMA()
        self.get_FIRST()
        self.get_FOLLOW()
        self.get_table()

    def get_GRAMMA(self):
        num = int(input('输入文法总数：'))
        print('输入全部文法（ S->A ）:')
        for i in range(num):
            temp = input()
            splitlist = temp[3:].replace("\n", "").split("|")
            self.Grammar[temp[0]] = splitlist

        print('文法：')

        for item in self.Grammar:
            print(item,self.Grammar[item])

    def get_FIRST(self):
        for key in self.Grammar:
            contents = self.Grammar[key]
            self.FIRST[key] = list()
            for _string in contents:
                if not (_string[0].isupper()):    #在以终结符开始的文法的集合中加入该终结符
                    self.FIRST[key].append(_string[0])
        for i in range(0, 2):
            for key in self.Grammar:
                contents = self.Grammar[key]
                for _string in contents:
                    if (_string[0].isupper()):
                        if '@' in self.FIRST[_string[0]]:
                            # 如果右边非终结符的First集中包含空串ε，则应找到该非终结符之后的一个非终结符
                            # 把这个非终结符First集中的元素加入到左边非终结符的First集中去，
                            for j in _string[1:]:
                                if j.isupper():
                                    self.FIRST[key].extend(self.FIRST[j])
                                    self.FIRST[key] = list(set(self.FIRST[key]))
                        else:
                            # 对于产生式右边第一个符号不是非终结符的情况，
                            # 把右边非终结符First集中的元素加入到左边非终结符的First集中去
                            self.FIRST[key].extend(self.FIRST[_string[0]])
                            self.FIRST[key] = list(set(self.FIRST[key]))

        for item in self.FIRST:
            print('FIRST('+item+')', self.FIRST[item])

    def get_FOLLOW(self):
        condition = lambda t: t != '@'  # 过滤器用于过滤空串
        for key in self.Grammar:  # 新建list
            self.FOLLOW[key] = list()
            if key == list(self.Grammar.keys())[0]:
                self.FOLLOW[key].append('#')
        for i in range(0,2):
            for key in self.Grammar:
                contents = self.Grammar[key]
                for _string in contents:
                    if _string[len(_string) - 1].isupper():
                        # 判断本句文法A→aB最后一个字符是否是非终结字符
                        self.FOLLOW[_string[len(_string) - 1]].extend(self.FOLLOW[key])
                        # 若是则把去除空串的FOLLOW(A)加至FOLLOW(B)中
                        self.FOLLOW[_string[len(_string) - 1]] = list(filter(condition, self.FOLLOW[_string[len(_string) - 1]]))

                    for index in range(0, len(_string) - 1):
                        # 除开最后一个字符每个字符依次判断
                        if _string[index].isupper():
                            if _string[index + 1].isupper():  # αBC，把FIRST(C)-{ε}加至FOLLOW(B)中；
                                self.FOLLOW[_string[index]].extend(self.FIRST[_string[index + 1]])
                                self.FOLLOW[_string[index]] = list(filter(condition, self.FOLLOW[_string[index]]))  # 去除空串
                            if not (_string[index + 1].isupper()) and (_string != '@'): # 若A→aBb是一个产生式，则把b加至FOLLOW(B)中；
                                self.FOLLOW[_string[index]].append(_string[index + 1])

                            # 判断是否需要将左侧加入右侧
                            emptyflag = 1
                            for i in range(index + 1, len(_string)):
                                if not (_string[i].isupper()) or (_string[i].isupper() and ('@' not in self.FIRST[_string[i]])):
                                    # 如果满足该位是终结符或该位非终结符的FIRST集有空串
                                    emptyflag = 0
                                    break
                            if emptyflag == 1:
                                self.FOLLOW[_string[index]].extend(self.FOLLOW[key])
                                # A→aBC是一个产生式而(即ε属于FIRST(C))，则把FOLLOW(A)加至FOLLOW(B)中,左侧加入右侧
                                self.FOLLOW[_string[index]] = list(filter(condition, self.FOLLOW[_string[index]]))  # 去除空串
            for key in self.FOLLOW:  # 去重
                self.FOLLOW[key] = list(set(self.FOLLOW[key]))
        for item in self.FOLLOW:
            print('FOLLOW(' + item + ')', self.FOLLOW[item])

    def get_VT(self):
        self.VT.add('#')
        for values in self.Grammar.values():
            for i in values:
                for j in i:
                    if not (j.isupper()) and (j != '@'):
                        self.VT.add(j)
        # print('终结符有：', self.VT)

    def get_table(self):
        self.get_VT()
        for key in self.Grammar:  # 初始化分析表
            self.AnalyzeTable[key] = {}
            for e in self.VT:
                self.AnalyzeTable[key][e] = None
        for key in self.Grammar:
            contents = self.Grammar[key]
            for _string in contents:
                if _string[0].isupper():
                    for e in self.VT:
                        if e in self.FIRST[_string[0]]:
                            self.AnalyzeTable[key][e] = _string
                if _string[0] in self.VT:
                    self.AnalyzeTable[key][_string[0]] = _string
                if (_string[0].isupper() and ('@' in self.FIRST[_string[0]])) or (_string == '@'):
                    for c in self.FOLLOW[key]:
                        self.AnalyzeTable[key][c] = _string
        # print('分析表为：', self.AnalyzeTable)
        for item in self.AnalyzeTable:
            print('AnalyzeTable('+item+')',self.AnalyzeTable[item])

    def analyze(self):
                temp = input('输入句子')
                inputstr = '#' + temp + '#'
                inputstr = inputstr[1:]
                inputstr = list(inputstr[::-1])
                print(inputstr)
                AnalyzeStack = list()
                AnalyzeStack.append('#')  # "#"入栈
                AnalyzeStack.append(list(self.Grammar.keys())[0])  # 开始符入栈
                error_flag = 0  # 出错标识
                count = 0  # 插入列表时的索引
                self.steps.clear()
                self.steps[count] = (''.join(AnalyzeStack), ''.join(inputstr), '\t', 'init')
                while True:
                    count += 1
                    cur = AnalyzeStack.pop()
                    if cur == inputstr[-1] == '#':  # 分析成功结束
                        self.steps[count] = ('句子', '接受', '', '')
                        break

                    if cur in self.VT and (cur == inputstr[-1]):  # 遇到终结符
                        inputstr.pop()
                        self.steps[count] = (''.join(AnalyzeStack), '\t'+''.join(inputstr), '\t', '读取下一个')
                        continue

                    if inputstr[-1] in self.VT:  # 判断是不是终结符
                        new = self.AnalyzeTable[cur][inputstr[-1]]
                    else:
                        error_flag = 1
                        self.steps[count] = (''.join(AnalyzeStack), '\t'+''.join(inputstr), '\t', 'Error:输入不合法！')
                        break

                    if new == None:  # 没有找到对应产生式
                        error_flag = 1
                        self.steps[count] = (''.join(AnalyzeStack), '\t'+''.join(inputstr), '\t', 'Error:没有找到对应产生式!')
                        break

                    if new == '@':  # 产生式为空串
                        self.steps[count] = (''.join(AnalyzeStack), '\t'+''.join(inputstr), '\t'+cur + '->@', '出栈')
                        continue

                    for c in reversed(new):  # 将产生式入栈
                        AnalyzeStack.append(c)
                    self.steps[count] = (''.join(AnalyzeStack), '\t'+''.join(inputstr), '\t'+cur + '->' + ''.join(new), '出栈、入栈')

                if error_flag == 0:
                    print("分析成功！")
                else:
                    print("分析失败！")

                items = list(self.steps.items())
                for i in range(len(items)):
                    print(items[i][0], end='\t')
                    for j in range(len(items[i][1])):
                        print(items[i][1][j], end='\t')
                    print('\t')
                # print(items)



'''
E->TM
M->+TM|@
T->FN
N->*FN|@
F->i|(E)
'''

if __name__ == '__main__':
    a = LL1u2d()
    a.analyze()


