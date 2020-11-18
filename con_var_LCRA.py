import numpy as np
import random
import os
# import pandas
# import matplotlib.pyplot as plt
# import scipy.special as sps
import copy

M = 25600000


# 返回  number数量对  [[s_id, d_id], flow] 以及 all_flow
def Generate_random_data_pair(number):
    pair_list = []
    flow = Gamma_flow(3.10338,85.2079072,number)
    all_flow = 0 
    for i in range(number*2):
        pair = [random.randint(1,54),random.randint(1,54)]
        if pair[1] == pair[0] or pair in pair_list:
            continue
        pair_list.append(pair)
        if len(pair_list) == number:
            break
    for i in range(number):
        all_flow += flow[i]
        pair_list[i] = [pair_list[i],flow[i]]
    # print(pair_list,len(pair_list))
    # print('all flow',all_flow)
    return pair_list,all_flow


# 返回number个伽马分布的流
def Gamma_flow(shape,scale,number):
    s=np.random.gamma(shape,scale,25600)#在2.到2.之间随机生成2560个小数
    # count, bins, ignored = plt.hist(s, 50, normed=True)#50：是50个条形图
    # y = bins**(shape-1)*(np.exp(-bins/scale)/(sps.gamma(shape)*scale**shape))
    # plt.plot(bins, y, linewidth=2, color='r')
    # plt.show()
    s=s.tolist()
    s.sort()
    flow=[]
    flow.append(s[0])
    factor = int(25600/(number-1))
    for i in range(1,number-1):
        flow.append(s[i*factor])
    flow.append(s[-1])
    return flow


# LCRA 路由算法，  直接返回的 router_list 就是源于目的节点的路由表
def Generate_router(start, end):
    # 没有星间链路的高纬度卫星
    high_lat = [1,2,10,11,19,20,28,29,37,38,46,47,5,6,14,15,23,24,32,33,41,42,50,51]

    # c_k轨道，c_r在轨道上的数量；d_k轨道，d_r在轨道上的数量；
    c_k = int((start - 1) / 9)
    c_r = start % 9 if start % 9 != 0 else 9
    d_k = int((end - 1) / 9)
    d_r = end % 9 if end % 9 != 0 else 9
    # print(c_k, c_r, d_k, d_r)

    # 记录路由走过的路径
    router_list = [start]
    i = 0

    while start != end:
        # print(c_k,c_r,d_k,d_r)
        if c_k != d_k and c_r == d_r:               # 一、不同轨道 同一水平线
            if start not in high_lat:               # （1）非极区：源 < 目的，直接右移 ； 源 > 目的，直接左移
                if c_k < d_k:
                    start = (c_k + 1) * 9 + c_r
                    router_list.append(start)
                else:
                    start = (c_k - 1) * 9 + c_r
                    router_list.append(start)            
            else:                                   # （2）极区：上移非极区则上移，下移非极区则下移
                if (c_r + 1) % 9 + c_k * 9 not in high_lat:
                    start = c_k * 9 + c_r + 1
                    router_list.append(start)
                else:
                    if (c_r - 1) % 9 == 0:
                        start = c_k * 9 + 9
                        router_list.append(start)
                    else:
                        start = c_k * 9 + c_r - 1
                        router_list.append(start)

        if c_k == d_k and c_r != d_r:              # 二、同一轨道 不同水平线
            if abs(c_r - d_r) > 4:
                if c_r < d_r:
                    if (c_r - 1) % 9 == 0:
                        start = c_k * 9 + 9
                        router_list.append(start)
                    else:
                        start = c_k * 9 + c_r - 1
                        router_list.append(start)
                else:
                    if c_r % 9 == 0:
                        start = c_k * 9 + 1
                        router_list.append(start)
                    else:
                        start = c_k * 9 + c_r + 1
                        router_list.append(start)                        
            else:
                if c_r < d_r:
                    start = c_k * 9 + c_r + 1
                    router_list.append(start)
                else:
                    start = c_k * 9 + c_r - 1
                    router_list.append(start)

        if c_k != d_k and c_r != d_r:                # 三、不同轨道 不同水平线
            if abs(c_r - d_r) > 4 and start in high_lat and end in high_lat:
                if c_r < d_r:
                    start = c_k * 9 + (c_r + 1) 
                    router_list.append(start)
                else:
                    start = c_k * 9 + (c_r - 1) 
                    router_list.append(start)
            elif abs(c_r - d_r) < 2 and start in high_lat and end in high_lat:
                if c_r in [1,5]: 
                    if (c_r - 1) % 9 == 0:                   
                        start = c_k * 9 + 9
                        router_list.append(start)
                    else:
                        start = c_k * 9 + (c_r + 1) 
                        router_list.append(start)
                else:
                    start = c_k * 9 + (c_r - 1) 
                    router_list.append(start)
            elif start in high_lat and end not in high_lat:
                # print(1111)
                if c_r < d_r:
                    if d_r - c_r < 5:
                        start = c_k * 9 + c_r + 1
                        router_list.append(start)
                    else:
                        if (c_r - 1) % 9 != 0:
                            start = c_k * 9 + c_r - 1 
                        else:
                            start = c_k * 9 + 9
                        router_list.append(start)
                else:
                    start =c_k * 9 + c_r - 1 
                    router_list.append(start)
            elif start not in high_lat and end in high_lat:
                if c_k < d_k:
                    start = (c_k + 1) * 9 + c_r
                    router_list.append(start)
                else:
                    start = (c_k - 1) * 9 + c_r
                    router_list.append(start)
            else:
                if c_r < d_r:
                    if d_r - c_r < 5:
                        start = c_k * 9 + c_r + 1
                        router_list.append(start) 
                    else:
                        if (c_r - 1) % 9 != 0:
                            start = c_k * 9 + c_r - 1 
                        else:
                            start = c_k * 9 + 9
                        router_list.append(start)                  
                else:
                    if c_r - d_r < 5:
                        start = c_k * 9 + c_r - 1
                        router_list.append(start) 
                    else:
                        start =c_k * 9 + (c_r + 1) % 9
                        router_list.append(start) 
        c_k = int((start - 1) / 9)
        c_r = start % 9 if start % 9 != 0 else 9
        i = i + 1
        # if i > 8:
        #     break
    # router_list.append(end)
    # print(router_list)
    return router_list


