import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
delay_A = np.array([0.14401743, 0.162533, 0.25483544, 0.28694658, 0.40532604, 0.40707673, 0.44358423, 0.51367936,0.60019568])
delay_B = np.array([0.19082038, 0.21199,  0.29173674, 0.36710548, 0.5189701,  0.57392202, 0.76794961, 0.85453205, 0.99011003])
delay_C = np.array([0.05145234, 0.045454, 0.05075625, 0.06866536, 0.05795721, 0.06825621, 0.07765463, 0.08742566, 0.09902566])

delay_TCRA = []
for i in range(0, len(delay_A)):
    delay_TCRA.append((delay_A[i] + delay_B[i] + delay_C[i]) / 3)

print(delay_TCRA)

# print()得出 delay_TCRA=       [0.12876334, 0.13999236, 0.199109897, 0.24090964, 0.3274133, 0.349033336, 0.42970949, 0.48521967, 0.56398666]
LCRA = np.array([0.12943157, 0.14194843,  0.21965438, 0.26863048, 0.3928825,  0.45377626, 0.60158749, 0.72786384, 0.90224962])
Dijkstra = np.array([0.13248944, 0.14545432,  0.43451326, 0.59746353, 0.7974562,  1.35943154, 1.83543154, 2.13245314, 2.91435435])


# label在图示(legend)中显示。若为数学公式,则最好在字符串前后添加"$"符号
# color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
# 线型：-  --   -.  :    ,
# marker：.  ,   o   v    <    *    +    1
plt.figure(figsize=(10, 5))
plt.grid(linestyle="--")  # 设置背景网格线为虚线
ax = plt.gca()
# ax.spines['top'].set_visible(False)  # 去掉上边框
# ax.spines['right'].set_visible(False)  # 去掉右边框


plt.plot(x, delay_TCRA, marker='x', color="blue", label="TCRA", linewidth=1.5)
plt.plot(x, LCRA, marker='^', color="green", label="LCRA", linewidth=1.5)
plt.plot(x, Dijkstra, marker='s', color="red", label="Dijkstra", linewidth=1.5)

group_labels = ['20', '30', '40', '50', '60', '70', '80', '90','100']  # x轴刻度的标识
plt.xticks(x, group_labels, fontsize=12, fontweight='bold')  # 默认字体大小为10
plt.yticks(fontsize=13, fontweight='bold')
# plt.title("example", fontsize=12, fontweight='bold')  # 默认字体大小为12
plt.xlabel("Number of traffic flows", fontsize=13, fontweight='bold')
plt.ylabel("Packet loss rate(%)", fontsize=13, fontweight='bold')
plt.xlim(0.9, 9.1)  # 设置x轴的范围
# plt.ylim(80, 120)

# plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=12, fontweight='bold')  # 设置图例字体的大小和粗细

plt.savefig('./packet_loss_rate_algorithm.png', format='png')  # 建议保存为svg格式,再用inkscape转为矢量图emf后插入word中
plt.show()