import numpy as np
import random

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
        pair_list[i] = ["A", pair_list[i], flow[i]]
    print(pair_list)
    print("the num of fow: ", len(pair_list))
    print("all flow: ", all_flow)
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
    print(pair_list)
    print("the num of fow: ", len(pair_list))
    print("all flow: ", all_flow)
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
    print(pair_list)
    print("the num of fow: ", len(pair_list))
    print("all flow: ", all_flow)
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


if __name__ == '__main__':
    pair_list = []
    all_flow = []

    # 产生A\B\C三种流，每种流的大小比值为1,2,3
    for i in range(0,9):
        for j in range(0,1):
            pairSingleA, flowSingleA = Generate_random_data_pairA(20 + i * 10)
            pairSingleB, flowSingleB = Generate_random_data_pairB(20 + i * 10)
            pairSingleC, flowSingleC = Generate_random_data_pairC(20 + i * 10)

    # pair_list = np.copy(pair_list)
    # print(pair_list)
    # all_flow = np.copy(all_flow)
    # print(all_flow)


