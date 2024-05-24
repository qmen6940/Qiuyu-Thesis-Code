import os

def tree_height(input_folder, output_folder):
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
                    # 检查颜色值是否符合条件
                    if len(parts) >= 6 and (parts[-3:] == ['0', '255', '0'] or parts[-3:] == ['255', '0', '0']):
                        z_values.append(float(parts[2]))  # 假设Z值是第三列

            if z_values:
                z_max = max(z_values)
                z_min = min(z_values)
                height = z_max - z_min
                print(height)

                with open(output_file_path, 'w') as output_file:
                    # output_file.write(f'height: {height}\n')
                    output_file.write(f"{height}\n")

# 示例用法
# input_folder = 'D:\\DESKTOP\\Thesiscode\\seg_train_dataset'
# output_folder = 'D:\\DESKTOP\\Thesiscode\\tree height'
# tree_height(input_folder, output_folder)
