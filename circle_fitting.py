# import os
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from circle_fitting_3d import Circle3D
#
# def circle_fitting(file_path, output_folder, output_folder_image,  index):
#     # load xyz
#     point_cloud_data = np.loadtxt(file_path)
#
#     # read xyz
#     # x_coordinates = point_cloud_data[:, 0]
#     # y_coordinates = point_cloud_data[:, 1]
#     # z_coordinates = point_cloud_data[:, 2]
#     points = point_cloud_data[:, :3].tolist()
#
#     # circle 3d
#     circle_3d = Circle3D(points)
#     center = circle_3d.center
#     radius = circle_3d.radius
#     print("Center:", center)
#     print("Radius:", radius)
#
#     # save center coordinate and r
#     output_txt_path = os.path.join(output_folder, f"stem_parameters_{index}.txt")
#     with open(output_txt_path, 'w') as f:
#         f.write(f"{center[0]} {center[1]} {center[2]}\n")
#         f.write(f"{radius}\n")
#
#     # with open(output_txt_path, 'w') as f:
#     #       f.write(f"Center: {center[0]}, {center[1]}, {center[2]}\n")
#     #       f.write(f"Radius: {radius}\n")
#
#     # plot 3d
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection="3d")
#     circle_3d.plot(ax)
#     ax.text(center[0], center[1], center[2], 'X', color='red')
#     ax.text(center[0] + 0.1, center[1], center[2], 'Y', color='green')
#     ax.text(center[0], center[1] + 0.1, center[2], 'Z', color='blue')
#     ax.set_xlim([center[0] - radius, center[0] + radius])
#     ax.set_ylim([center[1] - radius, center[1] + radius])
#     ax.set_zlim([center[2] - radius, center[2] + radius])
#
#     # title
#     plt.title("Circle Fitting Visualization")
#
#     # save img
#     output_image_path = os.path.join(output_folder_image, f"stem_parameters_{index}.png")
#     plt.savefig(output_image_path)
#
#     # show
#     plt.show(block=False)
#     plt.pause(0.1)  # delay
#     plt.close()
#
# # path
# point_cloud_folder_path = r'D:\DESKTOP\Thesiscode\part_of_stem'
# output_folder_txt = r'D:\DESKTOP\Thesiscode\stem_parameters'
# output_folder_image = r'D:\DESKTOP\Thesiscode\circle_fitting_visualization'
#
# # create folder
# os.makedirs(output_folder_txt, exist_ok=True)
# os.makedirs(output_folder_image, exist_ok=True)
#
# # loop
# for i, filename in enumerate(os.listdir(point_cloud_folder_path)):
#     if filename.endswith(".txt"):
#         file_path = os.path.join(point_cloud_folder_path, filename)
#         circle_fitting(file_path, output_folder_txt, output_folder_image, i)





import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
import os

# circle fitting error
def calculate_residuals(circle_params, points):
    center_x, center_y, radius = circle_params
    return np.sqrt((points[:, 0] - center_x)**2 + (points[:, 1] - center_y)**2) - radius

# circle fitting
def fit_circle_to_points(points):
    # init center point: average value of xy
    mean_x = np.mean(points[:, 0])
    mean_y = np.mean(points[:, 1])
    initial_radius = (np.max(points[:, 0]) - np.min(points[:, 0])) / 2
    initial_guess = [mean_x, mean_y, initial_radius]

    # ls
    result = least_squares(calculate_residuals, initial_guess, args=(points,))
    return result.x


def process_and_fit_circles_DBH(input_folder_path, output_folder_path, output_image_folder_path):
    # create folder
    if not os.path.exists(output_image_folder_path):
        os.makedirs(output_image_folder_path)

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)


    # loop
    for filename in os.listdir(input_folder_path):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder_path, filename)
            output_file_path = os.path.join(output_folder_path, f"radius_{filename}")
            output_image_path = os.path.join(output_image_folder_path, f"circle_{filename}.png")

            # load txt
            points = np.loadtxt(input_file_path)

            # ignore z
            points_xy = points[:, :2]

            # circle fitting
            center_x, center_y, radius = fit_circle_to_points(points_xy)
            print(radius)
            # save txt
            with open(output_file_path, 'w') as f_output:
                f_output.write(f"{radius}\n")

            # plot
            fig, ax = plt.subplots()
            circle = plt.Circle((center_x, center_y), radius, color='blue', fill=False)
            ax.add_artist(circle)
            ax.plot(points_xy[:, 0], points_xy[:, 1], 'ro', markersize=2)
            ax.set_aspect('equal', adjustable='datalim')
            ax.plot(center_x, center_y, 'bx')
            plt.title(f"Circle Fitting - {filename}")

            # save img
            plt.savefig(output_image_path)
            plt.close(fig)

            print(f"Processed and saved visualization for {filename}")


# input_folder_path = r"D:\DESKTOP\Thesiscode\part_of_stem"
# output_folder_path = r"D:\DESKTOP\Thesiscode\stem_parameters"
# output_image_folder_path = r"D:\DESKTOP\Thesiscode\circle_fitting_visualization"
#
# process_and_fit_circles_DBH(input_folder_path, output_folder_path, output_image_folder_path)
# rpa
