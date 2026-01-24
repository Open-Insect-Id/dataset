# Vérifier l'installation de Python
echo "Vérification de l'installation de Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Python3 n'est pas installé. Veuillez installer Python3."
    exit 1
fi

# Créer l'environnement virtuel
echo "Création de l'environnement virtuel..."
python3 -m venv venv

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Vérifier l'installation
echo "Vérification de l'installation..."
python --version
pip list | grep -E "(Pillow|ijson)"

echo "Installation terminée."