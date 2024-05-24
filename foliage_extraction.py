import os
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull

# def extract_foliage_points(input_file_path, output_file_path):
#     # 从原始点云数据中提取属于树干的部分并保存到新的文件中
#     data = np.loadtxt(input_file_path)
#
#     # 找到最后三列是0 255 0的行
#     foliage_rows = np.all(data[:, -3:] == [0, 255, 0], axis=1)
#
#     # 提取属于树干的点
#     foliage_points = data[foliage_rows]
#
#     # 保存到新文件
#     np.savetxt(output_file_path, foliage_points[:, :-3], fmt='%.6f')  # 删除最后三列
def extract_foliage_points(input_file_path, output_file_path, eps=0.5, min_samples=10):
    # 从文件加载点云数据
    data = np.loadtxt(input_file_path)
    min_z_data = np.loadtxt(r'D:\DESKTOP\Thesiscode\findmax.txt')
    height_threshold = np.max(min_z_data[:, 2])  # 假设Z坐标是第三列
    print(height_threshold)

    # 找到标记为绿色的点（树叶和误标的树干点）
    green_points = data[np.all(data[:, -3:] == [0, 255, 0], axis=1)]

    # 应用DBSCAN聚类算法，eps和min_samples参数需要根据实际数据调整
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(green_points[:, :3])  # 只使用XYZ坐标进行聚类

    # 标签为-1的点被视为噪声，通常会是孤立的树叶点
    foliage_points = green_points[db.labels_ == -1]
    foliage_points = foliage_points[foliage_points[:, 2] > height_threshold]

    # 额外的步骤：使用凸包（Convex Hull）来识别与主树干空间分离的点
    if foliage_points.shape[0] > 0:
        hull = ConvexHull(foliage_points[:, :3])
        foliage_points = foliage_points[hull.vertices, :]


    # foliage_points = green_points

    # 保存提取的树叶点，不包含颜色信息
    np.savetxt(output_file_path, foliage_points[:, :-3], fmt='%.6f')

# 原始点云数据所在文件夹路径
input_folder_path = r"D:\DESKTOP\Thesiscode\seg_train_dataset"

# 新生成的txt文件保存的文件夹路径
output_folder_path = r"D:\DESKTOP\Thesiscode\foliage_after_classification"

# 创建保存输出文件的文件夹（如果不存在）
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
# 遍历原始点云数据文件夹中的每个txt文件
for filename in os.listdir(input_folder_path):
    if filename.endswith(".txt"):
        input_file_path = os.path.join(input_folder_path, filename)
        output_file_path = os.path.join(output_folder_path, f"foliage_{filename}")

        # 提取属于树干的部分并保存到新文件
        extract_foliage_points(input_file_path, output_file_path, eps=0.02, min_samples=20)