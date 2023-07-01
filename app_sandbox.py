# ############################### Libraries ######################################
import os

# получаем путь до папки с файлами
currentDir = os.path.dirname(os.path.abspath(__file__))
includePath = os.path.join(currentDir, 'venv', 'include')

import sys

sys.path.append(includePath)

import gui_sandbox