#
def Network_flow(G,number,weight):
    pair_list,all_flow = Generate_random_data_pair(number)
    # print('pair list',pair_list)
    # print('all table',all_table)
    # return
    temp_weight = copy.deepcopy(weight)
    new_pair_list = copy.deepcopy(pair_list)
    for pair in pair_list:
        start = pair[0][0]
        end = pair[0][1]
        flow = pair[1]

        # 使用LCRA路由算法计算得到路由表
        routing = Generate_router(start,end)
        # print(routing)
        temp_point = routing[1]    # 第一跳
        i = 1
        while start != end:
            # print(start,temp_point,end)
            # print(start,point,flow,weight[start-1][point-1])
            weight[start - 1][temp_point - 1] -= flow
            weight[temp_point - 1][start - 1] -= flow
            start = temp_point
            if temp_point == end:
                break
            # print(i, routing)
            temp_point = routing[1 + i]            
            i = i + 1
    current_flow = np.array(weight)
    congestion_pair_list = []
    for i in range(current_flow.shape[0]):
        a = np.array(current_flow[i])
        temp = np.where( a < 2560 * 0.05)
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
    # return congestion_pair_list,all_flow
    return temp_weight, weight

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

    # plt.xticks(x,_xtick_labels)
    
    # plt.grid(alpha=2,linestyle=':')
    # # plt.legend(handles = [l1, l2], labels = ['a', 'b'], loc = 'best',prop=myfont)

   
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
    G=  [[0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
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
         [M, M, M, M, 2560, 0, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
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

    # 测试一把 LCRA 路由算法
    # route_table = Generate_router(46,7)
    # print(route_table)

    # congest_result = {}
    # for i in range(0,45):
    #     a = 0
    #     for j in range(0,1000):

    #         temp_weight = copy.deepcopy(weight)
    #         congestion_pair_list,all_flow = Network_flow(G,20+i,temp_weight)
    #         del temp_weight
    #         a = a + len(congestion_pair_list)
    #     congest_result[20+i] = a
    # # original_result =  sorted(original_result.items(), key=lambda v: v[0])
    # print(congest_result)
    # result = {}

    original_weight = []
    load_weight = []
    for i in range(0,6):
        for j in range(0,1000):
            temp_weight = copy.deepcopy(weight)
            # old_weight使用pair对之前的带宽， new_weight使用pair对之后的带宽
            old_weight,new_weight = Network_flow(G, 20+i*15, temp_weight)        # 流量对分别取值20 35 50 65 80 95
            del temp_weight
            # if old_weight == 0:
            #     continue
            old_weight = np.array(old_weight)
            new_weight = np.array(new_weight)
            original_weight.append(old_weight)
            load_weight.append(new_weight)
    original_weight = np.array(original_weight)  # [[54*54][54*54]......[54*54](1000个)] pair对计算之前
    load_weight = np.array(load_weight)    # [[54*54][54*54]......[54*54](1000个)]  pair对计算之后
    # print(original_weight.shape)

    original_weight = original_weight.reshape(6,1000,54,54)
    load_weight = load_weight.reshape(6,1000,54,54)

    original_result = []
    load_result = []
    for m in range(0,6):
        temp_original_weight = original_weight[m]
        temp_load_weight = load_weight[m]
        temp_original_result = 0
        temp_load_result = []
        for num in range(0,1000):
            for i in range(0,54):
                for j in range(0,54):
                    if i>j and temp_original_weight[num][i][j] <= 2560 :
                        if temp_original_weight[num][i][j] < 0:
                            temp_original_weight[num][i][j] = 0
                        a = temp_original_weight[num][i][j]
                        # print(temp_original_weight[num][i][j])
                    if i>j and temp_load_weight[num][i][j] <= 2560 :
                        if temp_load_weight[num][i][j] < 0:
                            temp_load_weight[num][i][j] = 0
                        b = temp_load_weight[num][i][j]
                        temp_original_result = temp_original_result + temp_load_weight[num][i][j]
                        temp_load_result.append(b)

        # original_arr_mean = np.mean(temp_original_result)
        # original_arr_std = np.std(temp_original_result,ddof=1)
        # original_result.append([original_arr_mean,original_arr_std])
        original_result.append(temp_original_result)
        load_arr_mean = np.mean(temp_load_result)
        load_arr_std = np.std(temp_load_result,ddof=1)

        # 使用LCRA后的剩余带宽均值，剩余带宽标准差
        load_result.append([load_arr_mean,load_arr_std])

    print(original_result)
    print(load_result)


    f=open("con_var_LCRA.txt","w")

    # 写入原始的带宽
    f.writelines(str(original_result)+'\n')
    # 写入 使用LCRA后的剩余带宽均值，剩余带宽标准差
    f.writelines(str(load_result))
    f.close()