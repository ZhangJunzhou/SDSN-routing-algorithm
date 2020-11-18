import os
import pandas
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.special as sps
import copy

M = 25600000

def Dijkstra(G,s,d):#迪杰斯特拉算法算s-d的最短路径，并返回该路径和代价
    # print("Start Dijstra Path……")
    path=[]#s-d的最短路径
    n=len(G)#邻接矩阵维度，即节点个数
    fmax=999
    w=[[0 for i in range(n)]for j in range(n)]      #邻接矩阵转化成维度矩阵，即0→max
    book=[0 for i in range(n)]      #是否已经是最小的标记列表
    dis=[fmax for i in range(n)]       #s到其他节点的最小距离
    book[s-1]=1      #节点编号从1开始，列表序号从0开始
    midpath=[-1 for i in range(n)]      #上一跳列表
    for i in range(n):
        for j in range(n):
            if G[i][j]!=0:
                w[i][j]=G[i][j]         #0→max
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

# def Dijkstra(G,s,d):#迪杰斯特拉算法算s-d的最短路径，并返回该路径和代价
#     # print("Start Dijstra Path……")
#     path=[]#s-d的最短路径
#     n=len(G)#邻接矩阵维度，即节点个数
#     fmax=999
#     w=[[0 for i in range(n)]for j in range(n)]#邻接矩阵转化成维度矩阵，即0→max
#     book=[0 for i in range(n)]#是否已经是最小的标记列表
#     dis=[fmax for i in range(n)]#s到其他节点的最小距离
#     book[s-1]=1#节点编号从1开始，列表序号从0开始
#     midpath=[-1 for i in range(n)]#上一跳列表
#     for i in range(n):
#         for j in range(n):
#             if G[i][j]!=0:
#                 w[i][j]=G[i][j]#0→max
#             else:
#                 w[i][j]=fmax
#             if i==s-1 and G[i][j]!=0:#直连的节点最小距离就是network[i][j]
#                 dis[j]=G[i][j]
       
#     if s<d:   
#         for i in range(n-1):#n-1次遍历，除了s节点
#             min=fmax
#             u=0
#             for j in range(n):
#                 if book[j]==0 and dis[j]<min:#如果未遍历且距离最小
#                     min=dis[j]
#                     u=j
#             book[u]=1
#             for v in range(n):#u直连的节点遍历一遍
#                 if dis[v]>dis[u]+w[u][v]:
#                     dis[v]=dis[u]+w[u][v]
#                     midpath[v]=u+1#上一跳更新
#                     if midpath.count(u+1)==2:
#                         dis[u]+=1
#                         w[midpath[u]-1][u]+=1
#                         w[u][midpath[u]-1]+=1
               
#     if s>d:
#         for i in range(n-1):#n-1次遍历，除了s节点
#             min=fmax
#             u=0
#             for j in range(n-1,-1,-1):
#                 if book[j]==0 and dis[j]<min:#如果未遍历且距离最小
#                     min=dis[j]
#                     u=j
#             book[u]=1
#             for v in range(n-1,-1,-1):#u直连的节点遍历一遍
#                 if dis[v]>dis[u]+w[u][v]:
#                     dis[v]=dis[u]+w[u][v]
#                     midpath[v]=u+1#上一跳更新
#                     if midpath.count(u+1)==2:
#                         dis[u]+=1
#                         w[midpath[u]-1][u]+=1
#                         w[u][midpath[u]-1]+=1
   
#     j=d-1#j是序号
#     path.append(d)#因为存储的是上一跳，所以先加入目的节点d，最后倒置
#     while(midpath[j]!=-1):
#         path.append(midpath[j])
#         j=midpath[j]-1
#     path.append(s)
#     path.reverse()#倒置列表
#     return path


def Generate_router_tabel(G):
    all_table = {}
    n = len(G)
    for i in range(1,n+1):
        table = {}
        for j in range(1,n+1):
            if i == j:
                continue 
            path = Dijkstra(G,i,j)
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
    for i in range(number*2):
        pair = [random.randint(1,20),random.randint(1,20)]
        if pair[1] == pair[0] or pair in pair_list:
            continue
        pair_list.append(pair)
        if len(pair_list) == number:
            break
    for i in range(number):
        pair_list[i] = [pair_list[i],flow[i]]
    # print(pair_list,len(pair_list))
    return pair_list

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
        flow.append(s[i * factor])
    flow.append(s[-1])
    return flow

