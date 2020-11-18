import numpy as np
import random
import os
# import pandas
# import matplotlib.pyplot as plt
# import scipy.special as sps
import copy

M = 25600000


# DijkStra路由算法
def Dijkstra(G,s,d):
    # print("Start Dijstra Path……")
    path=[]
    n=len(G)
    fmax=999
    w=[[0 for i in range(n)]for j in range(n)]
    book=[0 for i in range(n)]
    dis=[fmax for i in range(n)]
    book[s-1]=1#节点编号从1开始，列表序号从0开始
    midpath=[-1 for i in range(n)]#上一跳列表
    for i in range(n):
        for j in range(n):
            if G[i][j]!=0:
                w[i][j]=G[i][j]#0→max
            else:
                w[i][j]=fmax
            if i==s-1 and G[i][j]!=0:#直连的节点最小距离就是network[i][j]
                dis[j]=G[i][j]

    for i in range(n-1):#n-1次遍历，除了s节点
        min=fmax
        u=0
        for j in range(n):
            if book[j]==0 and dis[j]<min:#如果未遍历且距离最小
                min=dis[j]
                u=j
        book[u]=1
        for v in range(n):#u直连的节点遍历一遍
            if dis[v]>dis[u]+w[u][v]:
                dis[v]=dis[u]+w[u][v]
                midpath[v]=u+1#上一跳更新
    j=d-1#j是序号
    path.append(d)#因为存储的是上一跳，所以先加入目的节点d，最后倒置
    while(midpath[j]!=-1):
        path.append(midpath[j])
        j=midpath[j]-1
    path.append(s)
    path.reverse()#倒置列表
    # print(path)
    #print(midpath)
    # print(dis)
    return path


# 选择性迭代DijkStra路由算法
def O_Dijkstra(G,s,d):#迪杰斯特拉算法算s-d的最短路径，并返回该路径和代价
    # print("Start Dijstra Path……")
    path=[]#s-d的最短路径
    n=len(G)#邻接矩阵维度，即节点个数
    fmax=999
    w=[[0 for i in range(n)]for j in range(n)]#邻接矩阵转化成维度矩阵，即0→max
    book=[0 for i in range(n)]#是否已经是最小的标记列表
    dis=[fmax for i in range(n)]#s到其他节点的最小距离
    book[s-1]=1#节点编号从1开始，列表序号从0开始
    midpath=[-1 for i in range(n)]#上一跳列表
    for i in range(n):
        for j in range(n):
            if G[i][j]!=0:
                w[i][j]=G[i][j]#0→max
            else:
                w[i][j]=fmax
            if i==s-1 and G[i][j]!=0:#直连的节点最小距离就是network[i][j]
                dis[j]=G[i][j]
       
    if s<d:   
        for i in range(n-1):#n-1次遍历，除了s节点
            min=fmax
            u=0
            for j in range(n):
                if book[j]==0 and dis[j]<min:#如果未遍历且距离最小
                    min=dis[j]
                    u=j
            book[u]=1
            for v in range(n):#u直连的节点遍历一遍
                if dis[v]>dis[u]+w[u][v]:
                    dis[v]=dis[u]+w[u][v]
                    midpath[v]=u+1#上一跳更新
                    if midpath.count(u+1)==2:
                        dis[u]+=1
                        w[midpath[u]-1][u]+=1
                        w[u][midpath[u]-1]+=1
               
    if s>d:
        for i in range(n-1):#n-1次遍历，除了s节点
            min=fmax
            u=0
            for j in range(n-1,-1,-1):
                if book[j]==0 and dis[j]<min:#如果未遍历且距离最小
                    min=dis[j]
                    u=j
            book[u]=1
            for v in range(n-1,-1,-1):#u直连的节点遍历一遍
                if dis[v]>dis[u]+w[u][v]:
                    dis[v]=dis[u]+w[u][v]
                    midpath[v]=u+1#上一跳更新
                    if midpath.count(u+1)==2:
                        dis[u]+=1
                        w[midpath[u]-1][u]+=1
                        w[u][midpath[u]-1]+=1
   
    j=d-1#j是序号
    path.append(d)#因为存储的是上一跳，所以先加入目的节点d，最后倒置
    while(midpath[j]!=-1):
        path.append(midpath[j])
        j=midpath[j]-1
    path.append(s)
    path.reverse()#倒置列表
    return path


