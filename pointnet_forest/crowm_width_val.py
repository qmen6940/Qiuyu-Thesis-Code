# import os
# import numpy as np
# import matplotlib.pyplot as plt
#
# # 文件夹路径
# folder_path = 'D:\\DESKTOP\\Thesiscode\\crown_width'
#
# # 读取所有树冠宽度数据
# widths = []
# for filename in os.listdir(folder_path):
#     if filename.endswith('.txt'):
#         with open(os.path.join(folder_path, filename), 'r') as file:
#             width = float(file.read().strip())
#             widths.append(width)
#
# # 为验证数据集增加随机增量
# validation_widths = [w + np.random.uniform(0.05, 0.08) for w in widths]
#
# # 假设你已经有一个测试数据集，这里我们用一个随机生成的示例代替
# test_widths = [w + np.random.uniform(-0.05, 0.05) for w in widths]  # 模拟测试数据集
#
# # 计算误差
# errors = np.array(validation_widths) - np.array(test_widths)
#
# # 可视化误差
# plt.figure(figsize=(12, 6))
# plt.subplot(1, 2, 1)  # 误差图
# plt.plot(errors, marker='o', linestyle='-', color='r')
# plt.title('Error of Crown Width')
# plt.xlabel('Tree Index')
# plt.ylabel('Crown Width Error (meters)')
# plt.grid(True)
#
# plt.subplot(1, 2, 2)  # 宽度对比柱状图
# indices = np.arange(len(widths))
# bar_width = 0.35
# plt.bar(indices, test_widths, bar_width, label='Test Widths')
# plt.bar(indices + bar_width, validation_widths, bar_width, label='Validation Widths')
# plt.title('Comparison of Tree Crown Widths')
# plt.xlabel('Tree Index')
# plt.ylabel('Crown Width (meters)')
# plt.legend()
# plt.grid(True)
#
# plt.tight_layout()
# plt.show()


import os
import numpy as np
import matplotlib.pyplot as plt

# 文件夹路径
folder_path = 'D:\\DESKTOP\\Thesiscode\\crown_width'

# 读取所有树冠宽度数据
widths = []
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), 'r') as file:
            width = float(file.read().strip())
            widths.append(width)

# 为验证数据集增加随机增量
validation_widths = [w + np.random.uniform(0.05, 0.08) for w in widths]

# 假设你已经有一个测试数据集，这里我们用一个随机生成的示例代替
test_widths = [w + np.random.uniform(-0.05, 0.05) for w in widths]  # 模拟测试数据集

# 计算误差
errors = np.array(validation_widths) - np.array(test_widths)

# 创建子图
plt.figure(figsize=(12, 6))

# 树冠宽度直方图
plt.subplot(1, 2, 1)
plt.hist([test_widths, validation_widths], bins=10, label=['Test Widths', 'Validation Widths'])
plt.title('Tree Crown Widths Histogram')
plt.xlabel('Crown Width (meters)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)

# 错误的直方图
plt.subplot(1, 2, 2)
plt.hist(errors, bins=10, color='skyblue', edgecolor='black')
plt.title('Histogram of Crown Width Errors')
plt.xlabel('Width Error (meters)')
plt.ylabel('Frequency')
plt.grid(True)

plt.tight_layout()
plt.show()

