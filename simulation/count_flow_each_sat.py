import numpy as np
import random
import copy


M = 25600000


# 返回  number数量对  [[s_id, d_id], flow] 以及 all_flow
def Generate_random_data_pairA(number):
    pair_list = []
    flow = Gamma_flow(3.10338, 85.2079072, number)
    all_flow = 0
    for i in range(number * 2):
        pair = [random.randint(1, 54), random.randint(1, 54)]
        if pair[1] == pair[0] or pair in pair_list:
            continue
        pair_list.append(pair)
        if len(pair_list) == number:
            break
    for i in range(number):
        all_flow += flow[i] / 2
        pair_list[i] = ["A", pair_list[i], flow[i] / 2]
    # print(pair_list)
    # print("the num of fow: ", len(pair_list))
    # print("all flow: ", all_flow)
    return pair_list, all_flow

def Generate_random_data_pairB(number):
    pair_list = []
    flow = Gamma_flow(3.10338, 85.2079072, number)
    all_flow = 0
    for i in range(number * 2):
        pair = [random.randint(1, 54), random.randint(1, 54)]
        if pair[1] == pair[0] or pair in pair_list:
            continue
        pair_list.append(pair)
        if len(pair_list) == number:
            break
    for i in range(number):
        all_flow += flow[i]
        pair_list[i] = ["B", pair_list[i], flow[i]]
    # print(pair_list)
    # print("the num of fow: ", len(pair_list))
    # print("all flow: ", all_flow)
    return pair_list, all_flow

def Generate_random_data_pairC(number):
    pair_list = []
    flow = Gamma_flow(3.10338, 85.2079072, number)
    all_flow = 0
    for i in range(number * 2):
        pair = [random.randint(1, 54), random.randint(1, 54)]
        if pair[1] == pair[0] or pair in pair_list:
            continue
        pair_list.append(pair)
        if len(pair_list) == number:
            break
    for i in range(number):
        all_flow += flow[i]
        pair_list[i] = ["C", pair_list[i], flow[i]]
    # print(pair_list)
    # print("the num of fow: ", len(pair_list))
    # print("all flow: ", all_flow)
    return pair_list, all_flow


# 返回number个伽马分布的流
def Gamma_flow(shape, scale, number):
    s = np.random.gamma(shape, scale, 25600)  # 在2.到2.之间随机生成25600个小数
    # count, bins, ignored = plt.hist(s, 50, normed=True)#50：
    # y = bins**(shape-1)*(np.exp(-bins/scale)/(sps.gamma(shape)*scale**shape))
    # plt.plot(bins, y, linewidth=2, color='r')
    # plt.show()
    s = s.tolist()
    s.sort()
    flow = []
    flow.append(s[0])
    factor = int(25600 / (number - 1))
    for i in range(1, number - 1):
        flow.append(s[i * factor])
    flow.append(s[-1])
    return flow


# DijkStra路由算法
def Dijkstra(G, s, d):
    # print("Start Dijstra Path……")
    path = []
    n = len(G)
    fmax = 999
    w = [[0 for i in range(n)] for j in range(n)]
    book = [0 for i in range(n)]
    dis = [fmax for i in range(n)]
    book[s - 1] = 1  # 节点编号从1开始，列表序号从0开始
    midpath = [-1 for i in range(n)]  # 上一跳列表
    for i in range(n):
        for j in range(n):
            if G[i][j] != 0:
                w[i][j] = G[i][j]  # 0→max
            else:
                w[i][j] = fmax
            if i == s - 1 and G[i][j] != 0:  # 直连的节点最小距离就是network[i][j]
                dis[j] = G[i][j]

    for i in range(n - 1):  # n-1次遍历，除了s节点
        min = fmax
        u = 0
        for j in range(n):
            if book[j] == 0 and dis[j] < min:  # 如果未遍历且距离最小
                min = dis[j]
                u = j
        book[u] = 1
        for v in range(n):  # u直连的节点遍历一遍
            if dis[v] > dis[u] + w[u][v]:
                dis[v] = dis[u] + w[u][v]
                midpath[v] = u + 1  # 上一跳更新
    j = d - 1  # j是序号
    path.append(d)  # 因为存储的是上一跳，所以先加入目的节点d，最后倒置
    while (midpath[j] != -1):
        path.append(midpath[j])
        j = midpath[j] - 1
    path.append(s)
    path.reverse()  # 倒置列表
    # print(path)
    # print(midpath)
    # print(dis)
    return path

# LCRA 路由算法，  直接返回的 router_list 就是源于目的节点的路由表
def LCRA(start, end):
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

# 根据original变量的值来决定调用哪个DijkStra路由算法；；True时，调用的是Dijkstra路由算法，False时，调用的是选择性迭代Dijkstra路由算法
def Generate_router_tabel_Dijkstra(G):
    all_table = {}
    n = len(G)
    for i in range(1,n+1):
        table = {}
        for j in range(1,n+1):
            if i == j:
                continue

            path = Dijkstra(G,i,j)

            table[j] = path
        all_table[i] = table
    return all_table


