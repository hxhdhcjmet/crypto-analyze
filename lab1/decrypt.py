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

crypt_once=lambda Q,M,st0,st1,m:chr((Q[(((M[((T[((M.index((((Q.index((ord(m)-ord("A")+st0)%26)-st0)%26)+st1)%26)-st1)%26)]+st1)%26)]-st1)%26+st0)%26)]-st0)%26+ord("A"))

from copy import *

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



QUICK = [0, 18, 24, 12, 10, 20, 8, 6, 14, 2, 11, 15, 22, 3, 25, 7, 17, 13, 5, 1, 23, 9, 16, 21, 19, 4]
MID = [0, 10, 4, 2, 8, 1, 18, 20, 22, 19, 13, 6, 17, 5, 9, 3, 24, 14, 12, 25, 21, 11, 7, 16, 15, 23]
T = [10, 20, 14, 8, 25, 15, 16, 21, 3, 18, 0, 23, 13, 12, 2, 5, 6, 19, 9, 17, 1, 7, 24, 11, 22, 4]


if __name__=="__main__": 
    m="HELLOWORLD"
    c="WELLDONEEFGHIJ"
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
        
        guess_all_K2=set(sum([[(i,j) for i in range(26)] for j in range(26)],[])) # 从所有备选中进行筛选
        guess={}
        for case in ans:
            guess_case={}
            for i in range(26):
                for j in range(26):
                    for check in string.ascii_uppercase:
                        trans=check
                        path=[trans]
                        for k in case[1]:
                            trans=crypt_once(QUICK,MID,i-k,j,trans)
                            path.append(trans)
                        if trans==check:
                            guess_case[(i,j)]=(path)
                            break
            guess_all_K2&=set(guess_case)
            guess[case]=guess_case
        print("通过环路猜测的K2密钥个数: ")    
        print(len(guess_all_K2))      
                      
        guess_K2_K1={}                       
        for guess_K2 in guess_all_K2:
            K1={}
            flag=True    
            for case in ans:
                keychar=case[0]
                for real,pluged in zip(case[0],guess[case][guess_K2]): # real是环路中被观测的值, pluged是过接线板后的值
                    if real not in K1:
                        K1[real]=pluged
                    elif K1[real]!=pluged:
                        flag=False
                        break
                    if pluged not in K1:
                        K1[pluged]=real
                    elif K1[pluged]!=real:
                        flag=False
                        break
                if flag==False:
                    break
            if flag:
                guess_K2_K1[guess_K2]=K1
        print("通过环路及与环路相关的接线板设置无冲突, 猜测的K2密钥个数: ")    
        print(len(guess_K2_K1))
        
        final_guess={}
        for K2 in guess_K2_K1:
            K1_now=deepcopy(guess_K2_K1[K2])
            flag=True
            ok=True
            locs=set([i for i in range(len(m))])
            while flag and ok:
                flag=False
                for loc,pair in enumerate(zip(crib,m)):
                    known=set(pair)&set(K1_now)
                    if len(known)>=1:
                        locs-=set([loc])
                    if len(known)==1:
                        flag=True
                        unknown_char=list(set(pair)-known)[0]
                        known_char=list(known)[0]
                        pluged_unknown_char=crypt_once(QUICK,MID,K2[0]-(loc%26),K2[1]-(loc//26),K1_now[known_char])
                        if pluged_unknown_char not in K1_now:
                            K1_now[pluged_unknown_char]=unknown_char
                            K1_now[unknown_char]=pluged_unknown_char
                        else :
                            ok=False
            if ok:
                final_guess[K2]=(K1_now)
        print("通过环路及所有可能的接线板无冲突, 猜测的K2密钥个数: ")
        print(len(final_guess))    
        print("其中接线板总数不超过6条的密钥为: ")
        for guess in final_guess:
            count=0
            guess_K1=final_guess[guess]  
            K1=[-1]*26      # -1代表现有信息无法支撑获取该位置的接线板情况
            for i in guess_K1:
                if guess_K1[i]!=i:         
                    count+=1
                K1[ord(i)-ord("A")]=ord(guess_K1[i])-ord("A")
            if count/2>6:
                continue
            print(guess,K1,"接线板条数",count//2)
                    
