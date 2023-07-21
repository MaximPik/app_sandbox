############################### Libraries ######################################
import pathlib #библиотека для работы с файлами
import os #os.path - библиотека для работы с путями
import sys
#читает из файла по строке. Создаёт массив прочитанных строк
import pyperclip
import lib_common
import gui_sandbox
############################### Functions ######################################
def file_read_lines(filePath):
    encodingFile = 'windows-1251'
    strBuf = ""
    if(os.path.exists(filePath) == True): #существует ли файл по этому пути
        strArr = []
        # try:
        #     fo = open(filePath, "r+", encoding=encodingFile)
        #     fo.read()
        # except IOError:
        #     gui_sandbox.messagebox.showerror('Ошибка', f'Открыт файл {filePath}')
        #     return
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
    csvRecordList = lib_common.data_arr_creating(csvStrList)
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