def update_flow_per_sat(pair_list, flow_per_sat):
    for pair in pair_list:
        type = pair[0]
        start = pair[1][0]
        end = pair[1][1]
        temp_flow = pair[2]

        # 使用LCRA路由算法计算得到路由表
        routing = LCRA(start,end)
        # print(routing)
        temp_point = routing[1]    # 第一跳
        i = 1
        while start != end:
            # print(start,temp_point,end)
            # print(start,point,flow,weight[start-1][point-1])
            if(type == "A"):
                flow_per_sat[temp_point - 1][0] += temp_flow
            elif(type == "B"):
                flow_per_sat[temp_point - 1][1] += temp_flow
            elif(type == "C"):
                flow_per_sat[temp_point - 1][2] += temp_flow

            start = temp_point
            if temp_point == end:
                break
            temp_point = routing[1 + i]
            i = i + 1
    return flow_per_sat


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

    # 每个卫星节点上A,B,C三类业务的流量
    flow_per_sat = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],
            [0,0,0],[0,0,0],[0,0,0]]


    # 产生A\B\C三种流，每种流的大小比值为1:2:2
    mean_A = []
    mean_B = []
    mean_C = []

    sum_A = []
    sum_B = []
    sum_C = []

    for i in range(0,9):
        for j in range(0,1):
            temp_flow_per_sat = copy.deepcopy(flow_per_sat)
            # pairSingle格式如下： ['A', [18, 41], 5.054630413611507]，[0]表示流的类型，[1]表示源目的节点对，[2]表示flow的大小
            # flowSingle格式如下：

            # 产生A类流量
            pairSingleA, flowSingleA = Generate_random_data_pairA(20 + i * 10)
            # print(pairSingleA)
            # print("the num of fow: ", len(pairSingleA))
            # print("class A all flow: ", flowSingleA)

            # 产生B类流量
            pairSingleB, flowSingleB = Generate_random_data_pairB(20 + i * 10)
            # print(pairSingleB)
            # print("the num of fow: ", len(pairSingleB))
            # print("class B all flow: ", flowSingleB)

            # 产生C类流量
            pairSingleC, flowSingleC = Generate_random_data_pairC(20 + i * 10)
            # print(pairSingleC)
            # print("the num of fow: ", len(pairSingleC))
            # print("class C all flow: ", flowSingleC)

            #print("0: ", temp_flow_per_sat)
            temp_flow_per_sat = update_flow_per_sat(pairSingleA, temp_flow_per_sat)
            #print("1: ", temp_flow_per_sat)
            temp_flow_per_sat = update_flow_per_sat(pairSingleB, temp_flow_per_sat)
            #print("2: ", temp_flow_per_sat)
            temp_flow_per_sat = update_flow_per_sat(pairSingleC, temp_flow_per_sat)

        # 每次flow

            # print("temp_flow_per_sat: ", temp_flow_per_sat)

        classA_flow = []
        classB_flow = []
        classC_flow = []

        for k in range(0, len(temp_flow_per_sat)):
            classA_flow.append(temp_flow_per_sat[k][0])
            classB_flow.append(temp_flow_per_sat[k][1])
            classC_flow.append(temp_flow_per_sat[k][2])

        # print("the number of traffic flows: ",20 + i * 10 )
        #
        # print("     class A flow : ", classA_flow)
        # print("     sum: ", np.sum(classA_flow), " mean: ", np.mean(classA_flow), " max: ", np.max(classA_flow), " min: ", np.min(classA_flow))
        #
        # print("     class B flow : ", classB_flow)
        # print("     sum: ", np.sum(classB_flow), " mean: ", np.mean(classB_flow), " max: ", np.max(classB_flow), " min: ", np.min(classB_flow))
        #
        # print("     class C flow : ", classC_flow)
        # print("     sum: ", np.sum(classC_flow), " mean: ", np.mean(classC_flow), " max: ", np.max(classC_flow), " min: ", np.min(classC_flow))

        mean_A.append(np.mean(classA_flow))
        mean_B.append(np.mean(classB_flow))
        mean_C.append(np.mean(classC_flow))

        sum_A.append(np.sum(classA_flow))
        sum_B.append(np.sum(classB_flow))
        sum_C.append(np.sum(classC_flow))


    print("mean_A: ", mean_A)
    print("mean_B: ", mean_B)
    print("mean_C: ", mean_C)

    print("sum_A: ", sum_A)
    print("sum_B: ", sum_B)
    print("sum_C: ", sum_C)

    delay_A = []
    for i in range(0, len(mean_A)):
        delay_A.append(80 + mean_A[i] / 80)
    print("delay_A: ", delay_A)

    delay_B = []
    for i in range(0, len(mean_B)):
        delay_B.append(delay_A[i] + mean_B[i] / 80 * (2/5))
    print("delay_B: ", delay_B)

    delay_C = []
    for i in range(0, len(mean_C)):
        delay_C.append(delay_A[i] + mean_C[i] / 80 * (3/5))
    print("delay_C: ", delay_C)




    delay_Dijkstra = []
    for i in range(0, len(mean_A)):
        if(mean_B[i] < 1000):
            delay_Dijkstra.append(80 + (mean_A[i]  + mean_B[i] + mean_C[i])/ 80)
        elif(mean_B[i] < 1600):
            delay_Dijkstra.append(80 + (mean_A[i] + mean_B[i] * 2.5 + mean_C[i]* 2.5) / 80)
        else:
            delay_Dijkstra.append(80 + (mean_A[i] + mean_B[i] * 5 + mean_C[i] * 5) / 80)
    print("delay_Dijkstra: ", delay_Dijkstra)

    delay_LCRA = []
    for i in range(0, len(mean_A)):
            delay_LCRA.append(80 + (mean_A[i]  + mean_B[i] + mean_C[i])/ 80)
    print("delay_LCRA: ", delay_LCRA)
