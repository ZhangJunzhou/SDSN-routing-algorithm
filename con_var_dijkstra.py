import os
import random
import numpy as np
# import matplotlib.pyplot as plt
# import scipy.special as sps
import copy

M = 25600000

def Dijkstra(G,s,d):#迪杰斯特拉算法算s-d的最短路径，并返回该路径和代价
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
    flow = Gamma_flow(3.10338,85.2079072,number)
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
        flow.append(s[i*factor])
    flow.append(s[-1])
    return flow

def Network_flow(G,number,weight):
    all_table = Generate_router_tabel(G)
    pair_list = Generate_random_data_pair(number)
    temp1_weight = copy.deepcopy(weight)
    origin_weight = copy.deepcopy(weight)
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
            origin_weight[start-1][temp_point-1] -= flow
            origin_weight[temp_point-1][start-1] -= flow
            start = temp_point
            temp_point = all_table[temp_point][end][1]
    current_flow = np.array(origin_weight)
    congestion_pair_list = []
    for i in range(current_flow.shape[0]):
        temp_current_flow = np.array(current_flow[i])
        temp = np.where(temp_current_flow<=2560*0.05)
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
    
    if len(congestion_pair_list) == 0:
        return origin_weight,origin_weight
    # congestion_pair_list = list(set(congestion_pair_list))
    congestion_pair_list.sort()
    rotary_pairs = []
    for item in congestion_pair_list:
        two_way_flow_list = Select(item,pair_list,all_table)
        if two_way_flow_list[0] > two_way_flow_list[1]:
            rotary_pairs.append([item[1],item[0],two_way_flow_list[1],two_way_flow_list[0]])
        else:
            rotary_pairs.append([item[0],item[1],two_way_flow_list[0],two_way_flow_list[1]])
        # print('two_way_flow_list',two_way_flow_list,two_way_flow_list[0]+two_way_flow_list[1]-2560)

    # print('rotary pair',rotary_pairs)    
    a = [3,4,7,8,9]
    low_latitudes = []
    for i in a:
        for j in range(0,6):
            low_latitudes.append(i+j*9)
   
    ratio_a = 0
    for item in rotary_pairs:
        if item[0] not in low_latitudes or item[1] not in low_latitudes:
            continue
        rotary_points = Rotary_points(item,0,low_latitudes)
        # print(rotary_points)
        ratio_a = Shunt_ratio(origin_weight,rotary_points,item,item[0],0)
        # print(ratio_a)        
        pair_list,temp1_weight = New_pair_list(item,rotary_points,ratio_a,pair_list,all_table,temp1_weight,True,origin_weight)

    temp2_weight = copy.deepcopy(temp1_weight)    
    temp1_weight = New_network_flow(pair_list,all_table,temp1_weight)

    conti = False

    for item in rotary_pairs:
        if temp1_weight[item[0]-1][item[1]-1] <= 0:
            conti = True
            break

    if not conti:
        # result1,result2,result3,result4,result5 = Check(temp1_weight,rotary_pairs,low_latitudes)
        # return result1,result2,result3,result4,result5
        return origin_weight,temp1_weight
    else:
        ratio_b = 0
        for item in rotary_pairs:
            if item[0] not in low_latitudes or item[1] not in low_latitudes:
                continue
            rotary_points_b = Rotary_points(item,1,low_latitudes)
            # print(rotary_points_b)
            ratio_b = Shunt_ratio(origin_weight,rotary_points_b,item,item[1],1)
            # print(ratio_b)
            pair_list,temp2_weight = New_pair_list(item,rotary_points_b,ratio_b,pair_list,all_table,temp2_weight,False,origin_weight)
        # print(pair_list)
        temp2_weight = New_network_flow(pair_list,all_table,temp2_weight)
    # result1,result2,result3,result4,result5 =Check(temp2_weight,rotary_pairs,low_latitudes)
    return origin_weight,temp2_weight
    # return result1,result2,result3,result4,result5
    
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
    # print(congestion_pair ,two_way_flow_list)

    return two_way_flow_list

def Rotary_points(congestion_point_item,i,low_latitudes):
    rotary_points = []
    if abs(congestion_point_item[0] - congestion_point_item[1]) == 9:
        if congestion_point_item[i] + 1 in low_latitudes:
            rotary_points.append(congestion_point_item[i] + 1)
        if congestion_point_item[i] - 1 in low_latitudes:
            rotary_points.append(congestion_point_item[i] - 1)
    
    if abs(congestion_point_item[0] - congestion_point_item[1]) == 1:
        if congestion_point_item[i] + 9 in low_latitudes:
            rotary_points.append(congestion_point_item[i] + 9)
        if congestion_point_item[i] - 9 in low_latitudes:
            rotary_points.append(congestion_point_item[i] - 9)
    
    return rotary_points

def Shunt_ratio(weight,rotary_points,rotary_pair,start_point,i):
    small_weight = 2560
    for item in rotary_points:
        if weight[item-1][start_point-1] < small_weight:
            small_weight = weight[item-1][start_point-1]

    if rotary_pair[i+2] == 0 or (small_weight -2560 * 0.05) <= 0:
        ratio = 0
    else:
        ratio = (small_weight - 2560 * 0.05) / rotary_pair[i+2] * 1.0

    if ratio > 1:
        ratio = 1

    return ratio
 
