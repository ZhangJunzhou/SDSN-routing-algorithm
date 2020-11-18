M = 0


# 记录的是路由表中，路由中转 经过每个节点的次数
flagin=[  [0, 0, M, 0, M, M, M, M, M],
          [0, 0, 0, M, 0, M, M, M, M],
          [M, 0, 0, M, M, 0, M, M, M],
          [0, M, M, 0, 0, M, 0, M, M],
          [M, 0, M, 0, 0, 0, M, 0, M],
          [M, M, 0, M, 0, 0, M, M, 0],
          [M, M, M, 0, M, M, 0, 0, M],
          [M, M, M, M, 0, M, 0, 0, 0],
          [M, M, M, M, M, 0, M, 0, 0]]


# 此算法描述的是最原始的DijkStra算法
def Dijkstra(G,s,d):   # 迪杰斯特拉算法算s-d的最短路径，并返回该路径和代价
    # print("Start Dijstra Path……")
    path = []    # s-d的最短路径，记录的是路径
    n = len(G)   # 邻接矩阵维度，即节点个数，本测试中为9
    fmax = 999
    w = [[0 for i in range(n)]for j in range(n)]  # 邻接矩阵转化成维度矩阵，即0→max
    book=[0 for i in range(n)]                  # 是否已经是最小的标记列表；； book的值置为1时，说明已经找到s节点到该节点的最短路径了；
    dis = [fmax for i in range(n)]                # s到其他节点的最小距离，初始化为999，相当于正无穷
    book[s-1] = 1                                 # 节点编号从1开始，列表序号从0开始；
    midpath = [-1 for i in range(n)]              # 上一跳列表

    # 初始化w二维矩阵，并且初始化s到所有节点的最小距离
    for i in range(n):
        for j in range(n):
            if G[i][j]!=0:
                w[i][j]=G[i][j]                  # 图形的变化 0→max，非零的保持不变
            else:
                w[i][j]=fmax
            if i==s-1 and G[i][j]!=0:            # 直连的节点最小距离就是network[i][j]
                dis[j]=G[i][j]                   # 直连的保持原本的数据，非直连的值均被置为999

    for i in range(n-1):                         # n-1次遍历，除了s节点，相当于每次循环都找到距离s节点最短距离的节点；；；
        min = fmax
        u = 0
        for j in range(n):
            if book[j] == 0 and dis[j] < min:        # 如果未遍历且距离源节点S节点最小的  距离以及节点；；；若是距离保持一致，则选择第一个节点，，因为使用的是 ＜
                min = dis[j]
                u = j

        book[u] = 1                 # 找到book值为0时，距离源节点 最小的距离的节点

        for v in range(n):                       # u直连的节点遍历一遍；；更新距离源节点的最小距离，即dis列表
            if dis[v] > dis[u] + w[u][v]:
                dis[v] = dis[u] + w[u][v]
                midpath[v] = u + 1                   # 上一跳更新


    j= d-1                                        # j是序号
    path.append(d)                               # 因为存储的是上一跳，所以先加入目的节点d，最后倒置
    while(midpath[j]!=-1):
        path.append(midpath[j])
        j = midpath[j] - 1
    path.append(s)

    path.reverse()         # 倒置列表
    # print(path)
    # print(midpath)
    # print(dis)
    return path


# #  此算法描述的是选择性迭代DijkStra路由算法
# def Dijkstra(G,s,d):#迪杰斯特拉算法算s-d的最短路径，并返回该路径和代价
#     # print("Start Dijstra Path……")
#     path = []                    #s-d的最短路径
#     n = len(G)                   #邻接矩阵维度，即节点个数
#     fmax = 999
#     w=[[0 for i in range(n)]for j in range(n)]                # 邻接矩阵转化成维度矩阵，即0→max
#     book = [0 for i in range(n)]                              # 是否已经是最小的标记列表
#     dis = [fmax for i in range(n)]                            # s到其他节点的最小距离
#     book[s-1] = 1                                             # 节点编号从1开始，列表序号从0开始
#     midpath = [-1 for i in range(n)]                          #上一跳列表
#     for i in range(n):
#         for j in range(n):
#             if G[i][j]!=0:
#                 w[i][j]=G[i][j]                              # 0→max
#             else:
#                 w[i][j]=fmax
#             if i==s-1 and G[i][j]!=0:                         # 直连的节点最小距离就是network[i][j]
#                 dis[j]=G[i][j]
#
#     if s < d:
#         for i in range(n-1):                                # n-1次遍历，除了s节点
#             min = fmax
#             u=0
#             for j in range(n):
#                 if book[j]==0 and dis[j]<min:               #如果未遍历且距离最小
#                     min=dis[j]
#                     u=j
#             book[u]=1
#
#
#             for v in range(n):                              # u直连的节点遍历一遍
#                 if dis[v] > dis[u]+w[u][v]:
#                     dis[v] = dis[u]+w[u][v]
#                     midpath[v]= u+1                         # 上一跳更新
#                     if midpath.count(u+1) == 2:            # 该函数用于计算在列表中出现的次数
#                         dis[u]+=1
#                         w[midpath[u]-1][u]+=1
#                         w[u][midpath[u]-1]+=1
#
#
#     if s > d:
#         for i in range(n-1):           #n-1次遍历，除了s节点
#             min=fmax
#             u=0
#             for j in range(n-1,-1,-1):
#                 if book[j]==0 and dis[j]<min:#如果未遍历且距离最小
#                     min=dis[j]
#                     u=j
#             book[u]=1
#
#             for v in range(n-1,-1,-1):#u直连的节点遍历一遍
#                 if dis[v]>dis[u]+w[u][v]:
#                     dis[v]=dis[u]+w[u][v]
#                     midpath[v]=u+1#上一跳更新
#                     if midpath.count(u+1)==2:
#                         dis[u]+=1
#                         w[midpath[u]-1][u]+=1
#                         w[u][midpath[u]-1]+=1
#
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

def test(G, all_table):
    nodeNum = len(G)
    for i in range(0,nodeNum):
        for j in range(0,nodeNum):
            if i==j:
                continue
            start = i + 1
            end = j + 1
            temp = all_table[start]   # temp字典，存储的是到每个节点的路径
            routing = temp[end]
            temp_point = routing[1]   # [0]指的是start
            while temp_point != end:   # 即不是直连的
                # print(start,temp_point,end)
                # print(start,point,flow,weight[start-1][point-1])
                flagin[start - 1][temp_point - 1] += 1
                flagin[temp_point - 1][start - 1] += 1   # 对称的
                start = temp_point
                temp_point = all_table[temp_point][end][1]

    # 输出的是中转经过每个节点的次数
    print(flagin)
           




if __name__ == '__main__':
       
    G = [ [0, 1, M, 1, M, M, M, M, M],       # 拓扑的图形
          [1, 0, 1, M, 1, M, M, M, M],
          [M, 1, 0, M, M, 1, M, M, M],
          [1, M, M, 0, 1, M, 1, M, M],
          [M, 1, M, 1, 0, 1, M, 1, M],
          [M, M, 1, M, 1, 0, M, M, 1],
          [M, M, M, 1, M, M, 0, 1, M],
          [M, M, M, M, 1, M, 1, 0, 1],
          [M, M, M, M, M, 1, M, 1, 0] ]
    all_table = Generate_router_tabel(G)     # 生成路由表
    # all_table输出的是每个节点，到剩余所有节点的最短路径
    print(all_table)

    print()

    test(G,all_table)