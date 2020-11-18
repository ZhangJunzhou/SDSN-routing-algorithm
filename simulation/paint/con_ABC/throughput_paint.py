import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
classA = np.array(np.divide([13835.224193880671, 19126.539448485117, 25185.66198347935, 29834.91349213355, 37289.503249316534, 43076.27228921232, 45938.54419439832, 51951.388315011325, 58662.83414284349], 1000))
classB = np.array(np.divide([27036.519536554148, 36439.24106148178, 50774.457208929336, 60060.42543300751, 72111.86040578097, 79665.9954741205, 84846.34478962605, 90478.89889594565, 94588.9712941622], 1000))
classC = np.array(np.divide([27948.05696270698, 38813.69818954628, 49531.36158722392, 61653.0085653509, 73379.3557875285, 82613.50590373555, 88934.89585775476, 99364.22120163609, 105063.47000471184], 1000))

# label在图示(legend)中显示。若为数学公式,则最好在字符串前后添加"$"符号
# color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
# 线型：-  --   -.  :    ,
# marker：.  ,   o   v    <    *    +    1
plt.figure(figsize=(10, 5))
plt.grid(linestyle="--")  # 设置背景网格线为虚线
ax = plt.gca()
# ax.spines['top'].set_visible(False)  # 去掉上边框
# ax.spines['right'].set_visible(False)  # 去掉右边框


plt.plot(x, classA, marker='x', color="blue", label="class A", linewidth=1.5)
plt.plot(x, classB, marker='^', color="green", label="class B", linewidth=1.5)
plt.plot(x, classC, marker='s', color="red", label="class C", linewidth=1.5)

group_labels = ['20', '30', '40', '50', '60', '70', '80', '90','100']  # x轴刻度的标识
plt.xticks(x, group_labels, fontsize=13, fontweight='bold')  # 默认字体大小为10
plt.yticks(fontsize=13, fontweight='bold')
# plt.title("example", fontsize=12, fontweight='bold')  # 默认字体大小为12
plt.xlabel("Number of traffic flows", fontsize=13, fontweight='bold')
plt.ylabel("Data throughput(Mbps)", fontsize=13, fontweight='bold')
plt.xlim(0.9, 9.1)  # 设置x轴的范围
# plt.ylim(80, 120)

# plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=12, fontweight='bold')  # 设置图例字体的大小和粗细

plt.savefig('./throughput_paint.png', format='png')  # 建议保存为svg格式,再用inkscape转为矢量图emf后插入word中
plt.show()