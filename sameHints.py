from itertools import permutations as perm
from concurrent.futures import ProcessPoolExecutor
import sys

if len(sys.argv) != 3:
    print('input file is none')
    exit(1)

max_process = 20
W, L = int(sys.argv[1]), int(sys.argv[2])
input_directory = "hints/"
output_directory = "result/"
file_id = str(W) + "_" + str(L)
sudoku_file = input_directory + "sudoku" + file_id + ".txt"
hintStr_file = output_directory + "hintStr_" + file_id + ".txt"
sameHintStr_file = output_directory + "sameHintStr_" + file_id + ".txt"

def change(H, a, b, c, d, e, f):
    a_v = H[d] if d in H else None
    b_v = H[e] if e in H else None
    c_v = H[f] if f in H else None

    if a_v:      H[a] = a_v
    elif a in H: del H[a]
    
    if b_v:      H[b] = b_v
    elif b in H: del H[b]

    if c_v:      H[c] = c_v
    elif c in H: del H[c]


def getList(hint):
    pv = [[] for _ in range(9)]
    for p, v in hint.items():
        pv[v].append(chr(p+41))
    
    for i in range(9): 
        pv[i].sort()
    pv.sort()
    
    return pv


def getStr(hint):
    return "|".join(map("".join, getList(hint))) + "|"


def getH(h, s):
    h.clear()
    ks = []
    n = 0
    for i in range(len(s)):
        if s[i] == "|":
            n += 1
        else:
            h[ord(s[i]) - 41] = n


