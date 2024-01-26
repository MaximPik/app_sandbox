# ############################### Libraries ######################################
import os
import sys
import gui_sandbox

# получаем путь до папки с файлами
currentDir = os.path.dirname(os.path.abspath(__file__))
includePath = os.path.join(currentDir, 'venv', 'include')

sys.path.append(includePath)

def main():
    app = gui_sandbox.Application()
    app.mainloop()

main()