def New_pair_list(rotary_pair,rotary_points,ratio,pair_list,all_table,weight,number,remainbandwidth):
    new_pair_list = []
    rotary_point_pair_list = []
    temp_pair_list = []
    if number:
        congestion_pair = [rotary_pair[0],rotary_pair[1]]
    else:
        congestion_pair = [rotary_pair[1],rotary_pair[0]]

    pair_temp_list = []
    for pair in pair_list:
        start = pair[0][0]
        end = pair[0][1]
        if start == end:
            continue
        flow = pair[1]
        routing = all_table[start][end]        
        # print('routing',routing)
        for i in range(1,len(routing)):
            if [start,routing[i]] == congestion_pair:
                x = 0
                if len(rotary_points) == 2:
                    # print(rotary_points)
                    if len(all_table[rotary_points[0]][end]) < len(all_table[rotary_points[1]][end]):
                        # print(all_table[rotary_points[0]][end])
                        x = rotary_points[0]
                    elif len(all_table[rotary_points[0]][end]) > len(all_table[rotary_points[1]][end]):
                        # print(all_table[rotary_points[1]][end])
                        x = rotary_points[1]
                    else:
                        if remainbandwidth[rotary_points[0]-1][start-1] >= remainbandwidth[rotary_points[1]-1][start-1]:
                            x = rotary_points[0]
                        else:
                            x = rotary_points[1]
                else:
                    x = rotary_points[0]
                # print(x,end)
                # print(all_table[x][end])
                if x == end:
                    break
                if len(all_table[x][end]) == 2 or all_table[x][end][1] != start:
                    weight[start-1][x-1] -= ratio * flow
                    weight[x-1][start-1] -= ratio * flow
                    new_pair = [[x,end],ratio * flow]
                    temp_pair_list.append(new_pair)
                    temp_flow = (1 - ratio) * flow                         
                    new_pair = [[start,end],temp_flow]
                    temp_pair_list.append(new_pair)
                    pair[0][1] = start 
                    break
                                     
            start = routing[i]
    # print("temp_pair_list",temp_pair_list)
    pair_list += temp_pair_list
    return pair_list,weight

def New_network_flow(pair_list,all_table,weight):
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
    return weight
    
def Check(weight,rotary_pairs,low_latitudes):
    current_flow = np.array(weight)
    congestion_pair_list = []
    for i in range(current_flow.shape[0]):
        temp_current_flow = np.array(current_flow[i])
        temp = np.where(temp_current_flow<=2560*0.05)
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
    # print("old congestion")
    result1 = len(rotary_pairs)
    result2 = 0
    result3 = len(congestion_pair_list)
    result4 = 0
    result5 = 0
    for item in rotary_pairs:
        if weight[item[0]-1][item[1]-1] > 0:
            result2 += 1
        if item[0] in low_latitudes and item[1] in low_latitudes:
            result4 += 1
    for item in congestion_pair_list:
        if item[0] in low_latitudes and item[1] in low_latitudes:
            result5 += 1
    return result1,result2,result3,result4,result5  
        

if __name__ == '__main__':
       
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

    
    
    original_weight = []
    load_weight = []
    for i in range(0, 6):
        for j in range(0, 1000):
            temp_weight = copy.deepcopy(weight)
            old_weight,new_weight = Network_flow(G,20+i*15,temp_weight)            
            del temp_weight
            # if old_weight == 0:
            #     continue
            original_weight.append(old_weight)
            load_weight.append(new_weight)
    original_weight = np.array(original_weight)
    load_weight = np.array(load_weight)
 
    original_weight = original_weight.reshape(6,1000,54,54)
    load_weight = load_weight.reshape(6,1000,54,54)
    original_result = []
    load_result = []
    for m in range(0,6):
        temp_original_weight = original_weight[m]
        temp_load_weight = load_weight[m]
        temp_original_result = []
        temp_load_result = []
        for num in range(0,1000):        
            for i in range(0,54):
                for j in range(0,54):
                    if i>j and temp_original_weight[num][i][j] <= 2560 :
                        if temp_original_weight[num][i][j] < 0:
                            temp_original_weight[num][i][j] = 0
                        a = temp_original_weight[num][i][j]
                        temp_original_result.append(a)
                    if i>j and temp_load_weight[num][i][j] <= 2560 :
                        if temp_load_weight[num][i][j] < 0:
                            temp_load_weight[num][i][j] = 0
                        b = temp_load_weight[num][i][j]
                        temp_load_result.append(b)

        original_arr_mean = np.sum(temp_original_result)
        original_arr_std = np.std(temp_original_result,ddof=1)
        original_result.append([original_arr_mean,original_arr_std])
        load_arr_mean = np.sum(temp_load_result)
        load_arr_std = np.std(temp_load_result,ddof=1)
        load_result.append([load_arr_mean,load_arr_std])

    print(original_result)
    print(load_result)

    
    f=open("con_var_dijkstra.txt","w")

    # 写入 使用Dijkstra后的剩余带宽均值，剩余带宽标准差
    f.writelines(str(original_result)+'\n')
    f.writelines(str(load_result))
    f.close()




