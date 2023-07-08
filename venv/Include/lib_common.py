############################### Libraries ######################################
import re
import pathlib #библиотека для работы с файлами
import os #os.path - библиотека для работы с путями
import sys
import matplotlib.pyplot as plt #библиотека для графика
import numpy as np #библиотека для аппроксимации

############################### Functions ######################################

#читает из файла по строке. Создаёт массив прочитанных строк
import pyperclip


def file_read_lines(filePath):
    encodingFile = 'windows-1251'
    strBuf = ""
    if(os.path.exists(filePath) == True): #существует ли файл по этому пути
        strArr = []
        fo = open(filePath, "r+", encoding=encodingFile)
        lineStr = " "
        strArr.append(lineStr)
        while lineStr:
            lineStr = fo.readline()
            strArr.append(lineStr)
        strArr = strArr[1:len(strArr)]
    else:
        print("ERROR: filePath=" + filePath + " is invalid!")
        sys.exit()
    return strArr

# преобразовываем файл в двумерный массив (преобразуем строку в массив данных)
# заменяем запятые на точки
def data_arr_creating(strArr):
    dataArr = []
    for iter in range(1, len(strArr)):
        dataArr.append(strArr[iter].split(";"))
        for jter in range(0, len(dataArr[iter - 1])):
            dataArr[iter - 1][jter] = dataArr[iter - 1][jter].replace(",", ".")
    return dataArr

#проверка существования регулярного выражения
def regex_search(inputStr, pattern):
    foundObj = re.search(r'' + pattern, inputStr, re.MULTILINE | re.I)
    return foundObj

#заменяет нужные символы в строке
# def regex_replace_line(inputStr, pattern, replaceStr, replaceCnt):
#     if(replaceCnt > 0):
#         resultStr = re.sub(pattern, replaceStr, inputStr, replaceCnt)
#     else:
#         resultStr = re.sub(pattern, replaceStr, inputStr)
#     return resultStr

# замена символа в двумерном массиве. Заменяем символ 1 на символ 2
# Преобразование массива float в str
def replace_symbols(dataArr, s_1, s_2):
    dataArrStr = [[]]
    for iter in range(0, len(dataArr)):
        for jter in range(0, len(dataArr[iter])):
            if dataArr[iter][jter]:
                dataArr[iter][jter] = str(dataArr[iter][jter]).replace(s_1, s_2)
    dataArrStr = dataArr
    return dataArrStr

#записываем буффер в файл
def file_write_buf(filePath, strBuf):
    encodingFile = 'windows-1251'
    outDir = os.path.split(filePath)[0]
    pathlib.Path(outDir).mkdir(parents=True, exist_ok=True)
    fo = open(filePath, "w+", encoding=encodingFile)
    fo.write(strBuf)
    fo.close()
    return

#преобразование списка в строку, которую можно записать в файл
def process_list_to_csvFormat(csvRecordList):
    listBuf = []
    strBuf = ""
    for csvRecord in csvRecordList:
        if (csvRecord != None):
            for iter in range(0, len(csvRecord)):
                if (iter == len(csvRecord) - 1) and (str(csvRecord[iter][-1]) != '\n'):
                    strBuf += str(csvRecord[iter]) + "\n"
                else:
                    if str(csvRecord[iter][-1]) != '\n':
                        strBuf += str(csvRecord[iter]) + ";"
                    else:
                        strBuf += str(csvRecord[iter])
            listBuf.append(strBuf)
            strBuf = ""
    return listBuf

#генерируем список в csv файл и записываем
def generate_csv_file(csvRecordList):
    strBuf = ""
    for csvRecord in csvRecordList:
        if(csvRecord != None):
                strBuf += str(csvRecord)
    # file_write_buf(filePathOut, strBuf)
    return strBuf

#преобразовываем файл в список, с которым будет выполняться дальнейшая работа
def process_csv_file(file):
    csvRecordList = []
    csvStrList = file_read_lines(file)
    csvRecordList = data_arr_creating(csvStrList)
    return csvRecordList

#генерируем список в массив для копирования в буфер обмена
def generate_csv_buf(csvRecordList):
    arrBuf = []
    strBuf = ""
    #Получаю массив вида ["A","B","C\n",...]
    for iter in range(0, len(csvRecordList)):
        strArr = csvRecordList[iter].split(";")
        for jter in range(0, len(strArr)):
            arrBuf.append(strArr[jter])
    for csvRecord in arrBuf:
        if (csvRecord != None):
            if csvRecord[-1] != '\n':
                strBuf += str(csvRecord)+'\t'
            else:
                strBuf += str(csvRecord)
    #Обрезаем строку, исключая 2 последних символа (\n)
    strBuf = strBuf[:-2]
    return strBuf