import numpy as np
from sklearn.cluster import DBSCAN
import scipy.spatial
import os

# 加载点云数据
def convert_txt_to_npy(txt_file_path, npy_file_path):
    # 读取txt文件
    data = np.loadtxt(txt_file_path)
    # 保存为npy文件
    np.save(npy_file_path, data)

# 使用转换功能
txt_file_path = r'D:\DESKTOP\Thesiscode\dataset_txt.txt'  # 指定txt文件路径
npy_file_path = r'D:\DESKTOP\Thesiscode\dataset_npy.npy'  # 指定转换后的npy文件路径

# 将txt转换为npy
convert_txt_to_npy(txt_file_path, npy_file_path)
def load_point_cloud(npy_file_path):
    data = np.load(npy_file_path)
    points = data[:, :3]  # xyz坐标
    colors = data[:, 3:6]  # rgb颜色
    return points, colors

# 标记树干
def extract_tree_trunks(points, colors):
    # 找出所有红色点（树干）
    trunk_indices = np.all(colors == [255, 0, 0], axis=1)
    trunks = points[trunk_indices]
    return trunks, trunk_indices

# 使用DBSCAN聚类分割每个树干
def cluster_trunks(trunks, eps=1, min_samples=5):
    # 使用给定的eps和min_samples作为DBSCAN参数
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(trunks)
    labels = clustering.labels_
    return labels

# 加载npy格式的点云数据
npy_file_path = r'D:\DESKTOP\Thesiscode\dataset_npy.npy'  # 指定npy文件路径
points, colors = load_point_cloud(npy_file_path)

# 提取树干点
trunks, trunk_indices = extract_tree_trunks(points, colors)

# 设置DBSCAN参数
eps = 1  # 这个值需要根据您的数据点的密度和分布来调整
min_samples = 5  # 树干上最小的点的数量

# 聚类树干点
trunk_labels = cluster_trunks(trunks, eps=eps, min_samples=min_samples)

# 使用KDTree找出每个树干聚类中所有点及其周围1以内的点
kdtree = scipy.spatial.KDTree(points)

# 假设你有一个文件夹路径
output_folder = r"D:\DESKTOP\Thesiscode\seg_train_dataset"

# 创建输出文件夹
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for i in np.unique(trunk_labels):
    if i == -1:  # -1是噪声点
        continue

    # 选择当前聚类标签的树干点
    trunk_points = trunks[trunk_labels == i]

    # 找到树干聚类中所有点及其周围1以内的点
    indices = kdtree.query_ball_point(trunk_points, r=1)
    all_points_indices = np.unique([j for sublist in indices for j in sublist])
    all_points = points[all_points_indices]
    all_colors = colors[all_points_indices]

    # 保存整棵树的点云及其颜色为txt文件，保存到输出文件夹中
    output_file_path = os.path.join(output_folder, f'tree_{i}.txt')
    np.savetxt(output_file_path, np.hstack((all_points, all_colors)), fmt='%f %f %f %d %d %d')

