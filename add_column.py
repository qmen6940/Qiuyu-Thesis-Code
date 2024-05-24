def add_columns_to_txt(input_file):
    with open(input_file, 'r+') as f:
        lines = f.readlines()
        f.seek(0)  # 将文件指针移到文件开头
        for line in lines:
            # 去除行末尾的换行符，并添加四个0作为新的列
            new_line = line.strip() + ' 0 0 0 0\n'
            f.write(new_line)
        f.truncate()  # 截断文件，删除多余的内容

# 指定输入文件的路径
input_file_path = r'D:\DESKTOP\Thesiscode\notclass_xyz.txt'

# 向每一行添加四个0并直接写入原始文件中
add_columns_to_txt(input_file_path)

