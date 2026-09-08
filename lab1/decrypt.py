'''
给定如下明密文数据流, 中的两个转子和反射器的定义不变, 尝试恢复密钥K1和K2。(结果可能不唯一)
明文:  HELLOWORLD…
密文: …WELLDONEEFGHIJ…

已知K1中接线板的接线数量最多不超过六条;
对于K1中没有信息支撑的接线板情况, 可以考虑使用-1表示未知: 
例如[0,2,1,-1,...]表示A不接线(自身到自身), B与C相连, -1则表示字母D为自由(是否接线且与哪个字母接线未知)。


扰频器组合(固定2个转子, 无需从5个中选择2个)
快速转子QUICK = [0, 18, 24, 12, 10, 20, 8, 6, 14, 2, 11, 15, 22, 3, 25, 7, 17, 13, 5, 1, 23, 9, 16, 21, 19, 4]
即快速转子的表格中左侧一列为0, 1, 2, …, 25, 右侧一列0, 18, 24, …, 4; 下同
中速转子MID = [0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23]

反射器
T = [10, 20, 14, 8, 25, 15, 16, 21, 3, 18, 0, 23, 13, 12, 2, 5, 6, 19, 9, 17, 1, 7, 24, 11, 22, 4]
即a与k相连, b与u相连, ……
'''

import string
from copy import *
def crypt_once(QUICK, MID, SLOW, T, st0, st1, st2, ch):
    """
    在指定三个转子位置下，只加密一个字符。
    不经过接线板 K1，不自动转动转子。
    Args:
        QUICK: 快速转子
        MID:   中速转子
        SLOW:  慢速转子
        T:     反射器
        st0: 快速转子当前位置
        st1: 中速转子当前位置
        st2: 慢速转子当前位置

        ch: 输入字符，如 'A'

    Return:
        加密后的字符，如 'G'
    """

    # A -> 0, B -> 1, ...
    x = ord(ch) - ord('A')

    rotors = [QUICK, MID, SLOW]
    positions = [st0, st1, st2]
    rotor_left = []
    rotor_right = []
    # 根据当前位置旋转三个转子
    for rotor, pos in zip(rotors, positions):
        pos %= 26
        left = list(range(26))
        left = left[pos:] + left[:pos]
        right = rotor[pos:] + rotor[:pos]
        rotor_left.append(left)
        rotor_right.append(right)
    # 过三轮
    for i in range(3):
        x = rotor_right[i].index(
            rotor_left[i][x]
        )
    x = T[x]
    #逆向过三轮
    for i in range(2, -1, -1):
        x = rotor_left[i].index(
            rotor_right[i][x]
        )
    return chr(x + ord('A'))
def find_crib(c,m):
    """
        查找crib
        Args:   
            m: 明文字符串
            c: 密文字符串
        Return:
            cribs: 所有可用cribs    
    """
    
    # find the crib
    cribs = []
    maxl = len(c) - len(m) + 1
    ccount = 0 #密文起始点
    flag = 0
    while(ccount < maxl):
        temp_c = c[ccount : ccount + len(m)]
        ccount = ccount + 1
        for i in range(len(m)):
            if m[i] == temp_c[i]: # 有重复的, 一定不是crib
                flag = 1
                break
        if flag == 0:
            cribs.append(temp_c)
        else:
            flag = 0
    return cribs            


def build_graph(c,m):  #邻接表
    """
        查找crib
        Args:   
            m: 明文字符串
            c: 密文字符串
        Return:
            graph: 用于dfs的图, 边权为位置    
    """
    graph = {}
  # 遍历所有的边
    for l,uv  in  enumerate(zip(c,m)):
        u, v=uv
    # 如果u不在字典中, 就创建一个空列表
        if u not in graph:
            graph[u] = []
    # 把(v, l)这个元组添加到u的邻接列表中, 边权l是边的坐标 坐标就是索引，l=0就是c的第一个字母
        graph[u].append((v, l))
    for l, uv in  enumerate(zip(m,c)):
        u, v=uv  
    # 如果u不在字典中, 就创建一个空列表
        if u not in graph:
            graph[u] = []
    # 把(v, l)这个元组添加到u的邻接列表中, 边权l是边的坐标
        graph[u].append((v, l))
  # 返回字典
    return graph


def dfs(graph,pos,st,path,locs): # 从左到右依次为构建的无向图, 输入位置字符, 开始位置字符和坐标, 路径, 记录的环路构成边的坐标
    """
        查找crics
        Args:   
            graph: build graph得到的图
            pos: 当前遍历的字符
            st:开始位置字符和坐标
            path:路径
            locs:记录的环路构成边的坐标
        Return:
            ans: 所有可用crics    
    """

    ans=[]
    for i,l in graph[pos]:
        if i in path :
            tmp=(path[path.index(i):]+[i],locs[path.index(i):]+[l])
            if len(set(tmp[1]))>=2 and st[0] not in tmp[0][1:-1] and tmp[1][-1]==st[1]:
                ans+=[(tuple(tmp[0]),tuple(tmp[1]))]
            continue
        ans+=dfs(graph,i,st,path+[i],locs+[l])
    return ans



