# INF3190 - TP3
**Vigaru, Edward Ionut**

## Installation et exécution du projet

### 1. Prérequis
Assurez-vous d’avoir **Python** installé sur votre machine. Si vous êtes sur macOS et que Python n'est pas installé, utilisez la commande suivante :
```sh
brew install python
```

De plus, vous devez disposer de **Homebrew**. Si ce n’est pas encore le cas, installez-le avec :
```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Création et activation d’un environnement virtuel
Créez un environnement virtuel et activez-le en exécutant les commandes suivantes :
```sh
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```
(Sur Windows, utilisez `venv\Scripts\activate`.)

### 3. Installation des dépendances
Une fois l’environnement activé, installez Flask avec :
```sh
pip install flask
```

### 4. Lancement du projet
Définissez le fichier principal pour Flask :
```sh
export FLASK_APP=index.py
```

Démarrez ensuite le serveur Flask :
```sh
flask run
```

### 5. Accès à l’application
Ouvrez un navigateur web et accédez à l’URL fournie par Flask, généralement :
```
http://127.0.0.1:5000
```

Votre application est maintenant en cours d’exécution ! 🚀