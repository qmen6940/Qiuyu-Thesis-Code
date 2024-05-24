import os
import numpy as np

# # 存储提取的树干点云数据的文件夹路径
# stem_folder_path = r'D:\DESKTOP\Thesiscode\stem_after_classification'
#
# # 存储截取点云后的文件夹路径
# part_of_stem_folder_path = r'D:\DESKTOP\Thesiscode\part_of_stem'

# # 创建保存输出文件的文件夹（如果不存在）
# if not os.path.exists(part_of_stem_folder_path):
#     os.makedirs(part_of_stem_folder_path)

def extract_part_of_stem(input_file_path, output_file_path, height_threshold=1.28):
    # 从树干点云数据中截取特定高度范围的点云并保存到新的文件中
    data = np.loadtxt(input_file_path)

    # 找到Z值最小的点
    min_z_index = np.argmin(data[:, 2])

    # 获取最小Z值
    min_z_value = data[min_z_index, 2]

    # 找到比Z值最小值大1.29米到1.31米的位置
    height_condition = np.logical_and(data[:, 2] > min_z_value + height_threshold, data[:, 2] <= min_z_value + 1.32)

    # 提取满足条件的点云
    selected_points = data[height_condition]

    # 保存到新文件
    np.savetxt(output_file_path, selected_points, fmt='%.6f')

# # 遍历提取的树干点云数据文件夹中的每个txt文件
# for filename in os.listdir(stem_folder_path):
#     if filename.endswith(".txt"):
#         input_file_path = os.path.join(stem_folder_path, filename)
#         output_file_path = os.path.join(part_of_stem_folder_path, f"part_of_stem_{filename}")
#
#         # 截取特定高度范围的点云并保存到新文件
#         extract_part_of_stem(input_file_path, output_file_path)
