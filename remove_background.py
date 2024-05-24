import laspy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# read point cloud file
las_file_path = r"D:\DESKTOP\Thesiscode\HQPLR144V1_01_Output_laz1_4_b20_gr_z_class.las"
las_file = laspy.read(las_file_path)

# get x y z from point cloud
x = las_file.x
y = las_file.y
z = las_file.z


# create 5x5 grid(m)
grid_size = 4

# get the xyz max and min values
x_min = x.min()
x_max = x.max()
y_min = y.min()
y_max = y.max()


# init array
grid_z_values = np.zeros((int((x_max - x_min) / grid_size) + 1, int((y_max - y_min) / grid_size) + 1))
grid_point_counts = np.zeros_like(grid_z_values)

# Distribute point cloud data to a grid and update local minima
for i in range(len(las_file.points)):
    x_point, y_point, z_point = x[i], y[i], z[i]
    grid_x_index = int((x_point - x_min) / grid_size)
    grid_y_index = int((y_point - y_min) / grid_size)

    if z_point < grid_z_values[grid_x_index, grid_y_index] or grid_point_counts[grid_x_index, grid_y_index] == 0:
        grid_z_values[grid_x_index, grid_y_index] = z_point

    grid_point_counts[grid_x_index, grid_y_index] += 1

# calculate the difference of height and mark the point not ground
# tree detection 2m tree segmentation 1.3m
ground_threshold = 1.3

# create new las file
out_las_file = laspy.create(point_format=las_file.header.point_format, file_version=las_file.header.version)


# mark non ground points
is_ground = np.zeros(len(las_file.points), dtype=bool)
for i in range(len(las_file.points)):
    x_point, y_point, z_point = x[i], y[i], z[i]
    grid_x_index = int((x_point - x_min) / grid_size)
    grid_y_index = int((y_point - y_min) / grid_size)
    local_min_z = grid_z_values[grid_x_index, grid_y_index]

    if z_point - local_min_z < ground_threshold:
        is_ground[i] = True

# store the tree points in new file
out_las_file.points = las_file.points[~is_ground]



out_las_file.write(r"D:\DESKTOP\Thesiscode\non_ground_tree_detection.las")


# plot
# fig = plt.figure()
# ax = fig.add_subplot(111, projection="3d")

# # plot
# ax.scatter(x, y, z, s=1, c="b", marker=".")
#
#
# ax.set_xlabel("X")
# ax.set_ylabel("Y")
# ax.set_zlabel("Z")
# ax.set_title("3D point cloud visualization")
#
# # dhow point cloud
# plt.show()
#
# #las_file.close()




