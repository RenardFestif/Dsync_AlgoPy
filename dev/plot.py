from matplotlib import pyplot as plt

x = [1,2,3,4,5,6,7,8,9,10]
y = [122, 134, 11, 98, 295, 853, 8, 59, 932, 139]
y2 = [12, 14, 11, 9, 95, 53, 8, 59, 92, 139]



fig, ax1 = plt.subplots()

ax1.set_xlabel('temps')

ax1.set_ylabel('sin')
ax1.plot(x, y, color='red')


ax2 = ax1.twinx()  
ax2.set_ylabel('cos')  
ax2.plot(x, y2, color='green')

fig.tight_layout()
plt.show()