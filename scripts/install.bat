@echo off

REM Vérifier l'installation de Python
echo Vérification de l'installation de Python...
python --version
if %errorlevel% neq 0 (
    echo Python n'est pas installé. Veuillez installer Python.
    exit /b 1
)

REM Créer l'environnement virtuel
echo Création de l'environnement virtuel...
python -m venv venv

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Installer les dépendances
echo Installation des dépendances...
pip install -r requirements.txt

REM Vérifier l'installation
echo Vérification de l'installation...
python --version
pip list | findstr /C:"Pillow" /C:"ijson"

echo Installation terminée.
pause