def Network_flow(G,number,weight):
    all_table = Generate_router_tabel(G)
    pair_list = Generate_random_data_pair(number)
    print('pair list', pair_list)
    # print('all table',all_table)
    # return
    temp_weight = copy.deepcopy(weight)
    new_pair_list = copy.deepcopy(pair_list)
    for pair in pair_list:
        start = pair[0][0]
        end = pair[0][1]
        flow = pair[1]
        temp = all_table[start]
        routing = temp[end]
        temp_point = routing[1]
        while temp_point != end:
            # print(start,temp_point,end)
            # print(start,point,flow,weight[start-1][point-1])
            weight[start-1][temp_point-1] -= flow
            weight[temp_point-1][start-1] -= flow
            start = temp_point
            temp_point = all_table[temp_point][end][1]
    current_flow = np.array(weight)
    congestion_pair_list = []
    for i in range(current_flow.shape[0]):
        temp = np.where(current_flow[i]<2560*0.1)
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
    print(congestion_pair_list)
    # congestion_pair_list = list(set(congestion_pair_list))
    congestion_pair_list.sort()
    rotary_pair = {}
    for item in congestion_pair_list:
        two_way_flow_list = Select(item,pair_list,all_table)
        # return
        order = two_way_flow_list[0]
        reverse_order = two_way_flow_list[1]
        rotary_point = 0
        congestion_pair = []
        if order<reverse_order:
            if order*2/3 + reverse_order<2560*0.9:
                congestion_pair.append(item[0])
                congestion_pair.append(item[1])
                rotary_point = item[0]
            else:
                congestion_pair.append(item[1])
                congestion_pair.append(item[0])
                rotary_point = item[1]
        else:
            if order + reverse_order*2/3<2560*0.9:
                congestion_pair.append(item[1])
                congestion_pair.append(item[0])
                rotary_point = item[1]
            else:
                congestion_pair.append(item[0])
                congestion_pair.append(item[1])
                rotary_point = item[0]
        rotary_pair = Rotating_points(rotary_point,item,5,4)
        print('rotary pair',rotary_pair)
        print('congestion_pair',congestion_pair)
        print(weight[congestion_pair[0]-1][congestion_pair[1]-1])
        new_pair_list = Rotating_new_pair_list(rotary_pair,congestion_pair,new_pair_list,all_table,temp_weight)
    # print(temp_weight)
    New_network_flow(new_pair_list,all_table,temp_weight,congestion_pair_list)
    Check(temp_weight)
        # print()
        # break

    
def Select(congestion_pair,pair_list,all_table):
    temp_congestion_pair = list(reversed(congestion_pair))    
    flow_1 = 0
    flow_2 = 0
    for pair_item in pair_list:
        start = pair_item[0][0]
        end = pair_item[0][1]
        if start == end:
            continue
        flow = pair_item[1]
        temp = all_table[start]
        routing = temp[end]
        temp_point = routing[1]
        while temp_point != end:
            routing_part = [start,temp_point]
            if routing_part==congestion_pair:
                flow_1 += flow
                # break
            if routing_part==temp_congestion_pair:
                flow_2 += flow
                # break
            start = temp_point
            temp_point = all_table[temp_point][end][1]

    two_way_flow_list = [flow_1,flow_2]
    print(congestion_pair ,two_way_flow_list)

    return two_way_flow_list

