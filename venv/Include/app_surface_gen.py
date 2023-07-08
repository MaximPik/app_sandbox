# -*- coding: windows-1251 -*-

############################### Classes ######################################
class Axis:
    def __init__(self, minValue, maxValue, numCells):
        self.minValue = minValue
        self.maxValue = maxValue
        self.numCells = numCells


class Point:
    def __init__(self, X, Y, Z):
        self.X = X
        self.Y = Y
        self.Z = Z

############################### Libraries ######################################
import math
import pathlib  # ���������� ��� ������ � �������
import os  # os.path - ���������� ��� ������ � ������
import sys
from tkinter import *  # ����������� ���������
# ��� 3� �����������
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.interpolate import griddata
import re
from matplotlib.ticker import FuncFormatter

############################### Functions ######################################

def columnZ_creating(dataArr, formula, headings):
    columnZ=[]
    currFormula = re.sub(r"['^']", '**', formula)
    formulaWithValue = formula
    parts = re.split(r'[+\-*/()]', currFormula) # ��������� ������� �� ��������� ��������
    # ����� ���������� � ������ �� �� �������� �� �������
    #for iter in range(0, len(dataArr)-1):
    for row in dataArr:
        if len(row)>1:
            counter = 0
            currFormula = formula
            for name in headings:
                counter += 1
                for jter in range(0, len(parts)):
                    if name == parts[jter]:
                        formulaWithValue = re.sub(name, str(row[counter - 1]), currFormula)
                        currFormula = formulaWithValue
            formulaWithValue = re.sub(r"['^']", '**', formulaWithValue)
            columnZ.append(eval(formulaWithValue, {"__builtins__": None}, {"sqrt": math.sqrt}))
    return columnZ

# ������ ������ �����
def points_arr_creating(dataArr, columnX, columnY, arrZ):
    pointsArr = []
    counter = 0
    for row in dataArr:
        counter += 1
        if columnY != None:
            if len(row) >= 2 and row[columnX] and row[columnY]:  # �������� �� ������� ��������
                point = Point(row[columnX], row[columnY], arrZ[counter-1])
                pointsArr.append(point)
            else:
                counter -= 1
        else:
            if len(row) >= 2 and row[columnX]:  # �������� �� ������� ��������
                point = Point(row[columnX], 0, arrZ[counter - 1])
                pointsArr.append(point)
            else:
                counter -= 1
    return pointsArr


# ���������� ����� �� �������
def points_sort(axisX, axisY, pointsArr):
    # ������ ������ ��������� ������
    sortedPointsArr = [[[0 for kter in range(1)] for jter in range(axisX.numCells)] for iter in range(axisY.numCells)]
    cellsWidth = (axisX.maxValue - axisX.minValue) / axisX.numCells  # ������ ������
    cellsHeight = (axisY.maxValue - axisY.minValue) / axisY.numCells  # ������ ������
    for point in pointsArr:
        cellIndexX = int((float(point.X) - axisX.minValue) / cellsWidth) + 1  # ������ ������
        cellIndexY = int((float(point.Y) - axisY.minValue) / cellsHeight) + 1  # ������� ������
        if 0 <= cellIndexX <= axisX.numCells and 0 <= cellIndexY <= axisY.numCells:  # �������� ����� �� ��������
            sortedPointsArr[cellIndexX - 1][cellIndexY - 1].append(point)
    return sortedPointsArr


# ����� �������� �������� �������������� ����� ������ ������
def avg_sorted_points(axisX, axisY, sortedPointsArr):
    cellsWidth = (axisX.maxValue - axisX.minValue) / axisX.numCells  # ������ ������
    cellsHeight = (axisY.maxValue - axisY.minValue) / axisY.numCells  # ������ ������
    avgPointsArr = [[0 for jter in range(len(sortedPointsArr[1]))] for iter in range(len(sortedPointsArr))]
    for row in range(0, len(sortedPointsArr)):
        for col in range(0, len(sortedPointsArr[row])):
            summX = 0
            summY = 0
            summZ = 0
            if len(sortedPointsArr[row][col]) > 1:  # ���� ���� �����
                for point in sortedPointsArr[row][col]:
                    if point != 0:
                        summX = summX + float(point.X)
                        summY = summY + float(point.Y)
                        summZ = summZ + float(point.Z)
                avgX = summX / (len(sortedPointsArr[row][col]) - 1)
                avgY = summY / (len(sortedPointsArr[row][col]) - 1)
                avgZ = summZ / (len(sortedPointsArr[row][col]) - 1)
                avgPointsArr[row][col] = Point(avgX, avgY, avgZ)

    avgPointsArr = interpolate(avgPointsArr, axisX, axisY)
    return avgPointsArr


