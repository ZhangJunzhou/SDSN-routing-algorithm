#需要导入的库
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab  
import scipy.special as sps

M = 25600000

#2.2,6.0
shape,scale=3.10338,85.2079072   #2003-2006年西安骨干网的流量分布
s=np.random.gamma(shape,scale,10001)#在2.到2.之间随机生成1000个小数
# print(s[10000])

# count, bins, ignored = plt.hist(s, 50, normed=True)          #50：是50个条形图
count, bins, ignored  = plt.hist(s, 50)          #50：是50个条形图
y = bins**(shape-1)*(np.exp(-bins/scale)/(sps.gamma(shape)*scale**shape))
plt.plot(bins, y, linewidth=2, color='r')
plt.xlabel('$Flow/Mbs$')
plt.ylabel('$Probability$')
plt.title('Gamma Distribution')
plt.show()

s=s.tolist()
s.sort()
flow=[]
for i in range(101):
    flow.append(s[i*100])
print(flow)
print(s[-1])
import pdb
pdb.set_trace()
# print(count,bins,ignored)
plt.plot(bins,y,linewidth=2,color='r')
plt.show()


G=  [    [0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [1, M, M, M, M, M, M, 1, 0, M, M, M, 1, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, 0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, 1, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
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

weight=  [
         [0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [1, M, M, M, M, M, M, 1, 0, M, M, M, 1, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, 0, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, M, M, M, M, M, M, M, 1, 0, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
         [M, M, 1, M, M, M, M, M, M, M, 1, 0, 1, M, M, 1, M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
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