def Rotating_points(rotary_point,congestion_pair,row,col):
    rotary_pair = {}
    if rotary_point == congestion_pair[0]:
        congestion_object = congestion_pair[1]
    else:
        congestion_object = congestion_pair[0]

    if rotary_point<=col:
        if abs(congestion_object - rotary_point)==1:
            rotary_pair[rotary_point + col] = [rotary_point, rotary_point + col + (congestion_object - rotary_point)]
            if rotary_point - (congestion_object - rotary_point) <= col and rotary_point - (congestion_object - rotary_point) > 0:
                rotary_pair[rotary_point - (congestion_object - rotary_point)] = [rotary_point, rotary_point - (congestion_object - rotary_point) + col]
        if abs(congestion_object - rotary_point)==col:
            if rotary_point == 1:
                rotary_pair[rotary_point + 1] = [rotary_point, rotary_point + 1 + col]
            elif rotary_point == col:
                rotary_pair[rotary_point - 1] = [rotary_point, rotary_point - 1 + col]
            else:
                rotary_pair[rotary_point - 1] = [rotary_point, rotary_point - 1 + col]
                rotary_pair[rotary_point + 1] = [rotary_point, rotary_point + 1 + col]
        
    elif rotary_point>col and rotary_point<=col*(row - 1):
        if abs(congestion_object - rotary_point) == 1:
            rotary_pair[rotary_point - col] = [rotary_point, rotary_point - col + (congestion_object - rotary_point)]
            rotary_pair[rotary_point + col] = [rotary_point, rotary_point + col + (congestion_object - rotary_point)]
            if (rotary_point - (congestion_object - rotary_point)) % col != 0:
                rotary_pair[rotary_point - (congestion_object - rotary_point)] = [rotary_point, rotary_point - (congestion_object - rotary_point) + col, rotary_point - (congestion_object - rotary_point) + col]
        if abs(congestion_object - rotary_point) == col:
            if (rotary_point - 1) % col != 0:
                rotary_pair[rotary_point - 1] = [rotary_point, rotary_point - 1 + (congestion_object - rotary_point)]
            if (rotary_point + 1) % col != 1:
                rotary_pair[rotary_point + 1] = [rotary_point, rotary_point + 1 + (congestion_object - rotary_point)]
            rotary_pair[rotary_point + (rotary_point - congestion_object)] = [rotary_point]
            if (rotary_point + (rotary_point - congestion_object) - 1) % col != 0:
                rotary_pair[rotary_point + (rotary_point - congestion_object)].append(rotary_point + (rotary_point - congestion_object) - 1)
            if (rotary_point + (rotary_point - congestion_object) + 1) % col != 1:
                rotary_pair[rotary_point + (rotary_point - congestion_object)].append(rotary_point + (rotary_point - congestion_object) + 1)

    else:
        if abs(congestion_object - rotary_point) == 1:
            rotary_pair[rotary_point - col] = [rotary_point, rotary_point - col + (congestion_object - rotary_point)]
            if rotary_point - (congestion_object - rotary_point) <= row * col and rotary_point - (congestion_object - rotary_point) > (row - 1) * col:
                rotary_pair[rotary_point - (congestion_object - rotary_point)] = [rotary_point, rotary_point - (congestion_object - rotary_point) - col]
        if abs(congestion_object - rotary_point) == col:
            if rotary_point == row * (col - 1) +1:
                rotary_pair[rotary_point + 1] = [rotary_point, rotary_point + 1 - col]
            elif rotary_point == row * col:
                rotary_pair[rotary_point - 1] = [rotary_point, rotary_point - 1 - col]
            else:
                rotary_pair[rotary_point - 1] = [rotary_point, rotary_point - 1 - col]
                rotary_pair[rotary_point + 1] = [rotary_point, rotary_point + 1 - col]
    # print(rotary_point,rotary_pair)
    # for keys in rotary_pair.keys():
    #     if keys<1 or keys>row*col:
    #         del rotary_pair[keys]
    return rotary_pair

def Rotating_new_pair_list(rotary_pair,congestion_pair,pair_list,all_table,weight):
    rotary_point_pair_list = []
    # print(rotary_pair)
    for keys in rotary_pair.keys():
        rotary_point_pair_list.append([keys,congestion_pair[0]])
    
    pair_temp_list = []
    for pair in pair_list:
        start = pair[0][0]
        end = pair[0][1]
        if start == end:
            continue
        flow = pair[1]
        temp = all_table[start]
        # print("start",start,'end',end,'routing',temp)
        routing = temp[end]
        # print('routing',routing)
        for i in range(1,len(routing)-1):
            if [start,routing[i]] in rotary_point_pair_list:
                temp_rotary_pair = copy.deepcopy(rotary_pair)
                for item in rotary_pair[start]:
                    new_routing_table = all_table[item][end]
                    if new_routing_table[1] == start:
                        temp_rotary_pair[start].remove(item)
                if i!=1:
                    # print('start',start)
                    pair[0][1] = start
                    pair[1] = flow
                else:
                    pair[1] = 0
                for item in temp_rotary_pair[start]:
                    weight[start-1][item-1] -= flow / len(temp_rotary_pair[start])
                    pair_temp = [[item,end],flow / len(temp_rotary_pair[start])]
                    pair_temp_list.append(pair_temp)
            start = routing[i]
    pair_list += pair_temp_list

    return pair_list

