############################### Classes ######################################
class cfgData:
    def __init__(self):
        self.filePath = None
        self.statusCheckBox = None
        self.axisX = None
        self.axisY = None
        self.numCells = None
        self.step = None
        self.enteredFormula = None
        self.resultingFormula = None

############################### Libraries ######################################
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyperclip #копировать содержимое
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import app_surface_gen
import app_approximation
import app_vector
import re # работа с регулярными выражениями
import ast #Корректность формулы
import lib_common
import os #os.path - библиотека для работы с путями
import configparser # создание конфига
############################### Functions_Config ######################################
def get_gui_data(surfaceCfg, approximationCfg, vectorCfg):
    #Путь до файла
    surfaceCfg.filePath = pathSurface
    approximationCfg.filePath = pathApproximation
    vectorCfg.filePath = pathVector
    #Статус checkBox
    surfaceCfg.statusCheckBox = str(var.get())
    #ось Х
    surfaceCfg.axisX = xAxisComboboxSurface.get()
    approximationCfg.axisX = xAxisComboboxApproximation.get()
    vectorCfg.axisX = xAxisComboboxVector.get()
    #ось Y
    surfaceCfg.axisY = yAxisComboboxSurface.get()
    approximationCfg.axisY = yAxisComboboxApproximation.get()
    #количество ячеек
    surfaceCfg.numCells = numCellsEntrySurface.get()
    vectorCfg.numCells = numCellsEntryVector.get()
    # шаг
    approximationCfg.step = stepEntryApproximation.get()
    #Введённая формула
    surfaceCfg.enteredFormula = formulaEntrySurface.get()
    vectorCfg.enteredFormula = formulaEntryVector.get()
    #полученная формула
    approximationCfg.resultingFormula = formulaEntryVector.get()

def save_cfg(config, surfaceCfg, approximationCfg, vectorCfg):
    config['strData']['filePathSurface'] = surfaceCfg.filePath
    config['strData']['filePathApproximation'] = approximationCfg.filePath
    config['strData']['filePathVector'] = vectorCfg.filePath
    config['status']['statusCheckBox'] = surfaceCfg.statusCheckBox
    config['strData']['axisXSurface'] = surfaceCfg.axisX
    config['strData']['axisXApproximation'] = approximationCfg.axisX
    config['strData']['axisXVector'] = vectorCfg.axisX
    config['strData']['axisYSurface'] = surfaceCfg.axisY
    config['strData']['axisYApproximation'] = approximationCfg.axisY
    config['strData']['numCellsSurface'] = surfaceCfg.numCells
    config['strData']['numCellsVector'] = vectorCfg.numCells
    config['strData']['stepEntryApproximation'] = approximationCfg.step
    config['strData']['enteredFormulaSurface']=surfaceCfg.enteredFormula
    config['strData']['enteredFormulaVector'] = vectorCfg.enteredFormula
    config['strData']['resultingFormula']=approximationCfg.resultingFormula
    with open('config.cfg', 'w') as configfile:
        config.write(configfile)

def creating_cfg():
    surfaceCfg, approximationCfg, vectorCfg = cfgData(), cfgData(), cfgData()
    # создаём объект конфигурации
    config = configparser.ConfigParser()

    # Читаем файл конфигурации, если он существует
    config.read('config.cfg')

    # Проверка существования раздела
    if 'strData' not in config:
        # Если раздела нет - создать
        config['strData'] = {}
    # Проверка существования раздела
    if 'status' not in config:
        # Если раздела нет - создать
        config['status'] = {}

    get_gui_data(surfaceCfg, approximationCfg, vectorCfg)
    save_cfg(config, surfaceCfg, approximationCfg, vectorCfg)
    #Закрытие окна
    root.destroy()