# 根据original变量的值来决定调用哪个DijkStra路由算法；；True时，调用的是Dijkstra路由算法，False时，调用的是选择性迭代Dijkstra路由算法
def Generate_router_tabel(G,original):
    all_table = {}
    n = len(G)
    for i in range(1,n+1):
        table = {}
        for j in range(1,n+1):
            if i == j:
                continue 
            if original:
                path = Dijkstra(G,i,j)
            else:
                path = O_Dijkstra(G,i,j)
            # print(path)
            # for node in range(len(path)-1):
            #     start = path[node]-1
            #     end = path[node+1]-1
            #     # G[start][end] += 1
            #     # G[end][start] += 1
            table[j] = path
        all_table[i] = table

    # print(all_table)
    # print(G)
    return all_table

def Generate_random_data_pair(number):
    pair_list = []
    flow = Gamma_flow(3.10338, 85.2079072, number)
    all_flow = 0 
    for i in range(number*2):
        pair = [random.randint(1,54), random.randint(1,54)]  # 流的起始节点与终止节点
        if pair[1] == pair[0] or pair in pair_list:
            continue
        pair_list.append(pair)
        if len(pair_list) == number:           # 总共会产生number对的数据
            break
    for i in range(number):
        all_flow += flow[i]
        pair_list[i] = [pair_list[i],flow[i]]

    print(pair_list,len(pair_list))
    print('all flow : ',all_flow)

    return pair_list,all_flow

def Gamma_flow(shape, scale, number):
    s=np.random.gamma(shape,scale,25600)             #伽马分布，shape和scale不是指范围，指的是形状参数和指数参数，生成25600个小数  https://blog.csdn.net/weixin_43400774/article/details/90345425
    # count, bins, ignored = plt.hist(s, 50, normed=True)#50： 是50个条形图
    # y = bins**(shape-1)*(np.exp(-bins/scale)/(sps.gamma(shape)*scale**shape))
    # plt.plot(bins, y, linewidth=2, color='r')
    # plt.show()
    s = s.tolist()
    s.sort()
    flow=[]
    flow.append(s[0])
    factor = int(25600/(number - 1))
    for i in range(1,number-1):
        flow.append(s[ i * factor])
    flow.append(s[-1])               # s[-1]表示列表中的最后一位
    return flow

def Network_flow(G,number,weight,original):

    # all_table通过使用Dijkstra计算得到的路由表；
    all_table = Generate_router_tabel(G,original)

    pair_list,all_flow = Generate_random_data_pair(number)
    # print('pair list',pair_list)
    # print('all table',all_table)
    # return
    temp_weight = copy.deepcopy(weight)
    new_pair_list = copy.deepcopy(pair_list)
    for pair in pair_list:
        start = pair[0][0]  # 源卫星节点
        end = pair[0][1]    # 目的卫星节点
        flow = pair[1]      # 这对流的流大小

        temp = all_table[start]
        routing = temp[end]
        temp_point = routing[1]

        while temp_point != end:   # temp_point是中转节点
            # print(start,temp_point,end)
            # print(start,point,flow,weight[start-1][point-1])
            weight[start-1][temp_point-1] -= flow
            weight[temp_point-1][start-1] -= flow
            start = temp_point
            temp_point = all_table[temp_point][end][1]

    current_flow = np.array(weight)         # 剩余的带宽
    # print(current_flow)

    congestion_pair_list = []
    for i in range(current_flow.shape[0]):
        a = np.array(current_flow[i])
        temp = np.where( a < 2560*0.05)   # 剩余带宽小于5％，则认为是拥塞
        # print(temp[0])
        for j in temp[0]:
            if i==j:
                continue
            pair = [i+1,j+1]
            temp_pair = [j+1,i+1]
            if temp_pair in congestion_pair_list:
                continue
            # print(pair)
            congestion_pair_list.append(pair)
    # congestion_pair_list = list(set(congestion_pair_list))
    congestion_pair_list.sort()
    # print(congestion_pair_list)
    return congestion_pair_list,all_flow