QUICK = [7, 19, 3, 22, 11, 25, 14, 1, 16, 23, 8, 20, 5, 17, 12, 9, 24, 6, 15, 2, 18, 21, 4, 13, 10, 0]
MID = [0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23]
SLOW = [0, 23, 5, 12, 18, 3, 21, 9, 14, 1, 17, 6, 24, 11, 20, 4, 15, 8, 22, 7, 19, 13, 2, 16, 10, 25]
T = [5, 3, 7, 1, 8, 0, 9, 2, 4, 6, 12, 14, 10, 15, 11, 13, 18, 20, 16, 21, 17, 19, 24, 25, 22, 23]

if __name__=="__main__": 
    m="WETTERVORHERSAGEHEUTE"
    c="EWGZDSATLWNEDBBCJUNGW"
    cribs=find_crib(c,m)
    print("总的crib数量: ", len(cribs))
    for crib in cribs:
        print()
        print("当前crib为: ", crib)
        ans=set()  # 保存当前crib中包含的所有环路
        graph=build_graph(crib,m)
        visited=[0]*len(m)
        for i in range(len(m)):
            if visited[i]==1:
                continue    
            ansi=dfs(graph,m[i],(m[i],i),[m[i]],[])
            for find_ins in ansi:
                for loc in find_ins[1]: # 防止重复计算
                    visited[loc]=1    
            ans|=set(ansi)        
        print("当前crib包含的所有环路有: ", ans)
        for QUICK, MID, SLOW in [(QUICK, MID, SLOW),
                                 (QUICK, SLOW, MID),
                                 (MID, QUICK, SLOW),
                                 (MID, SLOW, QUICK),
                                 (SLOW, QUICK, MID),
                                 (SLOW, MID, QUICK)]:
            print("当前扰频器组合为: ", (QUICK, MID, SLOW))
            print("当前扰频器组合下的环路有: ", ans)
            guess_all_K2 = {(i, j, k) for i in range(26) for j in range(26) for k in range(26)} # 从所有备选中进行筛选
            guess={}
            for case in ans:
                guess_case={}
                for i in range(26):
                    for j in range(26):
                        for k in range(26):
                            #这里要保存所有路径
                            paths = []
                            for check in string.ascii_uppercase: #枚举所有字母，亮灯
                                trans=check #注意这个check就是已经过了接线板的
                                path=[trans]
                                for z in case[1]:
                                    trans=crypt_once(QUICK,MID,SLOW,T,(i-z)%26,j,k,trans)
                                    path.append(trans) 
                                if trans==check:
                                    paths.append(path)  
                            if len(paths)>0:
                                guess_case[(i,j,k)]=paths #保存所有路径
                guess_all_K2&=set(guess_case) #每个环路会有一个guess_case,得到很多ijk，然后取交集
                guess[case]=guess_case   #guess[case]是一个字典，guess[case][(i,j,k)]=path
            print("通过环路猜测的K2密钥个数: ")    
            print(len(guess_all_K2))      
                           
            #每个环都有很多路径，得有回溯搜索
            def merge_K1(K1, chars, path):
                """
                尝试把当前环的 path 合并进 K1
                有冲突返回 None
                """
                new_K1 = deepcopy(K1)
                for real, pluged in zip(chars, path):
                    # real -> pluged
                    if real in new_K1:
                        if new_K1[real] != pluged:
                            return None
                    else:
                        new_K1[real] = pluged
                    # pluged -> real
                    if pluged in new_K1:
                        if new_K1[pluged] != real:
                            return None
                    else:
                        new_K1[pluged] = real
                return new_K1
            def search_K1(cases, guess, K2, idx=0, K1=None):
                if K1 is None:
                    K1 = {}
                # 所有环都处理完
                if idx == len(cases):
                    return [K1]
                case = cases[idx]
                results = []
                # 当前环可能有多个闭环 path
                for path in guess[case][K2]:
                    new_K1 = merge_K1(K1,case[0],path)
                    if new_K1 is not None:
                        results += search_K1(cases,guess,K2,idx + 1,new_K1)
                return results                 
            guess_K2_K1 = {}
            cases = list(ans)
            for guess_K2 in guess_all_K2:
                K1_candidates = search_K1(cases,guess,guess_K2)
                if K1_candidates:
                    guess_K2_K1[guess_K2] = K1_candidates
            print("通过环路及与环路相关的接线板设置无冲突, 猜测的K2密钥个数: ")    
            print(len(guess_K2_K1))
              
            print("其中接线板总数不超过6条的密钥为: ")
            for guess in guess_K2_K1:
                count=0
                guess_K1=guess_K2_K1[guess][0]  
                K1=[-1]*26      # -1代表现有信息无法支撑获取该位置的接线板情况
                for i in guess_K1:
                    if guess_K1[i]!=i:         
                        count+=1
                    K1[ord(i)-ord("A")]=ord(guess_K1[i])-ord("A")
                if count/2>6:
                    continue
                print(guess,K1,"接线板条数",count//2)
                        