def get_cfg_data():
    global pathSurface, pathApproximation, pathVector, var
    config = configparser.ConfigParser()
    # Читаем файл конфигурации, если он существует
    config.read('config.cfg')
    if 'strData' in config:
        pathSurface = config['strData'].get('filePathSurface')
        selectedFileLabelSurface.config(text='Последний выбранный файл: ' + pathSurface)
        pathApproximation = config['strData'].get('filePathApproximation')
        selectedFileLabelApproximation.config(text='Последний выбранный файл: ' + pathApproximation)
        pathVector = config['strData'].get('filePathVector')
        selectedFileLabelVector.config(text='Последний выбранный файл: ' + pathVector)
        xAxisComboboxSurface.set(config['strData'].get('axisXSurface'))
        xAxisComboboxApproximation.set(config['strData'].get('axisXApproximation'))
        xAxisComboboxVector.set(config['strData'].get('axisXVector'))
        yAxisComboboxSurface.set(config['strData'].get('axisYSurface'))
        yAxisComboboxApproximation.set(config['strData'].get('axisYApproximation'))
        numCellsEntrySurface.insert(tk.END, config['strData'].get('numCellsSurface'))
        numCellsEntryVector.insert(tk.END, config['strData'].get('numCellsVector'))
        stepEntryApproximation.insert(tk.END, config['strData'].get('stepEntryApproximation'))
        formulaEntrySurface.insert(tk.END, config['strData'].get('enteredFormulaSurface'))
        formulaEntryVector.insert(tk.END, config['strData'].get('enteredFormulaVector'))
        formulaEntryApproximation.insert(tk.END, config['strData'].get('resultingformula'))
    if 'status' in config:
        var.set(int(config['status'].get('statusCheckBox')))

############################### Functions_Surface ######################################
def select_input_file_surface():
    global pathSurface  # указываем, что используем глобальную переменную path
    filePath = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    # Здесь можно выполнить действия с выбранным CSV-файлом
    if filePath:
        selectedFileLabelSurface.config(text='Последний выбранный файл: ' + filePath)
        strArr = lib_common.file_read_lines(filePath)
        dataArr = strArr[0].split(";") #Добавили только заголовки
        update_axis_combobox_surface(dataArr)
        pathSurface = filePath  # сохраняем содержимое файла в глобальной переменной

def update_axis_combobox_surface(values):
    xAxisComboboxSurface['values'] = values
    yAxisComboboxSurface['values'] = values

#Функция для обработки выбора из автодополнения
def show_variable_list_surface(event):
    global pathSurface  # указываем, что используем глобальную переменную path
    formula = formulaEntrySurface.get()
    parts = lib_common.re.split(r'[+\-*/( ]', formula) #используем операторы в качестве разделителей
    currentPart = parts[-1] if parts else ''
    variableList.delete(0, tk.END)
    if pathSurface:
        strArr = lib_common.file_read_lines(pathSurface)
        dataArr = strArr[0].split(";")  # Добавили только заголовки
        for iter in range(len(dataArr)):
            dataArr[iter] = dataArr[iter].split(",")[0]
    else:
        dataArr = []
    matchingVars = [var for var in dataArr if var.startswith(currentPart)]
    if len(matchingVars) != 1:
        for var in matchingVars:
            variableList.insert(tk.END, var)
        if matchingVars:
            #variableList.pack()
            variableList.place(relx=0.5, y=390, anchor="n")
        else:
            variableList.pack_forget()

def insert_variable_surface(event):
    selectedVar = variableList.get(variableList.curselection())
    #formulaEntrySurface.delete(0, tk.END) #удаляет содержимое tk.Entry
    formulaEntrySurface.insert(tk.END, selectedVar) #добавляет текст из variable в конец
    variableList.pack_forget() #Скрывает List с экрана
    formulaEntrySurface.focus_set()#устанавливает фокус на Entry, чтобы после выбора из списка не нужно было снова тыкать на Entry
    #show_variable_list_surface(None)


