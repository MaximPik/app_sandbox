############################### Libraries ######################################
import os
import sys
import importlib


############################### Functions ######################################
# установки необходимых библиотек при запуске программы
def setup():
    # список библиотек для установки
    requiredLibraries = ['numpy', 'matplotlib', 'pyinstaller']

    missingLibraries = []
    # проверка наличия установленных библиотек
    for library in requiredLibraries:
        try:
            importlib.import_module((library))
            print(f"Библиотека {library} установлена.")
        except ImportError:
            missingLibraries.append(library)
            print(f"Библиотека {library} не найдена.")

    if missingLibraries:
        for library in missingLibraries:
            os.system(f'pip install {library}')
            print(f'Установка завершена {library}.')
    else:
        print('Все библиотеки уже установлены.')
    return

# Функция для создания exe файла
def cr_exe():
    # проверка на наличие файла
    # получаем текущий рабочий каталог
    exePath = os.path.join(os.getcwd(), 'app_sandbox.exe')
    pyinstallerPath = sys.executable.replace('python.exe', 'pyinstaller.exe')
    if os.path.exists(exePath):
        print('Файл app_sandbox.exe уже существует.')
    else:
        # os.system('pip install pyinstaller')
        os.system(f'{pyinstallerPath} app_sandbox.py --onefile --windowed --distpath "{os.getcwd()}"')
        print('Файл app_sandbox.exe создан.')
    return
############################### Programm ######################################
# currentDir = os.path.dirname(os.path.abspath(__file__))
# # Добавляем путь в sys.path
# sys.path.append(currentDir)
# print(currentDir)

#includePath = os.path.join(currentDir, 'venv', 'include')
print(sys.path)
setup()
cr_exe()
