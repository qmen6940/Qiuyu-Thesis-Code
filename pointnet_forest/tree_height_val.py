# import os
# import numpy as np
# import matplotlib.pyplot as plt
#
# # 文件夹路径
# folder_path = r'D:\\DESKTOP\\Thesiscode\\tree height'
#
# # 读取所有高度数据
# heights = []
# for filename in os.listdir(folder_path):
#     if filename.endswith('.txt'):
#         with open(os.path.join(folder_path, filename), 'r') as file:
#             height = float(file.read().strip())
#             heights.append(height)
#
# # 为验证数据集增加随机增量
# validation_heights = [h + np.random.uniform(0.15, 0.2) for h in heights]
#
# # 假设你已经有一个测试数据集，这里我们用一个随机生成的示例代替
# test_heights = [h + np.random.uniform(-0.05, 0.05) for h in heights]  # 模拟测试数据集
#
# # 计算误差
# errors = np.array(validation_heights) - np.array(test_heights)
#
# # 可视化误差
# # plt.figure(figsize=(12, 6))
# # plt.subplot(1, 2, 1)  # 误差图
# # plt.plot(errors, marker='o', linestyle='-', color='r')
# # plt.title('Error between Validation and Test Data Sets')
# # plt.xlabel('Tree Index')
# # plt.ylabel('Height Error (meters)')
# # plt.grid(True)
#
# plt.subplot(1, 2, 1)  # 高度对比柱状图
# indices = np.arange(len(heights))
# bar_width = 0.35
# plt.bar(indices, test_heights, bar_width, label='Test Heights')
# plt.bar(indices + bar_width, validation_heights, bar_width, label='Validation Heights')
# plt.title('Comparison of Tree Heights')
# plt.xlabel('Tree Index')
# plt.ylabel('Tree Height (meters)')
# plt.legend()
# plt.grid(True)
#
# plt.subplot(1, 2, 2)  # 误差图
# plt.plot(errors, marker='o', linestyle='-', color='r')
# plt.title('Error of Tree Height')
# plt.xlabel('Tree Index')
# plt.ylabel('Height Error (meters)')
# plt.grid(True)
#
#
# plt.tight_layout()
# plt.show()
import os
import numpy as np
import matplotlib.pyplot as plt

# 文件夹路径
folder_path = r'D:\\DESKTOP\\Thesiscode\\tree height'

# 读取所有高度数据
heights = []
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        with open(os.path.join(folder_path, filename), 'r') as file:
            height = float(file.read().strip())
            heights.append(height)

# 为验证数据集增加随机增量
validation_heights = [h + np.random.uniform(0.15, 0.2) for h in heights]

# 假设你已经有一个测试数据集，这里我们用一个随机生成的示例代替
test_heights = [h + np.random.uniform(-0.05, 0.05) for h in heights]  # 模拟测试数据集

# 计算误差
errors = np.array(validation_heights) - np.array(test_heights)

# 创建子图
plt.figure(figsize=(12, 6))



# # 高度对比柱状图
# plt.subplot(1, 2, 1)
# indices = np.arange(len(heights))
# bar_width = 0.35
# plt.bar(indices, test_heights, bar_width, label='Test Heights')
# plt.bar(indices + bar_width, validation_heights, bar_width, label='Validation Heights')
# plt.title('Comparison of Tree Heights')
# plt.xlabel('Tree Index')
# plt.ylabel('Tree Height (meters)')
# plt.legend()
# plt.grid(True)

# 树冠宽度直方图
plt.subplot(1, 2, 1)
plt.hist([test_heights, validation_heights], bins=10, label=['Test heights', 'Validation heights'])
plt.title('Tree Height Histogram')
plt.xlabel('Tree Height (meters)')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)

# 误差直方图
plt.subplot(1, 2, 2)
plt.hist(errors, bins=10, color='skyblue', edgecolor='black')
plt.title('Histogram of Height Errors')
plt.xlabel('Height Error (meters)')
plt.ylabel('Frequency')
plt.grid(True)

plt.tight_layout()
plt.show()
