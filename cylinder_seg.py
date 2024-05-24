import numpy as np
import os

# 由于不能直接访问您的文件系统，以下代码是基于文件已经被加载到本地环境的情况

# 加载点云数据
points = np.loadtxt(r'D:\DESKTOP\Thesiscode\notclass_xyz.txt')  # 请确保文件路径是正确的

def in_cylinder(center, point, radius, zmin, zmax):
    x, y, z = point[:3]  # Only take the first three values
    cx, cy = center
    return (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2 and zmin <= z <= zmax

def generate_centers(points, radius):
    # 计算x和y的边界
    xmin, xmax = np.min(points[:, 0]), np.max(points[:, 0])
    ymin, ymax = np.min(points[:, 1]), np.max(points[:, 1])

    # 计算步长为圆柱体直径的网格
    step = radius * 2
    x_centers = np.arange(xmin, xmax, step)
    y_centers = np.arange(ymin, ymax, step)

    # 创建中心点列表
    centers = []
    for x in x_centers:
        for y in y_centers:
            centers.append((x, y))
    return centers

def cut_into_cylinders(points, radius, zmin, zmax, centers):
    # 使用提供的中心点列表来切割点云
    cylinders = []
    for center in centers:
        cylinder = []
        for point in points:
            if in_cylinder(center, point, radius, zmin, zmax):
                cylinder.append(point)
        cylinders.append(np.array(cylinder))
    return cylinders

# 加载点云数据
# points = np.loadtxt('path_to_your_txt_file')
points = np.loadtxt(r'D:\DESKTOP\Thesiscode\notclass_xyz.txt')  # 请确保文件路径是正确的
# 计算Z轴的范围和高度
zmin = np.min(points[:, 2])
zmax = np.max(points[:, 2])

# 定义圆柱体半径
radius = 1.25  # 直径为2.5米的圆柱体

# 生成中心点列表
centers = generate_centers(points, radius)

# 执行切割操作
cylinders = cut_into_cylinders(points, radius, zmin, zmax, centers)
# 确保输出文件夹存在，如果不存在则创建
output_folder = r'D:\DESKTOP\Thesiscode\after_in_cylinder'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 执行切割操作
cylinders = cut_into_cylinders(points, radius, zmin, zmax)

# 保存每个圆柱体的点云到指定文件夹
for i, cylinder in enumerate(cylinders):
    # 构建每个圆柱体的点云文件的完整路径
    cylinder_filename = os.path.join(output_folder, f'cylinder_{i}.txt')
    # 将点云数据保存为TXT文件
    np.savetxt(cylinder_filename, cylinder)


