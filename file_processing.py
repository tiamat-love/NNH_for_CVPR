import os
import re
import json
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt

from Algorithm import nnh


def process_file(file_path):
    with open(file_path, 'r') as file:
        data_dict = {}  # 用于存储提取的数据的字典
        index = 0  # 记录已读取行数
        data_dict['NAME'] = file.readline()  # 提取第一行显示的测试集名
        index += 1

        data_dict['NUMBER'] = 0  # 最大可用车辆数
        data_dict['CAPACITY'] = 0  # 车辆最大容积
        data_dict['NODES'] = []  # 用户集

        for line in file:
            index += 1  # 记录已读取行数
            numbers = list(re.findall(r'\d+', line))  # 使用正则表达式提取每一行中的所有数字
            numbers = [int(num) for num in numbers]
            if index == 5:
                data_dict['NUMBER'] = numbers[0]
                data_dict['CAPACITY'] = numbers[1]
            if index > 9:
                node_data = {
                    'NO': numbers[0],  # 用户序号
                    'X_COORD': numbers[1],  # 节点X坐标
                    'Y_COORD': numbers[2],  # 节点Y坐标
                    'DEMAND': numbers[3],  # 用户需求量
                    'READY_TIME': numbers[4],  # 时间窗开始
                    'DUE_TIME': numbers[5],  # 时间窗结束
                    'SERVICE_TIME': numbers[6]  # 服务时间
                }
                data_dict['NODES'].append(node_data)
    return data_dict


def jpg(data, output_file_path):
    # 创建一个新的图形
    plt.figure(figsize=(10, 10))

    # 循环处理每个路线
    for route in data["Routes"]:
        x_coords = [point["X_COORD"] for point in route["Route"]]
        y_coords = [point["Y_COORD"] for point in route["Route"]]

        # 添加连接点之间的连线
        plt.plot(x_coords, y_coords, marker='o')

        # 添加点的标签
        for i, txt in enumerate(route["Route"]):
            plt.annotate(txt["NO"], (x_coords[i], y_coords[i]))

    # 设置图形标题和标签
    plt.title(data["NAME"])

    # 保存图形为JPG文件
    plt.savefig(output_file_path + '.jpg')
    plt.close()


def process_txt_file(input_file_path, output_file_path):  # 处理单个txt文件
    data = process_file(input_file_path)

    result = nnh(data)
    jpg(result, output_file_path)
    with open(output_file_path, 'w') as output_file:
        json.dump(result, output_file, indent=2)


def process_txt_files(input_folder, output_folder):
    max_workers = 19  # 限制并发任务的数量
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 遍历输入文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if file.endswith('.txt'):
                    input_file_path = os.path.join(root, file)

                    # 获取相对路径，用于创建相应的文件夹结构在输出目录中
                    relative_path = os.path.relpath(input_file_path, input_folder)
                    output_file_path = os.path.join(output_folder, os.path.splitext(relative_path)[0] + '.json')

                    # 创建相应的文件夹结构
                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                    # 使用线程池处理每个文件
                    executor.submit(process_txt_file, input_file_path, output_file_path)
