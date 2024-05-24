import os

def crown_height(input_folder, output_folder):
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

    # 遍历文件夹中的所有txt文件
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            input_file_path = os.path.join(input_folder, file_name)
            output_file_path = os.path.join(output_folder, f"height_{file_name}")

            z_values = []
            with open(input_file_path, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) >= 3:  # 确保行有足够的数据
                        z_values.append(float(parts[2]))  # 假设Z值是第三列

            if z_values:
                z_max = max(z_values)
                z_min = min(z_values)
                height_difference = z_max - z_min
                print(f'File: {file_name}, Crown Height: {height_difference}')

                with open(output_file_path, 'w') as output_file:
                    # output_file.write(f'crown height: {height_difference}\n')
                    output_file.write(f"{height_difference}\n")

# # 示例用法
# input_folder = 'D:\\DESKTOP\\Thesiscode\\foliage_after_classification'
# output_folder = 'D:\\DESKTOP\\Thesiscode\\crown_height'
# crown_height(input_folder, output_folder)
