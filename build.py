import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '-w',
    '-y',
    '--clean',
    '-n Project Manager',
    '--icon=logo.ico'
])