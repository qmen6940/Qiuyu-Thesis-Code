import pandas as pd
# from pyntcloud import PyntCloud
#
# # 加载MLP文件
# mlp_file = r"D:\DESKTOP\Thesiscode\pointnet_forest\log\sem_seg\2024-02-06_16-57\visual\tree21_pred.obj"
# cloud = PyntCloud.from_file(mlp_file)
#
# # 获取点云数据
# points = cloud.points
#
# # 将点云数据保存为TXT文件
# txt_file = r"D:\DESKTOP\txt\tree21"
# points.to_csv(txt_file, sep=' ', index=False, header=False)


import pandas as pd

# 定义一个自定义的函数来读取MLP文件
def read_mlp_file(file_path):
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            # 如果数据行以'v'开头，表示是点的数据行
            if line.startswith('v'):
                # 假设数据格式为'v x y z'，使用空格分割
                values = line.strip().split()
                # 将x、y、z转换为浮点数并追加到points列表中
                points.append([float(values[1]), float(values[2]), float(values[3])])
    return pd.DataFrame(points)


# 加载MLP文件
mlp_file = r"D:\DESKTOP\Thesiscode\pointnet_forest\log\sem_seg\2024-02-06_16-57\visual\section_84_pred.obj"
points_df = read_mlp_file(mlp_file)

# 检查数据
print(points_df.head())

# 将点云数据保存为TXT文件
txt_file = r"D:\DESKTOP\txt\section84.txt"
points_df.to_csv(txt_file, sep=' ', index=False, header=False)