def calcRotate(same_hints):
    def chRotate(c):
        if c == '|': return c
        p = ord(c) - 41
        return chr((8 - p % 9) * 9 + (p // 9) + 41)
    
    def calcReverse(hl):
        for i in range(len(hl)):
            for j in range(len(hl[i])):
                o = ord(hl[i][j]) - 41
                hl[i][j] = chr((o // 9) * 9 + (8 - (o % 9)) + 41)

    h = dict()
    get_hs = set()
    for hs in same_hints:
        h.clear()
        getH(h, hs)
        hint_list = getList(h)
        hint_list = sorted(map(lambda x2: sorted(x2), map(lambda x1: map(chRotate, x1), hint_list)))
        hint_str = "|".join(map("".join, hint_list)) + "|"
        get_hs.add(hint_str)
    return get_hs


def changeRowSameBlock(hints):
    same_hints = set()
    h = dict()
    def changeRowSameBlock_(h, n):
        if n == 9:
            same_hints.add(getStr(h))
            #calcRotate(same_hints, h)
        else:
            for to1, to2, to3 in perm([n, n+1, n+2], 3):
                for i in range(9):
                    change(h, n*9+i, (n+1)*9+i, (n+2)*9+i, to1*9+i, to2*9+i, to3*9+i)
                
                changeRowSameBlock_(h, n+3)

                for i in range(9):
                    change(h, to1*9+i, to2*9+i, to3*9+i, n*9+i, (n+1)*9+i, (n+2)*9+i)
        return
    
    for s in hints:
        getH(h, s)
        changeRowSameBlock_(h, 0)
        
    return same_hints


def changeColSameBlock(hints):
    same_hints = set()
    h = dict()
    def changeColSameBlock_(h, n):
        if n == 9:
            same_hints.add(getStr(h))
            #calcRotate(same_hints, h)
        else:
            for to1, to2, to3 in perm([n, n+1, n+2], 3):
                for i in range(0, 81, 9):
                    change(h, i+n, i+n+1, i+n+2, i+to1, i+to2, i+to3)
                
                changeColSameBlock_(h, n+3)

                for i in range(0, 81, 9):
                    change(h, i+to1, i+to2, i+to3, i+n, i+n+1, i+n+2)
        return
    
    for s in hints:
        getH(h, s)
        changeColSameBlock_(h, 0)
        
    return same_hints


def changeRowBlock(hints):
    same_hints = set()
    h = dict()
    for s in hints:
        getH(h, s)
        for to1, to2, to3 in perm([0, 27, 54], 3):
            for i in range(27):
                change(h, i, 27+i, 54+i, to1+i, to2+i, to3+i)
                
            same_hints.add(getStr(h))
            #calcRotate(same_hints, h)

            for i in range(27):
                change(h, to1+i, to2+i, to3+i, i, 27+i, 54+i)
    
    # print("changeRowBlock", len(hints), len(same_hints))
    
    return same_hints


def changeColBlock(hints):
    same_hints = set()
    h = dict()
    for s in hints:
        getH(h, s)
        for to1, to2, to3 in perm([0, 3, 6], 3):
            for i in range(9):
                for j in range(3):
                    change(h, i*9+j, i*9+j+3, i*9+j+6, i*9+j+to1, i*9+j+to2, i*9+j+to3)
            
            same_hints.add(getStr(h))
            #calcRotate(same_hints, h)

            for i in range(9):
                for j in range(3):
                    change(h, i*9+j+to1, i*9+j+to2, i*9+j+to3, i*9+j, i*9+j+3, i*9+j+6)
    # print("changeColBlock", len(hints), len(same_hints))
    
    return same_hints


def getSameHints(H):
    hint_str = getStr(H)
    same_hints = set([hint_str])
    same_hints = same_hints.union(changeRowSameBlock(same_hints))
    print(len(same_hints))
    same_hints = same_hints.union(changeColSameBlock(same_hints))
    print(len(same_hints))
    same_hints = same_hints.union(changeRowBlock(same_hints))
    print(len(same_hints))
    same_hints = same_hints.union(changeColBlock(same_hints))
    print(len(same_hints))
    same_hints = same_hints.union(calcRotate(same_hints))
    print(len(same_hints))
    return same_hints


def getMinimamHintStr(same_hint):
    min_hint_str = None
    for s in same_hint:
        if min_hint_str == None:
            min_hint_str = s
        else:
            min_hint_str = min(min_hint_str, s)
    return min_hint_str

def getHints(data):
    hint_num = int(data[4])
    hints = dict()
    add = 0
    while data[add] != "(":
        add += 1
    for i in range(hint_num):
        row = int(data[add + i*5 + 1])
        col = int(data[add + i*5 + 2])
        num = int(data[add + i*5 + 3])
        hints[row*9 + col] = num
    return hints


def readFile(file_name):
    datas = []
    with open(file_name, "r") as f:
        for d in f.readlines():
            d = list(map(str, d.split()))
            if int(d[4]) != 17: continue
            datas.append(d)
    return datas


def getMinimum(data):
    hint = getHints(data)
    same_hints = getSameHints(hint)
    mini_hint_str = getMinimamHintStr(same_hints)
    return (mini_hint_str, len(same_hints))


hint_dict = dict()
def sameHint():
    i = 0
    while i < len(datas):
        with ProcessPoolExecutor(max_workers=max_process) as executor:
            for j, hint_str_len in enumerate(executor.map(getMinimum, datas[i:min(i+max_process, len(datas))])):
                hint_str, length = hint_str_len
                if hint_str in hint_dict:
                    hint_dict[hint_str].append(i+j+1)
                else:        
                    hint_dict[hint_str] = [i+j+1]
                    
                with open(hintStr_file, "a") as f:
                    f.write(str(i+1+j) + " " + str(len(hint_dict)) + " " + str(length) + " " + hint_str + " " + " ".join(map(str, hint_dict[hint_str])) + "\n")
        i += j+1


def writeFile():
    same = []
    for k, v in hint_dict.items():
        if len(v) > 1:
            same.append((k, v))

    print("kind", len(hint_dict))
    print("fit num", len(same))

    with open(sameHintStr_file, "w") as f:
        for s, n in same:
            for i in n:
                f.write(str(i) + " ")
            f.write("\n")


datas = readFile(sudoku_file)
sameHint()
print(len(hint_dict))
writeFile()