# �������������� ������������/������������� ������� ���� ����������
def interpolate(avgPointsArr, axisX, axisY):
    copyArr = np.array(avgPointsArr)  # ���������������
    cellsWidth = (axisX.maxValue - axisX.minValue) / axisX.numCells  # ������ ������
    cellsHeight = (axisY.maxValue - axisY.minValue) / axisY.numCells  # ������ ������
    arrX, arrY, arrZ = [], [], []
    for row in range(0, len(copyArr)):
        for col in range(0, len(copyArr)):
            if copyArr[row][col] != 0:
                arrX.append(copyArr[row][col].X)
                arrY.append(copyArr[row][col].Y)
                arrZ.append(copyArr[row][col].Z)
    arrX = np.array(arrX)
    arrY = np.array(arrY)
    arrZ = np.array(arrZ)

    # ���������� ������� ������� ���������
    A = np.column_stack([np.ones_like(arrX), arrX, arrY, arrX ** 2, arrY ** 2, arrX * arrY])

    # ������� ������� ���������
    coefficients, residuals, rank, singularVal = np.linalg.lstsq(A, arrZ, rcond=None)

    # ������������ ��������
    a, b, c, d, e, f = coefficients

    # �������������/������������
    for row in range(0, len(copyArr)):
        for col in range(0, len(copyArr)):
            if copyArr[row][col] == 0:
                avgX = ((row + 1) * cellsWidth - cellsWidth / 2 + axisX.minValue)
                avgY = ((col + 1) * cellsHeight - cellsHeight / 2 + axisY.minValue)
                avgZ = a + b * avgX + c * avgY + d * avgX ** 2 + e * avgY ** 2 + f * avgX * avgY
                copyArr[row][col] = Point(avgX, avgY, avgZ)
    copyArr = copyArr.tolist()
    return copyArr

    # -----------------------------------------------------------------
    #���������� ������������
    # copyArr = np.array(avgPointsArr) #���������������
    # pointsArr = [[]]
    # values = []
    # counter = 0
    # for row in range(0, len(copyArr)):
    #     for col in range(0, len(copyArr)):
    #         if copyArr[row][col] != 0:
    #             if counter != 0:
    #                 pointsArr.append([])
    #             pointsArr[counter].append(copyArr[row][col].X)
    #             pointsArr[counter].append(copyArr[row][col].Y)
    #             values.append(copyArr[row][col].Z)
    #             counter += 1
    # pointsArr = np.array(pointsArr)
    # values = np.array(values)
    # cellsWidth = (axisX.maxValue - axisX.minValue) / axisX.numCells  # ������ ������
    # cellsHeight = (axisY.maxValue - axisY.minValue) / axisY.numCells  # ������ ������
    # for row in range(0, len(copyArr)):
    #     for col in range(0, len(copyArr)):
    #         if copyArr[row][col] == 0:
    #             avgX = ((row + 1) * cellsWidth - cellsWidth / 2 + axisX.minValue)
    #             avgY = ((col + 1) * cellsHeight - cellsHeight / 2 + axisY.minValue)
    #             avgZ = griddata(pointsArr, values, (avgX, avgY), method='splinef2d')
    #             copyArr[row][col] = Point(avgX, avgY, avgZ)
    # return copyArr
    # -----------------------------------------------------------------

