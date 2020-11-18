# 本代码完成的是3中路由表的实现，分别是Dijkstra,选择性迭代Dijkstra，LCRA

M = 25600000

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


# 选择性迭代DijkStra路由算法
def O_Dijkstra(G, s, d):  # 迪杰斯特拉算法算s-d的最短路径，并返回该路径和代价
    # print("Start Dijstra Path……")
    path = []  # s-d的最短路径
    n = len(G)  # 邻接矩阵维度，即节点个数
    fmax = 999
    w = [[0 for i in range(n)] for j in range(n)]  # 邻接矩阵转化成维度矩阵，即0→max
    book = [0 for i in range(n)]  # 是否已经是最小的标记列表
    dis = [fmax for i in range(n)]  # s到其他节点的最小距离
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

    if s < d:
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
                    if midpath.count(u + 1) == 2:
                        dis[u] += 1
                        w[midpath[u] - 1][u] += 1
                        w[u][midpath[u] - 1] += 1

    if s > d:
        for i in range(n - 1):  # n-1次遍历，除了s节点
            min = fmax
            u = 0
            for j in range(n - 1, -1, -1):
                if book[j] == 0 and dis[j] < min:  # 如果未遍历且距离最小
                    min = dis[j]
                    u = j
            book[u] = 1
            for v in range(n - 1, -1, -1):  # u直连的节点遍历一遍
                if dis[v] > dis[u] + w[u][v]:
                    dis[v] = dis[u] + w[u][v]
                    midpath[v] = u + 1  # 上一跳更新
                    if midpath.count(u + 1) == 2:
                        dis[u] += 1
                        w[midpath[u] - 1][u] += 1
                        w[u][midpath[u] - 1] += 1

    j = d - 1  # j是序号
    path.append(d)  # 因为存储的是上一跳，所以先加入目的节点d，最后倒置
    while (midpath[j] != -1):
        path.append(midpath[j])
        j = midpath[j] - 1
    path.append(s)
    path.reverse()  # 倒置列表
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

def Generate_router_tabel(G ):
    all_table = {}
    n = len(G)  # 返回二维数组中一维数组的个数，此处为9
    # print("n:", n)

    for i in range(1,n+1):  # 包含左侧边界，不包含右侧边界  i取值1-9
        table = {}
        for j in range(1,n+1):  # j取值1-9
            if i == j:
                continue       # 对角处的不考虑，直接跳过

            path = Dijkstra(G,i,j)   # 在图形中搜索节点i至节点j的路径

            table[j] = path
        all_table[i] = table
    return all_table

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

    route_table = Generate_router_tabel(G)

    print(route_table)
