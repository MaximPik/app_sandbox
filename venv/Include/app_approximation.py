# -*- coding: windows-1251 -*-

############################### Constants ######################################
LEGEND_INIT_FUNC = '�������� �������'
LEGEND_APPROX_FUNC = '���������������� �������'
RED = 'r'
BLUE = 'b'

############################### Libraries ######################################
import re
import pathlib #���������� ��� ������ � �������
import os #os.path - ���������� ��� ������ � ������
import sys
import matplotlib.pyplot as plt #���������� ��� �������
import numpy as np #���������� ��� �������������

############################### Functions ######################################

#������������ csv ������ �� ���: ������ ������, ���� ���������� ������ ������ ������,
#������� ����� �������������� ��� �������������
def process_list(csvRecordList, referenceCol, diff):
    newRecordList=[]
    for iter in range (0, len(csvRecordList) - 1):
        if (len(csvRecordList[iter + 1])) > 1:
            if ((float(csvRecordList[iter][referenceCol]) - float(csvRecordList[iter + 1][referenceCol])) > float(diff)):
                newRecordList.append(csvRecordList[iter])
    return newRecordList

#������� �������������
def approx_func(dataArr, approxDegree, referenceCol_1, referenceCol_2, nameAxisX, nameAxisY):
    if ((len(dataArr) < approxDegree) | (approxDegree < 1)):
        print("ERROR: There can't be such a degree!")
        sys.exit()
    x = []
    y = []
    for iter in range(0, len(dataArr)):
        if len(dataArr[iter]) > 1:
            x.append(float(dataArr[iter][referenceCol_1]) - float(dataArr[0][referenceCol_1]))
            y.append(float(dataArr[iter][referenceCol_2]) / float(dataArr[0][referenceCol_2]))
    coeffPoly = np.polyfit(x, y, approxDegree) #��������� ������ �������������
    # print(coeffPoly)
    func = np.poly1d(coeffPoly) #������������ �������
    build_graph(x, y, func, coeffPoly, nameAxisX, nameAxisY)
    formula = coeff_to_str(coeffPoly)
    plt.show()
    return formula

#���������� �������
def build_graph(x, y, func, title, nameAxisX, nameAxisY):
    graph_setting(coeff_to_str(title), nameAxisX, nameAxisY)
    plt.plot(x, y, marker='.', label=LEGEND_INIT_FUNC, c=BLUE)
    plt.plot(x, func(x), label=LEGEND_APPROX_FUNC, c=RED)
    plt.legend()
    #plt.savefig('Graph.jpeg')
    return

#������������� ������ ������������� � ���������
def coeff_to_str(coeffPoly):
    outStr = ''
    for i in range(0, len(coeffPoly)):
        if (i != (len(coeffPoly) - 1)):
            if (coeffPoly[i + 1] > 0):
                outStr = outStr + str(rounding(coeffPoly[i])) + 'x^'+str(len(coeffPoly) - 1 - i) + '+'
            else:
                outStr = outStr + str(rounding(coeffPoly[i])) + 'x^' + str(len(coeffPoly) - 1 - i)
        else:
            outStr = outStr + str(rounding(coeffPoly[i]))
    return outStr

#��������� �������
def graph_setting(title, nameAxisX, nameAxisY):
    plt.title(title)
    plt.xlabel(nameAxisX)
    plt.ylabel(nameAxisY)
    plt.grid()
    return

# ������� ���������� �� �����. ���� ������������ ����� ����
def rounding(number):
    i = 3 #���-�� ������ ����� �������
    while (abs(round(number, i)) == 0):
        i += 1
    return round(number, i)