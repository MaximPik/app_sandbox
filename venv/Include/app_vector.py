############################### Libraries ######################################
import matplotlib.pyplot as plt
import numpy as np
from app_surface_gen import *
from lib_common import *

############################### Functions ######################################

def vector_creating(avgPointsArr, axisX, axisY, pointsArr, nameAxisX):
    arrX = []
    arrY = []
    pointsX = []
    pointsZ = []
    for row in range(0, len(pointsArr)):
        pointsX.append(float(pointsArr[row].X))
        pointsZ.append(float(pointsArr[row].Z))
    #созданим отдельно массивы координат
    for iter in range(0, len(avgPointsArr[0])):
        arrX.append(float(avgPointsArr[0][iter].X))
        arrY.append(float(avgPointsArr[0][iter].Z))
    arrX = np.array(arrX)
    arrY = np.array(arrY)
    plt.grid()  # Добавляем сетку
    plt.xlabel(nameAxisX)
    plt.ylabel('Y')
    plt.xlim(axisX.minValue, axisX.maxValue)  # Максимальное и минимальное значение оси x
    plt.ylim(axisY.minValue, axisY.maxValue)  # Максимальное и минимальное значение оси y
    #plt.scatter(arrX, arrY, s = 1, color='red')  # Строим точки
    plt.scatter(pointsX, pointsZ, s=1, color='red')
    plt.plot(arrX, arrY, color='blue')  # Строим вектор
    plt.show()
# группируем точки по ячейкам
def points_sort_vector(axisX, pointsArr):
    # создаём пустой трёхмерный массив
    sortedPointsArr = [[[0 for kter in range(1)] for jter in range(axisX.numCells)] for iter in range(1)]
    cellsWidth = (axisX.maxValue - axisX.minValue) / axisX.numCells  # ширина ячейки
    for point in pointsArr:
        cellIndexX = int((float(point.X) - axisX.minValue) / cellsWidth) + 1  # строка ячейки
        if 0 <= cellIndexX <= axisX.numCells:  # проверка выход за диапазон
            sortedPointsArr[0][cellIndexX - 1].append(point)
    return sortedPointsArr

# поиск среднего значение группированных точек каждой ячейки
def avg_sorted_points_vector(axisX, sortedPointsArr):
    cellsWidth = (axisX.maxValue - axisX.minValue) / axisX.numCells  # ширина ячейки
    avgPointsArr = [[0 for jter in range(len(sortedPointsArr[0]))] for iter in range(len(sortedPointsArr))]
    for row in range(0, len(sortedPointsArr)):
        for col in range(0, len(sortedPointsArr[row])):
            summX = 0
            summZ = 0
            if len(sortedPointsArr[row][col]) > 1:  # Если есть точка
                for point in sortedPointsArr[row][col]:
                    if point != 0:
                        summX = summX + float(point.X)
                        summZ = summZ + float(point.Z)
                avgX = summX / (len(sortedPointsArr[row][col]) - 1)
                avgZ = summZ / (len(sortedPointsArr[row][col]) - 1)
                avgPointsArr[row][col] = Point(avgX, 0, avgZ)
    return avgPointsArr