def run_program_surface():
    global csvRecordListSurface, allDataFromFile # указываем, что используем глобальную переменную
    #ПРОВЕРКИ
    xAxis = xAxisComboboxSurface.get()
    if len(xAxis) == 0:
        messagebox.showerror('Ошибка', 'Не задана ось Х.')
        return
    yAxis = yAxisComboboxSurface.get()
    if len(yAxis) == 0:
        messagebox.showerror('Ошибка', 'Не задана ось Y.')
        return
    numCells = numCellsEntrySurface.get()
    if not numCells.isdigit() or int(numCells) < 0:
        messagebox.showerror('Ошибка', 'Неверное задано количество ячеек.')
        return
    formula = formulaEntrySurface.get()
    try:
        ast.parse(formula)
    except SyntaxError:
        messagebox.showerror('Ошибка', 'Формула не корректна.')
        return

    # ПРОГРАММА
    if var.get() == 1:
        dataFromFile = lib_common.file_read_lines(pathSurface)
        strArr = dataFromFile
        strArr = strArr[0].split(";")  # Добавили только заголовки
        for iter in range(0,len(strArr)):
            if xAxis == strArr[iter]:
                columnX = iter
            if yAxis == strArr[iter]:
                columnY = iter

        tempArr = strArr  # Добавили только заголовки
        for iter in range(len(strArr)):
            tempArr[iter] = strArr[iter].split(",")[0]
        dataArr = lib_common.data_arr_creating(dataFromFile)
        allDataFromFile = allDataFromFile + dataArr
        arrZ = app_vector.columnZ_creating(allDataFromFile, formula, tempArr)
        pointsArr = app_vector.points_arr_creating(allDataFromFile, columnX, columnY, arrZ)
        maxValX = max(pointsArr, key=lambda point: float(point.X)).X  # максимальное Х из массива точек
        maxValY = max(pointsArr, key=lambda point: float(point.Y)).Y  # максимальное Y из массива точек
        minValX = min(pointsArr, key=lambda point: float(point.X)).X  # минимальное Х из массива точек
        minValY = min(pointsArr, key=lambda point: float(point.Y)).Y  # минимальное Y из массива точек
        maxValZ = max(pointsArr, key=lambda point: float(point.Z)).Z  # максимальное Z из массива точек
        minValZ = min(pointsArr, key=lambda point: float(point.Z)).Z  # минимальное Z из массива точек
        sortedPoints = app_vector.points_sort(app_vector.Axis(float(minValX), float(maxValX), int(numCells)),
                                              app_vector.Axis(float(minValY), float(maxValY), int(numCells)), pointsArr)
        avgPointsArr = app_vector.avg_sorted_points(app_vector.Axis(float(minValX), float(maxValX), int(numCells)),
                                                    app_vector.Axis(float(minValY), float(maxValY), int(numCells)), sortedPoints)

        csvRecord = app_vector.replace_symbols_surface(avgPointsArr, '.', ',')
        csvRecordListSurface = app_vector.process_list_to_csvFormat_surface(csvRecord)
        csvRecord = app_vector.replace_symbols_surface(avgPointsArr, ',', '.')
        app_vector.surface(avgPointsArr, pointsArr)
        allDataFromFile = []
    else:
        dataFromFile = lib_common.file_read_lines(pathSurface)
        strArr = dataFromFile
        strArr = strArr[0].split(";")  # Добавили только заголовки
        for iter in range(0, len(strArr)):
            if xAxis == strArr[iter]:
                columnX = iter
            if yAxis == strArr[iter]:
                columnY = iter
        tempArr = strArr  # Добавили только заголовки
        for iter in range(len(strArr)):
            tempArr[iter] = strArr[iter].split(",")[0]
        dataArr = lib_common.data_arr_creating(dataFromFile)
        allDataFromFile = allDataFromFile + dataArr
        arrZ = app_vector.columnZ_creating(allDataFromFile, formula, tempArr)
        pointsArr = app_vector.points_arr_creating(allDataFromFile, columnX, columnY, arrZ)
        maxValX = max(pointsArr, key=lambda point: float(point.X)).X  # максимальное Х из массива точек
        maxValY = max(pointsArr, key=lambda point: float(point.Y)).Y  # максимальное Y из массива точек
        minValX = min(pointsArr, key=lambda point: float(point.X)).X  # минимальное Х из массива точек
        minValY = min(pointsArr, key=lambda point: float(point.Y)).Y  # минимальное Y из массива точек
        maxValZ = max(pointsArr, key=lambda point: float(point.Z)).Z  # максимальное Z из массива точек
        minValZ = min(pointsArr, key=lambda point: float(point.Z)).Z  # минимальное Z из массива точек
        sortedPoints = app_vector.points_sort(app_vector.Axis(float(minValX), float(maxValX), int(numCells)),
                                              app_vector.Axis(float(minValY), float(maxValY), int(numCells)), pointsArr)
        avgPointsArr = app_vector.avg_sorted_points(app_vector.Axis(float(minValX), float(maxValX), int(numCells)),
                                                    app_vector.Axis(float(minValY), float(maxValY), int(numCells)), sortedPoints)

        csvRecord = app_vector.replace_symbols_surface(avgPointsArr, '.', ',')
        csvRecordListSurface = app_vector.process_list_to_csvFormat_surface(csvRecord)
        csvRecord = app_vector.replace_symbols_surface(avgPointsArr, ',', '.')
        app_vector.surface(avgPointsArr, pointsArr)

def download_file_surface():
    strBuf = lib_common.generate_csv_file(csvRecordListSurface)  # записываем в csv файл
    filePath = filedialog.asksaveasfilename(defaultextension=".csv")
    with open(filePath, mode="w") as file:
        file.write(strBuf)

def copy_to_clipboard_surface():
    strBuf = lib_common.generate_csv_buf(csvRecordListSurface)  # записываем в csv файл
    lib_common.pyperclip.copy(strBuf)

