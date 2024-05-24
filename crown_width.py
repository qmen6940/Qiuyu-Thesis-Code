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


def process_and_fit_circles(input_folder_path, output_folder_path, output_image_folder_path):
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

            radius = radius # + 0.15
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


input_folder_path = r"D:\DESKTOP\Thesiscode\foliage_after_classification"
output_folder_path = r"D:\DESKTOP\Thesiscode\crown_width"
output_image_folder_path = r"D:\DESKTOP\Thesiscode\circle_fitting_crown_visualization"

process_and_fit_circles(input_folder_path, output_folder_path, output_image_folder_path)


