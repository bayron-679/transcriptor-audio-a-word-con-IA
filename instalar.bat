@echo off
title Instalador Profesional - Transcriptor Whisper
setlocal

:: 1. Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python no detectado. Descargando instalador silencioso...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe -OutFile python_installer.exe"
    echo [!] Instalando Python (esto tardara un par de minutos)...
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo [OK] Python instalado correctamente.
) else (
    echo [OK] Python ya esta instalado.
)

:: 2. Crear entorno virtual e instalar librerias
echo.
echo [*] Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate

echo [*] Instalando PyTorch con soporte CUDA (Este es el paso mas pesado)...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
echo [*] Instalando Whisper y dependencias...
pip install openai-whisper python-docx

:: 3. CREAR ACCESO DIRECTO EN EL ESCRITORIO
echo.
echo [*] Creando acceso directo en el escritorio...
set SCRIPT_PATH=%~dp0iniciar.bat
set ICON_PATH=%~dp0logo.ico
set SHORTCUT_PATH=%userprofile%\Desktop\TranscriptorIA.lnk

:: Generamos un pequeño script de VBScript al vuelo para crear el acceso directo
echo set WshShell = WScript.CreateObject("WScript.Shell") > create_shortcut.vbs
echo set oShellLink = WshShell.CreateShortcut("%SHORTCUT_PATH%") >> create_shortcut.vbs
echo oShellLink.TargetPath = "%SCRIPT_PATH%" >> create_shortcut.vbs
echo oShellLink.WorkingDirectory = "%~dp0" >> create_shortcut.vbs
echo oShellLink.WindowStyle = 1 >> create_shortcut.vbs
echo oShellLink.IconLocation = "%ICON_PATH%" >> create_shortcut.vbs
echo oShellLink.Description = "Transcriptor de Audio con IA" >> create_shortcut.vbs
echo oShellLink.Save >> create_shortcut.vbs

cscript /nologo create_shortcut.vbs
del create_shortcut.vbs

echo.
echo ======================================================
echo    INSTALACION FINALIZADA
echo    Ya puedes cerrar esta ventana y usar el icono 
echo    "TranscriptorIA" en tu escritorio.
echo ======================================================
pause