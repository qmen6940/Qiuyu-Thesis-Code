import os


def process_txt_files(input_folder, output_folder):
    # 确保输出文件夹存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中所有的txt文件
    txt_files = [file for file in os.listdir(input_folder) if file.endswith('.txt')]

    for file_name in txt_files:
        input_file_path = os.path.join(input_folder, file_name)
        output_file_path = os.path.join(output_folder, file_name)

        with open(input_file_path, 'r') as input_file:
            lines = input_file.readlines()

        with open(output_file_path, 'w') as output_file:
            for line in lines:
                try:
                    # 按空格分割行并转换为浮点数列表
                    row = list(map(float, line.strip().split()))

                    # 判断最后三个column的值并写入对应的column
                    if row[-3:] == [0.0, 255.0, 0.0]:
                        output_file.write(f"{line.strip()} 0\n")
                    elif row[-3:] == [0.0, 255.0, 255.0]:
                        output_file.write(f"{line.strip()} 1\n")
                    elif row[-3:] == [255.0, 0.0, 0.0]:
                        output_file.write(f"{line.strip()} 2\n")
                    elif row[-3:] == [0.0, 0.0, 255.0]:
                        output_file.write(f"{line.strip()} 3\n")
                    else:
                        output_file.write(f"{line.strip()} -1\n")
                except ValueError:
                    # 如果转换出错，直接写入原始行
                    output_file.write(line.strip() + " -1\n")  # 在行末尾添加新值（-1）


# 指定输入文件夹路径和输出文件夹路径
input_folder = r'D:\DESKTOP\Thesiscode\after_in_pieces'
output_folder = r'D:\DESKTOP\Thesiscode\classed'

# 处理txt文件
process_txt_files(input_folder, output_folder)