def New_network_flow(pair_list,all_table,weight,congestion_pair_list):
    # print('new pair list',pair_list)
    # print('all table',all_table)
    for pair in pair_list:
        start = pair[0][0]
        end = pair[0][1]
        if start == end:
            continue
        flow = pair[1]
        temp = all_table[start]
        routing = temp[end]
        temp_point = routing[1]
        while temp_point != end:
            # print(start,point,flow,weight[start-1][point-1])
            weight[start-1][temp_point-1] -= flow
            weight[temp_point-1][start-1] -= flow
            start = temp_point
            temp_point = all_table[temp_point][end][1]
    # print('new weight')
    for item in congestion_pair_list:
        print((item[0],item[1]),weight[item[0]-1][item[1]-1])
    # print(weight)
    return weight
    # print(congestion_pair)
    
def Check(weight):
    current_flow = np.array(weight)
    congestion_pair_list = []
    for i in range(current_flow.shape[0]):
        temp = np.where(current_flow[i]<2560*0.1)
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
    print(congestion_pair_list)
    for item in congestion_pair_list:
        print(weight[item[0]-1][item[1]-1])
    
        



if __name__ == '__main__':
       
    G = [[0, 1, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
          [1, 0, 1, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
          [M, 1, 0, 1, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M],
          [M, M, 1, 0, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M],
          [1, M, M, M, 0, 1, M, M, 1, M, M, M, M, M, M, M, M, M, M, M],
          [M, 1, M, M, 1, 0, 1, M, M, 1, M, M, M, M, M, M, M, M, M, M],
          [M, M, 1, M, M, 1, 0, 1, M, M, 1, M, M, M, M, M, M, M, M, M],
          [M, M, M, 1, M, M, 1, 0, M, M, M, 1, M, M, M, M, M, M, M, M],
          [M, M, M, M, 1, M, M, M, 0, 1, M, M, 1, M, M, M, M, M, M, M],
          [M, M, M, M, M, 1, M, M, 1, 0, 1, M, M, 1, M, M, M, M, M, M],
          [M, M, M, M, M, M, 1, M, M, 1, 0, 1, M, M, 1, M, M, M, M, M],
          [M, M, M, M, M, M, M, 1, M, M, 1, 0, M, M, M, 1, M, M, M, M],
          [M, M, M, M, M, M, M, M, 1, M, M, M, 0, 1, M, M, 1, M, M, M],
          [M, M, M, M, M, M, M, M, M, 1, M, M, 1, 0, 1, M, M, 1, M, M],
          [M, M, M, M, M, M, M, M, M, M, 1, M, M, 1, 0, 1, M, M, 1, M],
          [M, M, M, M, M, M, M, M, M, M, M, 1, M, M, 1, 0, M, M, M, 1],
          [M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M, 0, 1, M, M],
          [M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, 1, 0, 1, M],
          [M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, 1, 0, 1],
          [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M, M, 1, 0]]

    weight = [[0, 2560, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [2560, 0, 2560, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, 2560, 0, 2560, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, 2560, 0, M, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M, M],
            [2560, M, M, M, 0, 2560, M, M, 2560, M, M, M, M, M, M, M, M, M, M, M],
            [M, 2560, M, M, 2560, 0, 2560, M, M, 2560, M, M, M, M, M, M, M, M, M, M],
            [M, M, 2560, M, M, 2560, 0, 2560, M, M, 2560, M, M, M, M, M, M, M, M, M],
            [M, M, M, 2560, M, M, 2560, 0, M, M, M, 2560, M, M, M, M, M, M, M, M],
            [M, M, M, M, 2560, M, M, M, 0, 2560, M, M, 2560, M, M, M, M, M, M, M],
            [M, M, M, M, M, 2560, M, M, 2560, 0, 2560, M, M, 2560, M, M, M, M, M, M],
            [M, M, M, M, M, M, 2560, M, M, 2560, 0, 2560, M, M, 2560, M, M, M, M, M],
            [M, M, M, M, M, M, M, 2560, M, M, 2560, 0, M, M, M, 2560, M, M, M, M],
            [M, M, M, M, M, M, M, M, 2560, M, M, M, 0, 2560, M, M, 2560, M, M, M],
            [M, M, M, M, M, M, M, M, M, 2560, M, M, 2560, 0, 2560, M, M, 2560, M, M],
            [M, M, M, M, M, M, M, M, M, M, 2560, M, M, 2560, 0, 2560, M, M, 2560, M],
            [M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, 2560, 0, M, M, M, 2560],
            [M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, M, 0, 2560, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, 2560, 0, 2560, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, 2560, 0, 2560],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, 2560, M, M, 2560, 0]]

    # all_table = Generate_router_tabel(G)
    Network_flow(G,70,weight)


