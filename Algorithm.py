# nnh算法实现
import copy
import math

Consider_the_time_window = False


def nnh(data):
    result_dict = {  # 用于存储运算结果的字典
        'NAME': data['NAME'],  # 文件名
        'All_Distance': 0,  # 总距离
        'All_Time': 0,  # 总时间
        'Routes': [],  # 路径
        'Nodes_no_go': []}  # 不去的节点

    number = data['NUMBER']  # 传递车辆数
    num = 1
    capacity = data['CAPACITY']  # 传递车辆容量
    nodes = list(data['NODES'])  # 传递节点

    route = []  # 定义单辆车的路径

    nodes_togo = nodes.copy()  # 等待去的节点
    last_node = {}  # 用于存储上一个节点

    time_temp = 0
    capacity_temp = 0
    distance = 0

    while nodes_togo:
        limit = False
        node_temp = []
        for node in nodes_togo:  # 根据约束寻找符合约束的节点
            if Consider_the_time_window:
                if (node['READY_TIME'] <= time_temp <= node['DUE_TIME'] - node['SERVICE_TIME']
                        and capacity_temp + node['DEMAND'] <= capacity):
                    node_temp.append(node)
            else:
                if capacity_temp + node['DEMAND'] <= capacity:
                    node_temp.append(node)

        if not node_temp:  # 找不到节点
            for node in nodes_togo:  # 放宽约束寻找符合约束的节点
                if Consider_the_time_window:
                    if (time_temp <= node['DUE_TIME'] - node['SERVICE_TIME']
                            and capacity_temp + node['DEMAND'] <= capacity):
                        node_temp.append(node)
                        limit = True
                else:
                    if capacity_temp + node['DEMAND'] <= capacity:
                        node_temp.append(node)

        if not node_temp:  # 实在找不到节点，换下一辆车
            result_dict['Routes'].append({'num': num, 'Route': route, 'Distance': math.sqrt(distance)})
            result_dict['All_Distance'] += math.sqrt(distance)
            result_dict['All_Time'] += time_temp

            if num < number:
                num += 1
                route = []
                last_node = {}
                time_temp = 0
                capacity_temp = 0
                continue
            else:  # 车不够，停止运算
                result_dict['Nodes_no_go'] = copy.copy(nodes_togo)
                nodes_togo.clear()
                break

        if not last_node:  # 寻找第一个节点
            nearest_node = min(node_temp, key=lambda x: x['X_COORD'] ** 2 + x['Y_COORD'] ** 2)
            distance += nearest_node['X_COORD'] ** 2 + nearest_node['Y_COORD'] ** 2
        else:  # 寻找下一个节点
            nearest_node = min(node_temp, key=lambda x: (x['X_COORD'] - last_node['X_COORD']) ** 2
                                                        + (x['Y_COORD'] - last_node['Y_COORD']) ** 2)
            distance += ((nearest_node['X_COORD'] - last_node['X_COORD']) ** 2
                         + (nearest_node['Y_COORD'] - last_node['Y_COORD']) ** 2)

        nodes_togo.remove(nearest_node)
        route.append(nearest_node)
        last_node = nearest_node
        if limit:
            time_temp = nearest_node['READY_TIME'] + nearest_node['SERVICE_TIME']
        time_temp += nearest_node['SERVICE_TIME']
        capacity_temp += nearest_node['DEMAND']

    return copy.deepcopy(result_dict)
