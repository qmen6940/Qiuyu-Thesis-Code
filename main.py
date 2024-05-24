import os
import numpy as np
from stem_extraction import extract_stem_points
from DBH_seg import extract_part_of_stem
from circle_fitting import process_and_fit_circles_DBH
from foliage_extraction import extract_foliage_points
from tree_height import tree_height
from crown_height import crown_height
from crown_width import process_and_fit_circles

def main():
    script_folder = os.path.dirname(os.path.abspath(__file__))
    ################################   DBH Calculation    #######################################################################
    # stem extraction
    input_folder_path_seg_train_dataset = os.path.join(script_folder, "seg_train_dataset")
    output_folder_path_stem_after_classification = os.path.join(script_folder, "stem_after_classification")
    if not os.path.exists(output_folder_path_stem_after_classification):
        os.makedirs(output_folder_path_stem_after_classification)

    for filename in os.listdir(input_folder_path_seg_train_dataset):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder_path_seg_train_dataset, filename)
            output_file_path = os.path.join(output_folder_path_stem_after_classification, f"stem_{filename}")

            extract_stem_points(input_file_path, output_file_path)

    # stem seg at 1.3m and thickness 4cm
    input_folder_path_stem_after_classification = os.path.join(script_folder, 'stem_after_classification')
    output_folder_path_part_of_stem = os.path.join(script_folder, 'part_of_stem')

    if not os.path.exists(output_folder_path_part_of_stem):
        os.makedirs(output_folder_path_part_of_stem)

    for filename in os.listdir(input_folder_path_stem_after_classification):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder_path_stem_after_classification, filename)
            output_file_path = os.path.join(output_folder_path_part_of_stem, f"part_of_stem_{filename}")

            extract_part_of_stem(input_file_path, output_file_path)

    # circle fitting
    # path
    input_folder_path_part_of_stem = os.path.join(script_folder, 'part_of_stem')
    output_folder_path_stem_parameters = os.path.join(script_folder, 'stem_parameters')
    output_folder_path_circle_fitting_visualization = os.path.join(script_folder, 'circle_fitting_visualization')

    # create folder
    os.makedirs(output_folder_path_stem_parameters, exist_ok=True)
    os.makedirs(output_folder_path_circle_fitting_visualization, exist_ok=True)

    # loop
    # for i, filename in enumerate(os.listdir(input_folder_path_part_of_stem)):
    #     if filename.endswith(".txt"):
    #         file_path = os.path.join(input_folder_path_part_of_stem, filename)
    #         process_and_fit_circles_DBH(file_path, output_folder_path_stem_parameters, output_folder_path_circle_fitting_visualization)

    process_and_fit_circles_DBH(input_folder_path_part_of_stem, output_folder_path_stem_parameters, output_folder_path_circle_fitting_visualization)
    ########################################################################################################################################




    ############################ Tree Height Calculation #################################################################################

    input_folder_path_seg_train_dataset = os.path.join(script_folder, "seg_train_dataset")
    output_folder_path_tree_height = os.path.join(script_folder, "tree height")
    tree_height(input_folder_path_seg_train_dataset, output_folder_path_tree_height)

    ########################################################################################################################################


    ############################# Crown Height Calculation ###########################################################################

    # foliage extraction
    input_folder_path_seg_train_dataset = os.path.join(script_folder, "seg_train_dataset")
    output_folder_path_foliage_after_classification = os.path.join(script_folder, "foliage_after_classification")

    # create folder
    if not os.path.exists(output_folder_path_foliage_after_classification):
        os.makedirs(output_folder_path_foliage_after_classification)

    for filename in os.listdir(input_folder_path_seg_train_dataset):
        if filename.endswith(".txt"):
            input_file_path = os.path.join(input_folder_path_seg_train_dataset, filename)
            output_file_path = os.path.join(output_folder_path_foliage_after_classification, f"foliage_{filename}")
            extract_foliage_points(input_file_path, output_file_path, eps=0.02, min_samples=20)
    #Crown Height
    input_folder_path_foliage_after_classication = os.path.join(script_folder, "foliage_after_classification")
    output_folder_path_crown_height = os.path.join(script_folder, "crown_height")
    crown_height(input_folder_path_foliage_after_classication, output_folder_path_crown_height)
    ###################################################################################################################################




    ############################# Crown Width Calculation ############################################################################

    input_folder_path_foliage_after_classification = os.path.join(script_folder, "foliage_after_classification")
    output_folder_path_crown_width = os.path.join(script_folder, "crown_width")
    output_folder_path_circle_fitting_crown_visualization = os.path.join(script_folder, "circle_fitting_crown_visualization")
    process_and_fit_circles(input_folder_path_foliage_after_classification, output_folder_path_crown_width, output_folder_path_circle_fitting_crown_visualization)


    #########################################################################################################################################








if __name__ == "__main__":
    main()