def drawPillar(D_dict,D_O_dict):   
      
    x = range(20,35,1)
    print(D_dict,D_O_dict)
    y_1 = []
    y_2 = []
    for item1 in D_dict:
        item2 = item1[1]
        pair = 0
        for key_num in item2.keys():
            news = item2[key_num]
            pair += news[0]
        pair /= 100.0
        print(pair)
        y_1.append(pair)
    print(y_1)

    for item1 in D_O_dict:
        item2 = item1[1]
        pair = 0
        for key_num in item2.keys():
            news = item2[key_num]
            pair += news[0]
        pair /= 100.0
        print(pair)
        y_2.append(pair)
    print(y_2)
    
    # #设置图形大小
    # # plt.figure(figsize=(20,10),dpi=100)
    # plt.xlabel('业 务 流 个 数',fontsize=16)
    # plt.ylabel('平 均 拥 塞 链 路 个 数',fontsize=16)
    # plt.plot(x,y_1,label="Dijkstra算法",color="r")
    # plt.plot(x,y_2,label="选择性迭代最短路径算法",color="b",linestyle="--")
    # _xtick_labels = ["{}".format(i) for i in x]
    #
    # plt.xticks(x,_xtick_labels)
    #
    # plt.grid(alpha=2,linestyle=':')
    # # plt.legend(handles = [l1, l2], labels = ['a', 'b'], loc = 'best',prop=myfont)
    #
    #
    # plt.legend( loc = 'upper left',fontsize=15)
    # # plt.legend('\fontsize {10}')
    # # plt.title('Gamma Distribution')
    # plt.show()


    return y_1,y_2

def sortedDictValues2(adict): 
    keys = adict.keys() 
    keys.sort() 
    return [dict[key] for key in keys] 
    


if __name__ == '__main__':
        # 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54
    G =  [[0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [1, M, M, M, M, M, M, 1, 0, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, 0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, 1, 1, M, M, M, M, M, M, 1, 0, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 1, M, M, M, M, M, M, 1, 0, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 1, M, M, M, M, M, M, 1, 0, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 1, M, M, M, M, M, M, 1, 0, M, M, M, M, M, M, M, M, 1],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 0, 1, M, M, M, M, M, M, 1],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, 1, 0, 1],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, 1, M, M, M, M, M, M, 1, 0]]

    weight=  [[0, 2560, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [2560, M, M, M, M, M, M, 2560, 0, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, 0, 2560, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, 2560, 2560, M, M, M, M, M, M, 2560, 0, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 0, 2560, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 2560, M, M, M, M, M, M, 2560, 0, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 0, 2560, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 2560, M, M, M, M, M, M, 2560, 0, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 0, 2560, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, 2560, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 2560, M, M, M, M, M, M, 2560, 0, M, M, M, M, M, M, M, M, 2560],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 0, 2560, M, M, M, M, M, M, 2560],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 0, 2560, M, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560, M],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, M, M, M, M, 2560, 0, 2560],
         [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, 2560, M, M, M, M, M, M, 2560, 0]]

    # all_table = Generate_router_tabel(G, True)
    # print(all_table)

    original_result = {}
    for i in range(0,15):         # i取值0-14
        a = {}
        for j in range(0,100):    # j取值0-99
            
            temp_weight = copy.deepcopy(weight)          # 将权重这个二维矩阵复制一份用于操作
            congestion_pair_list,all_flow = Network_flow(G, 20+i, temp_weight, True)
            del temp_weight                              # 操作过后将weight的复制品删除

            a[j] =[len(congestion_pair_list),all_flow]

        original_result[20+i] = a
    # 使用DijkStra路由算法得到的result
    original_result = sorted(original_result.items(), key=lambda v: v[0])


    result = {}
    for i in range(0, 15):
        a = {}
        for j in range(0,100):
            temp_weight = copy.deepcopy(weight)           # 将权重复制一份
            congestion_pair_list,all_flow = Network_flow(G,20+i,temp_weight,False)
            del temp_weight
            a[j] =[len(congestion_pair_list),all_flow]
        result[20+i] = a
    # 使用选择性迭代DijkStra路由算法得到的result
    result = sorted(result.items(), key = lambda v: v[0])
    # print(result)


    # from pylab import *
    # mpl.rcParams['font.sans-serif'] = ['SimHei']
    # import matplotlib.pyplot as plt


    drawPillar(original_result, result)

