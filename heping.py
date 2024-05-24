import os

def merge_txt_files(input_directory, output_file):
    with open(output_file, 'w') as outfile:
        for root, dirs, files in os.walk(input_directory):
            for filename in files:
                if filename.endswith('.txt'):
                    filepath = os.path.join(root, filename)
                    with open(filepath, 'r') as infile:
                        for line in infile:
                            outfile.write(line)

# 示例用法
input_directory = r'D:\DESKTOP\Thesiscode\after_in_pieces'  # 输入文件夹路径
output_file = r'D:\DESKTOP\Thesiscode\heping.txt'  # 输出文件路径

merge_txt_files(input_directory, output_file)
