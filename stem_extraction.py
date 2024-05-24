import os
import numpy as np

# # 原始点云数据所在文件夹路径
# input_folder_path = r"D:\DESKTOP\Thesiscode\seg_train_dataset"
#
# # 新生成的txt文件保存的文件夹路径
# output_folder_path = r"D:\DESKTOP\Thesiscode\stem_after_classification"
#
# # 创建保存输出文件的文件夹（如果不存在）
# if not os.path.exists(output_folder_path):
#     os.makedirs(output_folder_path)

def extract_stem_points(input_file_path, output_file_path):
    # 从原始点云数据中提取属于树干的部分并保存到新的文件中
    data = np.loadtxt(input_file_path)

    # 找到最后三列是255 0 0的行
    stem_rows = np.all(data[:, -3:] == [255, 0, 0], axis=1)

    # 提取属于树干的点
    stem_points = data[stem_rows]

    # 保存到新文件
    np.savetxt(output_file_path, stem_points[:, :-3], fmt='%.6f')  # 删除最后三列

# # 遍历原始点云数据文件夹中的每个txt文件
# for filename in os.listdir(input_folder_path):
#     if filename.endswith(".txt"):
#         input_file_path = os.path.join(input_folder_path, filename)
#         output_file_path = os.path.join(output_folder_path, f"stem_{filename}")
#
#         # 提取属于树干的部分并保存到新文件
#         extract_stem_points(input_file_path, output_file_path)
