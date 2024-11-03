import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "main.py",
        "-w",
        "-y",
        "--clean",
        "-n Project Manager",
        "--icon=logo.ico",
        "--onefile",
        "--add-data=path_file.txt;.",
        "--add-data=type_pm.txt;.",
        "--add-data=button_clicks.txt;.",
    ]
)