def reset_data_file_surface():
    global allDataFromFile
    allDataFromFile = []
    selectedFileLabelSurface.config(text='Последний выбранный файл: ')

def reset_data_surface():
    global pathSurface
    reset_data_file_surface()
    pathSurface = ''
    xAxisComboboxSurface.set('')
    yAxisComboboxSurface.set('')
    numCellsEntrySurface.delete(0, tk.END)
    formulaEntrySurface.delete(0, tk.END)

############################### Functions_Approximation ######################################

def select_input_file_approximation():
    global pathApproximation  # указываем, что используем глобальную переменную path
    filePath = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    # Здесь можно выполнить действия с выбранным CSV-файлом
    if filePath:
        selectedFileLabelApproximation.config(text='Выбранный файл: ' + filePath)
        strArr = lib_common.file_read_lines(filePath)
        dataArr = strArr[0].split(";") #Добавили только заголовки
        update_axis_combobox_approximation(dataArr)
        pathApproximation = filePath  # сохраняем содержимое файла в глобальной переменной

def update_axis_combobox_approximation(values):
    xAxisComboboxApproximation['values'] = values
    yAxisComboboxApproximation['values'] = values

def is_float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False

def run_program_approximation():
    global csvRecordListApproximation, formula  # указываем, что используем глобальную переменную
    # ПРОВЕРКИ
    xAxis = xAxisComboboxApproximation.get()
    if len(xAxis) == 0:
        messagebox.showerror('Ошибка', 'Не задан УОЗ.')
        return
    yAxis = yAxisComboboxApproximation.get()
    if len(yAxis) == 0:
        messagebox.showerror('Ошибка', 'Не задан крутящий момент.')
        return
    step = stepEntryApproximation.get()
    if not is_float(step) or float(step) < 0:
        messagebox.showerror('Ошибка', 'Неверное задан шаг.')
        return

    headings = lib_common.file_read_lines(pathApproximation)[0]  # наименования столбцов
    strArr = headings
    strArr = strArr.split(";")  # Добавили только заголовки
    referenceCol_1 = 0 # номер столбца УОЗ
    referenceCol_2 = 0 # номер столбца рутящего момента
    counter = 0 # счётчик
    for name in strArr:
        if (xAxis == name):
            referenceCol_1 = counter
        if (yAxis == name):
            referenceCol_2 = counter
        counter += 1
    dataArr = lib_common.process_csv_file(pathApproximation) # преобразовываем csv файл в массив, с которым работаем
    #dataArr = replace_symbols(dataArr, ',','.')
    resultArr = app_approximation.process_list(dataArr, referenceCol_1, step) #очищаем лишние данные
    csvRecord = lib_common.replace_symbols(resultArr, '.', ',')
    csvRecord = lib_common.process_list_to_csvFormat(csvRecord) #преобразовываем список в тот вид, который подходит для записи в csv файл
    csvRecord.insert(0, headings) #вставляем в начало наименования столбцов
    csvRecordListApproximation = csvRecord
    resultArr = lib_common.replace_symbols(resultArr, ',', '.')

    formula = app_approximation.approx_func(resultArr, 3, referenceCol_1, referenceCol_2, strArr[referenceCol_1], strArr[referenceCol_2]) # аппроксимация и построение графика; 3 - степень аппроксимации
    update_entry_approximation(formula)

def update_entry_approximation(formula):
    formulaEntryApproximation.delete(0, tk.END)
    formulaEntryApproximation.insert(0, formula)

def copy_to_clipboard_formula():
    lib_common.pyperclip.copy(formula)

def download_file_approximation():
    strBuf = lib_common.generate_csv_file(csvRecordListApproximation)  # записываем в csv файл
    filePath = filedialog.asksaveasfilename(defaultextension=".csv")
    with open(filePath, mode="w") as file:
        file.write(strBuf)

def reset_data_approximation():
    global pathApproximation
    selectedFileLabelApproximation.config(text='Последний выбранный файл: ')
    pathApproximation = ''
    xAxisComboboxApproximation.set('')
    yAxisComboboxApproximation.set('')
    stepEntryApproximation.delete(0, tk.END)
    formulaEntryApproximation.delete(0, tk.END)

