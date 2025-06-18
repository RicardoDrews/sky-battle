import sys
import os
from cx_Freeze import setup, Executable



NOME_ARQUIVO_PRINCIPAL = "main.py"

pacotes_incluidos = [
    "pygame",
    "os",
    "sys",
    "random",
    "math",
    "datetime",
    "speech_recognition",
    "pyttsx3"
]

arquivos_incluidos = [
    ("Recursos", "Recursos"), 
]

build_exe_options = {
    "packages": pacotes_incluidos,
    "include_files": arquivos_incluidos,
    "excludes": ["tkinter"],
}

base = "Win32GUI" if sys.platform == "win32" else None

executables = [
    Executable(
        NOME_ARQUIVO_PRINCIPAL,
        base=base,
        target_name="SkyBattle.exe",
        icon="Recursos/imagens/aviao.ico" 
    )
]



setup(
    name="Sky Battle",
    version="1.0",
    description="Jogo de nave estilo steampunk | Ricardo Drews",
    author="Ricardo Drews",
    options={"build_exe": build_exe_options},
    executables=executables
)
