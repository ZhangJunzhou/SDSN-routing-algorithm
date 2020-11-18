# 1）准备数据
# x = range(len(movie_name))

# # 2）创建画布
# # plt.figure(figsize=(10,5), dpi=100)

# # 3）绘制柱状图
# plt.bar(x, first_day, width=0.2, label="Dijkstra算法")
# plt.bar([i+0.2 for i in x], first_weekend, width=0.2, label="选择性迭代最短路径算法")
# plt.xlabel('平 均 拥 塞 链 路 数 量',fontsize=16)
# plt.ylabel('最 大 承 载 流 量 大 小 /Mbs',fontsize=16) 
# # 显示图例
# plt.legend()

# # 修改x轴刻度显示
# plt.xticks([i+0.1 for i in x], movie_name ,fontsize=15)
# # 4）显示图像
# plt.show()


# 论文最后的柱状图


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
# movie_name = ['0.1','0.2','0.3']



def auto_label(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height), # put the detail data
                    xy=(rect.get_x() + rect.get_width() / 2, height), # get the center location.
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def auto_text(rects):
    for rect in rects:
        ax.text(rect.get_x(), rect.get_height(), rect.get_height(), ha='left', va='bottom')


labels = ['20', '35', '50', '65', '80', '95']
[[2393.8191650180142, 359.4673563366046], [2283.939238497484, 493.00870412252283], [2177.60940614406, 618.6711864161103], [2074.488966694445, 739.4485643853906], [1975.8857100152463, 847.4750366388744], [1889.754806068938, 940.2511003573287]]
[[2393.6895186338156, 359.14298493037535], [2282.715552672478, 491.6823247717679], [2175.3389340861763, 616.7767259014726], [2070.5850711580147, 736.598015542877], [1970.896653670441, 840.6758082127606], [1885.6373667215923, 925.1363313595394]]

[[2302.1067913828906, 392.9329218578492], [2131.093988898009, 494.402601448427], [1965.8912266233058, 577.4082930049647], [1800.4550490145075, 655.5753496581731], [1647.4907709645652, 718.009261457111], [1502.0831359318852, 761.7392299624197]]
[[2302.1995812975865, 387.7658000127175], [2132.21681117385, 477.39189763669356], [1968.6252291740993, 554.1437591084466], [1798.872194739347, 628.2163926347858], [1639.43143172761, 685.7992694732709], [1492.3925784063415, 724.3395031572484]]


# Dijkstra
D_E = [181765221, 168606913, 155343828, 142279056, 130085523, 118494041]
D_V = [393,494,577,656,718,762]

# SIDA
SI_E = [181767790, 168578286, 155147623, 142100397, 129567000, 117933899]
SI_V = [388, 477, 554, 628, 686, 724]

#SSLB
C_E = [188989059, 180339236, 171650302, 163601294, 155911231, 149233272]
C_V = [388, 475, 552, 625, 679, 709]

# LCDA
LC_E = [175782344, 158654188, 141238124, 124923693, 109193907, 95145040]
LC_V = [434, 524, 600, 658, 700, 716]
#[432, 531, 625, 717, 803, 885]

# labels = ['20']
index = np.arange(len(labels))
width = 0.2

fig, ax = plt.subplots()
plt.plot(labels,SI_V,color="lightcoral")
plt.plot(labels,C_V,color="blue")
rect1 = ax.bar(index - width / 2, SI_V, color ='lightcoral', width=width, label ='SIDA')
rect2 = ax.bar(index + width / 2, C_V, color ='blue', width=width, label ='SSLB')

# ax.set_title('Scores by gender')
ax.set_xticks(ticks=index)
ax.set_xticklabels(labels)
plt.xlabel('Number of business flows',fontsize=12)
 
plt.ylabel('Standard deviation of link residual bandwidth / Mbs',fontsize=12)

ax.set_ylim(350, 750)
# auto_label(rect1)
# auto_label(rect2)
auto_text(rect1)
auto_text(rect2)

ax.legend(loc='best', fontsize=18)
fig.tight_layout()
plt.savefig("SIDA与SSLB剩余带宽标准差.tif", dpi=300)
# plt.show()