############################### Functions_Vector ######################################
def select_input_file_vector():
    global pathVector  # указываем, что используем глобальную переменную path
    filePath = filedialog.askopenfilename(filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    # Здесь можно выполнить действия с выбранным CSV-файлом
    if filePath:
        selectedFileLabelVector.config(text='Выбранный файл: ' + filePath)
        strArr = lib_common.file_read_lines(filePath)
        dataArr = strArr[0].split(";") #Добавили только заголовки
        update_axis_combobox_vector(dataArr)
        pathVector = filePath  # сохраняем содержимое файла в глобальной переменной

def update_axis_combobox_vector(values):
    xAxisComboboxVector['values'] = values

def run_program_vector():
    global csvRecordListVector # указываем, что используем глобальную переменную
    #ПРОВЕРКИ
    xAxis = xAxisComboboxVector.get()
    if len(xAxis) == 0:
        messagebox.showerror('Ошибка', 'Не задана ось Х.')
        return
    numCells = numCellsEntryVector.get()
    if not numCells.isdigit() or int(numCells) < 0:
        messagebox.showerror('Ошибка', 'Неверное задано количество ячеек.')
        return
    formula = formulaEntryVector.get()
    try:
        ast.parse(formula)
    except SyntaxError:
        messagebox.showerror('Ошибка', 'Формула не корректна.')
        return

    # ПРОГРАММА

    dataFromFile = lib_common.file_read_lines(pathVector)
    strArr = dataFromFile
    strArr = strArr[0].split(";")  # Добавили только заголовки
    for iter in range(0,len(strArr)):
        if xAxis == strArr[iter]:
            columnX = iter
    columnY = None
    #currArr = strArr
    tempArr = strArr  # Добавили только заголовки
    for iter in range(0, len(strArr)):
        tempArr[iter] = tempArr[iter].split(",")[0]
    dataArr = lib_common.data_arr_creating(dataFromFile)
    arrZ = app_vector.columnZ_creating(dataArr, formula, tempArr)
    pointsArr = app_vector.points_arr_creating(dataArr, columnX, columnY, arrZ)
    for point in pointsArr:
        point.Y = point.Z
    maxValX = max(pointsArr, key=lambda point: float(point.X)).X  # максимальное Х из массива точек
    maxValY = max(pointsArr, key=lambda point: float(point.Y)).Y  # максимальное Y из массива точек
    minValX = min(pointsArr, key=lambda point: float(point.X)).X  # минимальное Х из массива точек
    minValY = min(pointsArr, key=lambda point: float(point.Y)).Y  # минимальное Y из массива точек
    sortedPoints = app_vector.points_sort_vector(app_vector.Axis(float(minValX), float(maxValX), int(numCells)), pointsArr)
    avgPointsArr = app_vector.avg_sorted_points_vector(app_vector.Axis(float(minValX), float(maxValX), int(numCells)), sortedPoints)
    csvRecord = app_vector.replace_symbols_surface(avgPointsArr, '.', ',')
    csvRecordListVector = app_vector.process_list_to_csvFormat_surface(csvRecord)
    csvRecord = app_vector.replace_symbols_surface(avgPointsArr, ',', '.')
    app_vector.vector_creating(avgPointsArr, app_vector.Axis(float(minValX), float(maxValX), 0),
                               app_vector.Axis(float(minValY), float(maxValY), 0), pointsArr, strArr[columnX])

#Функция для обработки выбора из автодополнения
def show_variable_list_vector(event):
    global pathVector  # указываем, что используем глобальную переменную path
    formula = formulaEntryVector.get()
    parts = lib_common.re.split(r'[+\-*/( ]', formula) #используем операторы в качестве разделителей
    currentPart = parts[-1] if parts else ''
    variableListVector.delete(0, tk.END)
    if pathVector:
        strArr = lib_common.file_read_lines(pathVector)
        dataArr = strArr[0].split(";")  # Добавили только заголовки
        for iter in range(len(dataArr)):
            dataArr[iter] = dataArr[iter].split(",")[0]
    else:
        dataArr = []
    matchingVars = [var for var in dataArr if var.startswith(currentPart)]
    if len(matchingVars) != 1:
        for var in matchingVars:
            variableListVector.insert(tk.END, var)
        if matchingVars:
            variableListVector.place(relx=0.5, y=305, anchor="n")
        else:
            variableListVector.pack_forget()

def insert_variable_vector(event):
    selectedVar = variableListVector.get(variableListVector.curselection())
    #formulaEntrySurface.delete(0, tk.END) #удаляет содержимое tk.Entry
    formulaEntryVector.insert(tk.END, selectedVar) #добавляет текст из variable в конец
    variableListVector.pack_forget() #Скрывает List с экрана
    formulaEntryVector.focus_set()#устанавливает фокус на Entry, чтобы после выбора из списка не нужно было снова тыкать на Entry
    #show_variable_list_surface(None)

def download_file_vector():
    strBuf = lib_common.generate_csv_file(csvRecordListVector)  # записываем в csv файл
    filePath = filedialog.asksaveasfilename(defaultextension=".csv")
    with open(filePath, mode="w") as file:
        file.write(strBuf)

def copy_to_clipboard_vector():
    strBuf = lib_common.generate_csv_buf(csvRecordListVector)  # записываем в csv файл
    lib_common.pyperclip.copy(strBuf)


def reset_data_vector():
    global pathVector
    selectedFileLabelVector.config(text='Последний выбранный файл: ')
    pathVector = ''
    xAxisComboboxVector.set('')
    numCellsEntryVector.delete(0, tk.END)
    formulaEntryVector.delete(0, tk.END)
############################### GUI ######################################

root = tk.Tk()
root.title("Пример GUI")
root.geometry("800x800+{}+{}".format(root.winfo_screenwidth() // 2 - 400, root.winfo_screenheight() // 2 - 400))
pathSurface, pathApproximation, pathVector = "", "", ""  # глобальная переменная для сохранения пути из файла
csvRecordListSurface, csvRecordListApproximation, csvRecordListVector = '', '', '' #Список для записи в файл
allDataFromFile = [] #хранить данные из файла (для их суммирования)
formula = '' #формула

# Создание вкладок
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="y")

# Вкладка "Создание поверхности"
surfaceTab = ttk.Frame(notebook)
notebook.add(surfaceTab, text="Создание поверхности")

#RadioButton
var = app_vector.IntVar() # получает 1, если активен, и 0, если неактивен
checkButtonSurface = app_vector.Checkbutton(surfaceTab, text="Сбрасывать данные при открытии файла", variable=var, onvalue=1, offvalue=0)
checkButtonSurface.place(relx=0.5, y=20, anchor="n")
checkButtonSurface.select() # активное исходное состояние

# Надпись после выбора файла
selectedFileLabelSurface = ttk.Label(surfaceTab, text='Последний выбранный файл: ')
selectedFileLabelSurface.pack()

# Раздел выбора файла во вкладке "Создание поверхности"
fileFrameSurface = ttk.LabelFrame(surfaceTab, text="Выберите CSV-файл")
fileFrameSurface.place(relx=0.5, y=50, anchor="n")

fileButtonSurface = ttk.Button(fileFrameSurface, text="Выбрать файл", command=select_input_file_surface)
fileButtonSurface.config(width=25)
fileButtonSurface.pack(padx = 10, pady = 5)


resetButtonSurface = ttk.Button(surfaceTab, text="Сбросить файлы", command=reset_data_file_surface)
resetButtonSurface.place(relx=0.25, y=120, anchor="n")
resetButtonSurface.config(width=25)

resetSettingsButtonSurface = ttk.Button(surfaceTab, text="Сбросить настройки", command=reset_data_surface)
resetSettingsButtonSurface.place(relx=0.75, y=120, anchor="n")
resetSettingsButtonSurface.config(width=25)

# Раздел выбора осей, ввода параметров и кнопки запуска программы во вкладке "Создание поверхности"
xAxisLabelSurface = ttk.Label(surfaceTab, text="Выберите базовую ось X:")
xAxisLabelSurface.place(relx=0.5, y=150, anchor="n")

xAxisValuesSurface=[]
xAxisComboboxSurface = ttk.Combobox(surfaceTab,values=xAxisValuesSurface, state='readonly')
xAxisComboboxSurface.place(relx=0.5, y=180, anchor="n")
xAxisComboboxSurface.config(width=40)

yAxisLabelSurface = ttk.Label(surfaceTab, text="Выберите базовую ось Y:")
yAxisLabelSurface.place(relx=0.5, y=210, anchor="n")

yAxisValuesSurface=[]
yAxisComboboxSurface = ttk.Combobox(surfaceTab, values=yAxisValuesSurface, state='readonly')
yAxisComboboxSurface.place(relx=0.5, y=240, anchor="n")
yAxisComboboxSurface.config(width=40)

numCellsLabelSurface = ttk.Label(surfaceTab, text="Введите количество ячеек:")
numCellsLabelSurface.place(relx=0.5, y=270, anchor="n")

numCellsEntrySurface = ttk.Entry(surfaceTab)
numCellsEntrySurface.place(relx=0.5, y=300, anchor="n")
numCellsEntrySurface.config(width=40)

#Список для отображения переменных
variableList = app_vector.Listbox(surfaceTab)
variableList.bind("<Double-Button-1>", insert_variable_surface)
variableList.place(relx=0.5, y=390, anchor="n")

formulaLabelSurface = ttk.Label(surfaceTab, text="Введите формулу.")
formulaLabelSurface.place(relx=0.5, y=330, anchor="n")

zLabelSurface = ttk.Label(surfaceTab, text="Z =")
zLabelSurface.place(relx=0.1, y=360)

formulaEntrySurface = app_vector.Entry(surfaceTab)
formulaEntrySurface.place(relx=0.5, y=360, anchor="n")
formulaEntrySurface.config(width=40)
#<KeyRelease> - отпускание клавиши
formulaEntrySurface.bind("<KeyRelease>", show_variable_list_surface)
#"<FocusIn>" - фокус на виджете
formulaEntrySurface.bind("<FocusIn>", show_variable_list_surface)

runButtonSurface = ttk.Button(surfaceTab, text="Запустить программу", command=run_program_surface)
runButtonSurface.place(relx=0.5, y=570, anchor="n")
runButtonSurface.config(width=25)

copyButtonSurface = ttk.Button(surfaceTab, text="Скопировать результат", command=copy_to_clipboard_surface)
copyButtonSurface.place(relx=0.5, y=600, anchor="n")
copyButtonSurface.config(width=25)

downloadButtonSurface = ttk.Button(surfaceTab, text="Скачать таблицу", command=download_file_surface)
downloadButtonSurface.place(relx=0.5, y=630, anchor="n")
downloadButtonSurface.config(width=25)

#---------------------------------------------------------------------------------------------------------
# Вкладка "Аппроксимация"
approximationTab = ttk.Frame(notebook)
notebook.add(approximationTab, text="Аппроксимация")

# Надпись после выбора файла
selectedFileLabelApproximation = ttk.Label(approximationTab, text='Выбранный файл: ')
selectedFileLabelApproximation.pack()

# Раздел выбора файла во вкладке "Аппроксимация"
fileFrameApproximation = ttk.LabelFrame(approximationTab, text="Выберите CSV-файл")
fileFrameApproximation.place(relx=0.5, y=20, anchor="n")

fileButtonApproximation = ttk.Button(fileFrameApproximation, text="Выбрать файл", command=select_input_file_approximation)
fileButtonApproximation.config(width=25)
fileButtonApproximation.pack(padx=10, pady=10)

resetSettingsButtonApproximation = ttk.Button(approximationTab, text="Сбросить настройки", command=reset_data_approximation)
resetSettingsButtonApproximation.place(relx=0.5, y=90, anchor="n")
resetSettingsButtonApproximation.config(width=25)

# Раздел выбора осей, ввода параметров и кнопки запуска программы во вкладке "Аппроксимация"
xAxisLabelApproximation = ttk.Label(approximationTab, text="Выберите данные УОЗ:")
xAxisLabelApproximation.place(relx=0.5, y=120, anchor="n")

xAxisValuesApproximation=[]
xAxisComboboxApproximation = ttk.Combobox(approximationTab, values=xAxisValuesApproximation, state='readonly')
xAxisComboboxApproximation.place(relx=0.5, y=150, anchor="n")
xAxisComboboxApproximation.config(width=40)

yAxisValuesApproximation=[]
yAxisLabelApproximation = ttk.Label(approximationTab, text="Выберите данные крутящего момента:")
yAxisLabelApproximation.place(relx=0.5, y=180, anchor="n")

yAxisComboboxApproximation = ttk.Combobox(approximationTab, values=yAxisValuesApproximation, state='readonly')
yAxisComboboxApproximation.place(relx=0.5, y=210, anchor="n")
yAxisComboboxApproximation.config(width=40)

stepApproximation = ttk.Label(approximationTab, text="Шаг:")
stepApproximation.place(relx=0.5, y=240, anchor="n")

stepEntryApproximation = ttk.Entry(approximationTab)
stepEntryApproximation.place(relx=0.5, y=270, anchor="n")
stepEntryApproximation.config(width=40)

formulaLabelApproximation = ttk.Label(approximationTab, text="Полученная формула:")
formulaLabelApproximation.place(relx=0.5, y=300, anchor="n")

formulaEntryApproximation = ttk.Entry(approximationTab)
formulaEntryApproximation.place(relx=0.5, y=330, anchor="n")
formulaEntryApproximation.config(width=40)

runButtonApproximation = ttk.Button(approximationTab, text="Запустить программу", command=run_program_approximation)
runButtonApproximation.config(width=25)
runButtonApproximation.place(relx=0.5, y=360, anchor="n")

copyButtonApproximation = ttk.Button(approximationTab, text="Скопировать результат", command=copy_to_clipboard_formula)
copyButtonApproximation.config(width=25)
copyButtonApproximation.place(relx=0.5, y=390, anchor="n")

downloadButtonApproximation = ttk.Button(approximationTab, text="Скачать таблицу", command=download_file_approximation)
downloadButtonApproximation.config(width=25)
downloadButtonApproximation.place(relx=0.5, y=420, anchor="n")

#---------------------------------------------------------------------------------------------------------
# Вкладка "Построение вектора"
vectorTab = ttk.Frame(notebook)
notebook.add(vectorTab, text="Построение вектора")

# Надпись после выбора файла
selectedFileLabelVector = ttk.Label(vectorTab, text='Выбранный файл: ')
selectedFileLabelVector.pack()

# Раздел выбора файла во вкладке "Создание вектора"
fileFrameVector = ttk.LabelFrame(vectorTab, text="Выберите CSV-файл")
fileFrameVector.place(relx=0.5, y=20, anchor="n")

fileButtonVector = ttk.Button(fileFrameVector, text="Выбрать файл", command=select_input_file_vector)
fileButtonVector.pack(padx=10, pady=5)
fileButtonVector.config(width=25)

resetSettingsButtonVector = ttk.Button(vectorTab, text="Сбросить настройки", command=reset_data_vector)
resetSettingsButtonVector.place(relx=0.5, y=90, anchor="n")
resetSettingsButtonVector.config(width=25)

# Раздел выбора осей, ввода параметров и кнопки запуска программы во вкладке "Создание вектора"
xAxisLabelVector = ttk.Label(vectorTab, text="Выберите базовую ось X:")
xAxisLabelVector.place(relx=0.5, y=120, anchor="n")

xAxisValuesVector=[]
xAxisComboboxVector = ttk.Combobox(vectorTab, values=xAxisValuesVector, state='readonly')
xAxisComboboxVector.place(relx=0.5, y=150, anchor="n")
xAxisComboboxVector.config(width=40)

numCellsLabelVector = ttk.Label(vectorTab, text="Введите количество ячеек:")
numCellsLabelVector.place(relx=0.5, y=180, anchor="n")

numCellsEntryVector = ttk.Entry(vectorTab)
numCellsEntryVector.place(relx=0.5, y=210, anchor="n")
numCellsEntryVector.config(width=40)

#Список для отображения переменных
variableListVector = tk.Listbox(vectorTab)
variableListVector.bind("<Double-Button-1>", insert_variable_vector)
variableListVector.place(relx=0.5, y=305, anchor="n")

formulaLabelVector = ttk.Label(vectorTab, text="Введите формулу.")
formulaLabelVector.place(relx=0.5, y=240, anchor="n")

formulaLabelVector = ttk.Label(vectorTab, text="Y =")
formulaLabelVector.place(relx=0.1, y=270, anchor="n")

formulaEntryVector = ttk.Entry(vectorTab)
formulaEntryVector.place(relx=0.5, y=270, anchor="n")
formulaEntryVector.config(width=40)
#<KeyRelease> - отпускание клавиши
formulaEntryVector.bind("<KeyRelease>", show_variable_list_vector)
#"<FocusIn>" - фокус на виджете
formulaEntryVector.bind("<FocusIn>", show_variable_list_vector)

runButtonVector = ttk.Button(vectorTab, text="Запустить программу", command=run_program_vector)
runButtonVector.place(relx=0.5, y=480, anchor="n")
runButtonVector.config(width=25)

copyButtonVector = ttk.Button(vectorTab, text="Скопировать результат", command=copy_to_clipboard_vector)
copyButtonVector.place(relx=0.5, y=510, anchor="n")
copyButtonVector.config(width=25)

downloadButtonVector = ttk.Button(vectorTab, text="Скачать таблицу", command=download_file_vector)
downloadButtonVector.place(relx=0.5, y=540, anchor="n")
downloadButtonVector.config(width=25)

notebook.pack(padx=10, pady=10)

# saveCfgButton = ttk.Button(text="Сохранить конфиг", command=creating_cfg)
# saveCfgButton.config(width=25)
# saveCfgButton.pack(padx = 10, pady = 5)
#
# getCfgButton = ttk.Button(text="Загрузить конфиг", command=get_cfg_data)
# getCfgButton.config(width=25)
# getCfgButton.pack(padx = 10, pady = 5)

#Получает данные из файла .cfg
get_cfg_data()
#Действия после закрытия окна
root.protocol("WM_DELETE_WINDOW", creating_cfg)

root.mainloop()