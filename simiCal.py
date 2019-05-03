import numpy as np
from math import sqrt
import readFile
import datetime


def pearson_similarity(user_a, user_b):
    '''
    user_a和user_b都是字典类型，字典的key为itemID，value为该uer对该item的打分
    两个user的相似度用pearson相关系数来表示
    '''
    # 首先寻找两个user都打了分的item
    common_item = list()
    for item in user_a.keys():
        if item in user_b:
            common_item.append(item)
    # 计算a,b两个用户的平均打分
    average_a_rating = 0
    for each_rating in user_a.values():
        average_a_rating += each_rating
    average_a_rating = average_a_rating/len(user_a.values())
    average_b_rating = 0
    for each_rating in user_b.values():
        average_b_rating += each_rating
    average_b_rating = average_b_rating/len(user_b.values())
    # 计算两个用户的pearson相关系数
    pearson_simi = 0
    for each_item in common_item:
        r_a = user_a[each_item]
        r_b = user_b[each_item]
        diff_a = r_a - average_a_rating
        diff_b = r_b - average_b_rating
        pearson_simi += diff_a * diff_b
    deno_a = 0
    deno_b = 0
    for rating in user_a.values():
        deno_a += (rating - average_a_rating)*(rating - average_a_rating)
    for rating in user_b.values():
        deno_b += (rating - average_b_rating)*(rating - average_b_rating)
    deno_a = sqrt(deno_a)
    deno_b = sqrt(deno_b)
    deno = deno_a*deno_b
    if 0 == deno and 0 == pearson_simi:
        pearson_simi = 0
    else:
        pearson_simi = pearson_simi/deno
    return pearson_simi


def pearson_similarity_numpy(user_a, user_b):
    '''
    使用numpy来计算pearson相关系数
    和普通版本相比或快或慢，主要看稀疏程度
    '''
    # 首先寻找两个user都打了分的item
    common_item = list()
    for item in user_a.keys():
        if item in user_b:
            common_item.append(item)
    r_a_vector = [value for value in user_a.values()]
    r_b_vector = [value for value in user_b.values()]
    r_a_c_vector = [user_a[item] for item in common_item]
    r_b_c_vector = [user_b[item] for item in common_item]
    r_a_vector = np.array(r_a_vector)  # 用户a的打分向量
    r_b_vector = np.array(r_b_vector)  # 用户b的打分向量
    r_a_c_vector = np.array(r_a_c_vector)  # 用户a对a，b共有项的打分向量
    r_b_c_vector = np.array(r_b_c_vector)  # 用户b对a，b共有项的打分向量
    r_a_mean = np.mean(r_a_vector)
    r_b_mean = np.mean(r_b_vector)
    r_a_mean_vector = np.array([r_a_mean for _ in range(len(r_a_vector))])
    r_b_mean_vector = np.array([r_b_mean for _ in range(len(r_b_vector))])
    r_a_vector = np.subtract(r_a_vector, r_a_mean_vector)
    r_b_vector = np.subtract(r_b_vector, r_b_mean_vector)
    r_a_c_mean_vector = np.array([r_a_mean for _ in range(len(r_a_c_vector))])
    r_b_c_mean_vector = np.array([r_b_mean for _ in range(len(r_b_c_vector))])
    r_a_c_vector = np.subtract(r_a_c_vector, r_a_c_mean_vector)
    r_b_c_vector = np. subtract(r_b_c_vector, r_b_c_mean_vector)
    deno = np.linalg.norm(r_a_vector)*np.linalg.norm(r_b_vector)
    nume = np.matmul(r_b_c_vector, r_a_c_vector.T)
    if deno == 0:
        pearson_simi = 0
    else:
        pearson_simi = nume/deno
    return pearson_simi


def consine_similarity(list_a, list_b):
    # 计算余弦相似度
    if list_a == None or list_b == None:
        print("list 为空")
        return 0
    vector_a = np.array(list_a)
    vector_b = np.array(list_b)
    num = np.matmul(vector_a, vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    cos = num / denom
    return cos


def compare():
    a = {1:4, 4:5, 5:1}
    b = {1:5, 2:5, 3:4}
    c = {4:2, 5:4, 6:5}
    print(pearson_similarity(a,b))
    print(pearson_similarity(a,c))
    print(pearson_similarity_numpy(a, b))
    print(pearson_similarity_numpy(a, c))

def write_simi():
    '''
    本来打算将计算好的相似度直接写入文件中
    再次使用时可以直接读取
    但是写出来的文件太大了
    '''
    user_item_rating = readFile.read_train("train.txt")
    file = open("similarity.txt", 'a')
    users = [user for user in user_item_rating.keys()]
    n_users = len(users)
    # 用户i和用户j的相似度
    for i in range(n_users):
        print("计算到" + str(i))
        user_simi = {}
        user_i = user_item_rating[users[i]]
        for j in range(i+1, n_users):
            user_j = user_item_rating[users[j]]
            simi = pearson_similarity_numpy(user_i, user_j)
            index = (users[i], users[j])
            user_simi[index] = simi
        for each_index in user_simi:
            line = str(each_index[0]) + ':' + str(each_index[1]) + ':' + str(round(user_simi[each_index],4)) + '\n'
            file.write(line)
        print("写入完成")
    print("全部完成")



if __name__ == '__main__':
    compare()


