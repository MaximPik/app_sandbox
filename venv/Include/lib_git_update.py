import os
import sys
import subprocess
import tqdm

def install_git():
    # Проверить, установлен ли Git на компьютере
    try:
        subprocess.run(["git", "--version"], check=True)
        print("Git установлен на компьютере")
    except subprocess.CalledProcessError:
        print("Git не установлен на компьютере")

        # Попытаться скачать и установить Git с официального сайта
        try:
            import requests
            print("Скачивание Git с официального сайта")
            response = requests.get("https://git-scm.com/download/win")
            response.raise_for_status()
            with open("GitSetup.exe", "wb") as f:
                # Добавить индикатор прогресса для скачивания
                for chunk in tqdm.tqdm(response.iter_content(chunk_size=1024), total=int(response.headers['Content-Length']) // 1024, unit="KB"):
                    f.write(chunk)
            print("Запуск установки Git")
            subprocess.run(["GitSetup.exe"], check=True)
            print("Git успешно установлен")
        except Exception as e:
            print("Не удалось скачать или установить Git")
            print(e)
            sys.exit(1)

def update_programm(gitDirr, urlGit):
    # Перейти в папку с локальной копией программы
    os.chdir(gitDirr)
    #url = 'https://github.com/MaximPik/sandbox.git'

    # Получить изменения из удаленного репозитория
    subprocess.run(["git", "fetch", urlGit])
    #Проверка на наличие изменений
    output = subprocess.check_output(['git','diff','--name-only','HEAD',urlGit+'/master'])
    if output: #Если есть изменения, то внести их
        # Слить изменения с локальной веткой
        subprocess.run(["git", "merge", urlGit + "/master"])
        #Перезапуск текущей программы после обновления файлов
        pythonExe = sys.executable
        args = sys.argv
        os.execl(pythonExe, pythonExe, *args)
    else:
        print("Изменений нет.")
