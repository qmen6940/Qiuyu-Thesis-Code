import os
import numpy as np


def load_point_cloud_from_txt(file_path):
    # 从txt文件中读取点云数据
    points = np.loadtxt(file_path)
    return points


def split_point_cloud_along_x(points, num_sections):
    # 计算点云的x轴范围
    min_x = np.min(points[:, 0])
    max_x = np.max(points[:, 0])
    x_range = max_x - min_x

    # 计算每个区段的x轴长度
    section_width = x_range / num_sections

    # 按x轴等距分割点云
    sections = []
    for i in range(num_sections):
        start_x = min_x + i * section_width
        end_x = start_x + section_width
        # 选择在当前区间内的点
        section_points = points[(points[:, 0] >= start_x) & (points[:, 0] < end_x)]
        sections.append(section_points)

    return sections


# 示例用法
# file_path = r'D:\DESKTOP\Thesiscode\classed2.txt'  # 点云txt文件路径
# output_directory = r'D:\DESKTOP\Thesiscode\after_in_pieces'  # 输出文件夹路径

file_path = r'D:\DESKTOP\Thesiscode\notclass_xyz.txt'  # 点云txt文件路径
output_directory = r'D:\DESKTOP\Thesiscode\after_in_pieces_new'  # 输出文件夹路径

num_sections = 50  # 要分割成的份数

# 从txt文件中加载点云数据
points = load_point_cloud_from_txt(file_path)

# 按x轴等距分割点云
sections = split_point_cloud_along_x(points, num_sections)

# 创建输出文件夹
os.makedirs(output_directory, exist_ok=True)

import os
import numpy as np

# 定义格式字符串
# format_str = '%.4f %.4f %.4f %.4f %.4f %.4f'
format_str = '%.4f %.4f %.4f %.4f %.4f %.4f %.4f'
# %d %d %d %d

# 从50开始
i = 50

# 输出或保存分割后的点云
for section_index, section in enumerate(sections):
    print(f"Section {i} has {len(section)} points")
    # 构建输出文件路径
    output_file_path = os.path.join(output_directory, f"section_{i}.txt")
    # 保存每个部分的点云到txt文件
    np.savetxt(output_file_path, section, fmt=format_str)
    i += 1
