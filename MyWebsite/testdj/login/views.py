from django.shortcuts import render, HttpResponse
import pandas as pd
import numpy as np
from math import *
from login import models
"""import sys
sys.path.append(r'E:\PycharmProjects\MyWebsite\testdj\login')
import models"""

# Create your views here.
user_list = []

num = 10

# 读取数据
tutors = pd.read_csv(r"E:\PycharmProjects\MyWebsite\testdj\login\ltutor.csv")
tutors1 = np.array(tutors)
frequency = pd.read_csv(r"E:\PycharmProjects\MyWebsite\testdj\login\lfrequency.csv")
data = pd.merge(tutors, frequency, on='tutorID')
data[['userID', 'frequency', 'tutorID', 'name']].sort_values('userID').to_csv(r'E:\PycharmProjects\MyWebsite\testdj\login\data.csv', index=False)
file = open(r"E:\PycharmProjects\MyWebsite\testdj\login\data.csv", 'r', encoding='UTF-8')
data = {}  # 存放每位用户搜索的导师和次数
# 读取data.csv中每行中除了名字的数据
for line in file.readlines()[1:]:
    line = line.strip().split(',')
    # 如果字典中没有某位用户，则使用用户ID来创建这位用户
    if not line[0] in data.keys():
        data[line[0]] = {line[3]: line[1]}
    # 否则直接添加以该用户ID为key字典中
    else:
        data[line[0]][line[3]] = line[1]


def get_area(tname):
    for tutor in tutors1:
        if tname == tutor[1]:
            return tutor[2]


def Euclidean(user1, user2):
    # 取出两位用户搜索过的导师和次数
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0

    # 找到两位用户都搜索过的导师，并计算欧式距离
    for key in user1_data.keys():
        if key in user2_data.keys():
            # 注意，distance越大表示两者越相似
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

    return 1 / (1 + sqrt(distance))  # 这里返回值越小，相似度越大


# 计算某个用户与其他用户的相似度
def top10_simliar(userID):
    res = []
    for userid in data.keys():
        # 排除与自己计算相似度
        if not userid == userID:
            simliar = Euclidean(userID, userid)
            res.append((userid, simliar))
    res.sort(key=lambda val: val[1])
    return res[:4]
    # 用户之间相似度结果：0表示两位的搜索次数几乎一样，1表示没有共同的搜索


def recommend(user):
    # 相似度最高的用户
    top_sim_user = top10_simliar(user)[0][0]
    # 相似度最高的用户的搜索记录
    items = data[top_sim_user]
    recommendations = []
    # 筛选出该用户未搜索的导师并添加到列表中
    for item in items.keys():
        if item not in data[user].keys():
            recommendations.append((item, items[item]))
    recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照频率排序
    # 返回频率最高的5位导师
    return recommendations[:5]


def index(request):
    tutor_list = []
    if request.method == 'POST':
        userID = num+1
        tname = request.POST.get('tutorname')
        tname = tname.split(sep='，')
        for name in tname:
            if not userID in data.keys():
                data[userID] = {name: 1}
            else:
                data[userID][name] = 1
        Recommendations = recommend(userID)
        area = request.POST.get('area')
        for Recommendation in Recommendations:
            if area == get_area(Recommendation[0]):
                tutor_list.append(Recommendation[0])
        # 数据保存到数据库
        # models.UserInfo.objects.create(userID=userID, tname=tname, area=area)

    # 数据库读取数据
    # user_list = models.UserInfo.objects.all()
    print(tutor_list)
    return render(request, 'index.html', {'data': tutor_list})