# �������������� ������ � ������, ������� ����� �������� � ����
def process_list_to_csvFormat_surface(avgPointsArr):
    listBuf = []
    strBuf = ""
    for csvRecord in avgPointsArr:
        if (csvRecord != None):
            for iter in range(0, len(csvRecord)):
                if (iter == len(csvRecord) - 1):
                    if csvRecord[iter] != 0:
                        strBuf += str(csvRecord[iter].Z) + "\n"
                    else:
                        strBuf += str(csvRecord[iter]) + "\n"
                else:
                    if csvRecord[iter] != 0:
                        strBuf += str(csvRecord[iter].Z) + ";"
                    else:
                        strBuf += str(csvRecord[iter]) + ";"
            listBuf.append(strBuf)
            strBuf = ""
    return listBuf

# ������ ������� � ��������� �������. �������� ������ 1 �� ������ 2
# �������������� ������� float � str
def replace_symbols_surface(dataArr, s_1, s_2):
    dataArrStr = [[]]
    for iter in range(0, len(dataArr)):
        for jter in range(0, len(dataArr[iter])):
            if dataArr[iter][jter] != 0:
                dataArr[iter][jter].Z = str(dataArr[iter][jter].Z).replace(s_1, s_2)
    dataArrStr = dataArr
    return dataArrStr


# ���������� 3� �����������
def surface(avgPointsTab, pointsArr):
    # ����������� ��������� ������ ������� ����� � 2 ���������� ������� ��������� � � Y
    arrX = [[0 for jter in range(len(avgPointsTab[1]))] for iter in range(len(avgPointsTab))]
    arrY = [[0 for jter in range(len(avgPointsTab[1]))] for iter in range(len(avgPointsTab))]
    arrZ = [[0 for jter in range(len(avgPointsTab[1]))] for iter in range(len(avgPointsTab))]
    pointsX = []
    pointsY = []
    pointsZ = []
    for row in range(0, len(avgPointsTab)):
        for col in range(0, len(avgPointsTab[row])):
            if avgPointsTab[row][col] != 0:
                arrX[row][col] = avgPointsTab[row][col].X
                arrY[row][col] = avgPointsTab[row][col].Y
                arrZ[row][col] = avgPointsTab[row][col].Z
    for row in range(0, len(pointsArr)):
        pointsX.append(float(pointsArr[row].X))
        pointsY.append(float(pointsArr[row].Y))
        pointsZ.append(float(pointsArr[row].Z))

    arrZ = np.array(arrZ)
    # ������ 3� ������
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # ������ ��������� �����������
    # ax.plot_wireframe(arrX, arrY, arrZ, cmap='viridis')
    ax.plot_surface(arrX, arrY, arrZ, color='blue')
    # ������� ��������� �����
    ax.scatter(pointsX, pointsY, pointsZ, s=0.5, color='red')

    # ����������� ����
    maxValX = max(pointsArr, key=lambda point: float(point.X)).X  # ������������ � �� ������� �����
    maxValY = max(pointsArr, key=lambda point: float(point.Y)).Y  # ������������ Y �� ������� �����
    minValX = min(pointsArr, key=lambda point: float(point.X)).X  # ����������� � �� ������� �����
    minValY = min(pointsArr, key=lambda point: float(point.Y)).Y  # ����������� Y �� ������� �����
    maxValZ = max(pointsArr, key=lambda point: float(point.Z)).Z  # ������������ Z �� ������� �����
    minValZ = min(pointsArr, key=lambda point: float(point.Z)).Z  # ����������� Z �� ������� �����
    ax.set_xlim(float(minValX), float(maxValX))
    ax.set_ylim(float(minValY), float(maxValY))
    ax.set_zlim(float(minValZ), float(maxValZ))
    # �������� ����
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    #ax.xaxis.set_major_formatter(FuncFormatter(format_func))
    #ax.yaxis.set_major_formatter(FuncFormatter(format_func))
    ax.zaxis.set_major_formatter(FuncFormatter(format_func))
    plt.show()

def format_func(value, tick_number):
    if value >= 100000:
        return '{:,.0f}'.format(value)  # ����������� ������ �������� � �������������
    else:
        return '{:.2f}'.format(value)  # ����������� �������� � ����� ������� ����� �������