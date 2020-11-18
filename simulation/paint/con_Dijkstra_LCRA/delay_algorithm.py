import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

delay_A = np.array([83.14832513739559, 84.18998341122571, 86.09493378425017, 87.90097260022615, 88.53483198286916, 90.0307558698184, 90.15094431847919, 92.75835863347007, 93.98914278050097])
delay_B = np.array([83.8730084267728, 84.35792407896753, 86.88189456663389, 90.54694217573044, 92.25084781567737, 94.5107786394753, 96.1604531900372, 99.67651038822368, 101.6720880907984])
delay_C = np.array([84.56818119441542, 84.90323666391701, 87.44547431967476, 93.26043372976912, 95.73959493399792, 97.8151031852617, 99.42735542964473, 104.33654532622809, 107.13376728645926])
delay_TCRA = []
for i in range(0, len(delay_A)):
    delay_TCRA.append((delay_A[i] + delay_B[i] + delay_C[i]) / 3)
TCRA = np.array(delay_TCRA)

LCRA = np.array([88.31353951464986, 93.0494070984528, 101.60866173270779, 120.12029076511138, 126.35170871830739, 132.85184597883594, 140.58175784934963, 158.0903420198346, 179.84384137102455])
Dijkstra = np.array([94.38757307200264, 102.12380386399332, 118.72913002920284, 161.83719313228937, 179.79949514504807,258.35864989931218, 309.0693744619886, 342.96208840915784, 424.4298013224683])


# label在图示(legend)中显示。若为数学公式,则最好在字符串前后添加"$"符号
# color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
# 线型：-  --   -.  :    ,
# marker：.  ,   o   v    <    *    +    1
plt.figure(figsize=(8, 5))
plt.grid(linestyle="--")  # 设置背景网格线为虚线
ax = plt.gca()
# ax.spines['top'].set_visible(False)  # 去掉上边框
# ax.spines['right'].set_visible(False)  # 去掉右边框


plt.plot(x, TCRA, marker='x', color="blue", label="TCRA", linewidth=1.5)
plt.plot(x, LCRA, marker='^', color="green", label="LCRA", linewidth=1.5)
plt.plot(x, Dijkstra, marker='s', color="red", label="Dijkstra", linewidth=1.5)

group_labels = ['20', '30', '40', '50', '60', '70', '80', '90','100']  # x轴刻度的标识
plt.xticks(x, group_labels, fontsize=12, fontweight='bold')  # 默认字体大小为10
plt.yticks(fontsize=13, fontweight='bold')
# plt.title("example", fontsize=12, fontweight='bold')  # 默认字体大小为12
plt.xlabel("Number of traffic flows", fontsize=13, fontweight='bold')
plt.ylabel("Mean end-to-end delay(ms)", fontsize=13, fontweight='bold')
plt.xlim(0.9, 9.1)  # 设置x轴的范围
# plt.ylim(80, 120)

# plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=12, fontweight='bold')  # 设置图例字体的大小和粗细

plt.savefig('./delay_algorithm.png', format='png')  # 建议保存为svg格式,再用inkscape转为矢量图emf后插入word中
plt.show()