import os


# 将path路劲下的txt文本每行首个字符，如果是a就替换成b
def replace_a_as_b(path, a, b):
    """
    :param path:
    :param a:
    :param b:
    :return:
    """
    labels_files = os.listdir(path)
    for label_file in labels_files:
        if not label_file.endswith('.txt') and not label_file.endswith('.TXT'):
            continue
        if label_file == 'classes.txt':
            continue

        label_path = path + '/' + label_file
        print(label_path)
        with open(label_path, 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            print(lines[i])
            if lines[i][0] == a:
                lines[i] = lines[i].replace(lines[i][0], b, 1)

        with open(label_path, 'w') as file:
            file.writelines(lines)
