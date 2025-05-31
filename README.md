# PyFoxPro IDE

Un IDE moderne pour Python inspiré de Visual FoxPro, conçu pour faciliter la migration et le développement d'applications de base de données.

## 🚀 Fonctionnalités

- **Éditeur de code** avec coloration syntaxique Python
- **Explorateur de base de données** SQLite intégré
- **Générateur de requêtes SQL** visuel
- **Concepteur de formulaires** drag & drop
- **Gestionnaire de projets** avec arborescence de fichiers
- **Console d'exécution** intégrée
- **Modèles de code** prêts à l'emploi
- **Visualiseur de données** tabulaire

## 📋 Prérequis

- Python 3.8+
- PyQt6

## 🛠️ Installation

1. Cloner le repository :
```bash
git clone https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
cd VOTRE_REPO
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install PyQt6
```

## 🚀 Utilisation

Lancer l'IDE :
```bash
python main.py
```

## 📁 Structure du projet

```
├── main.py           # Fichier principal
├── theme.py          # Thème et styles
├── editor.py         # Éditeur de code
├── database.py       # Modules base de données
├── console.py        # Console de sortie
├── sql_builder.py    # Générateur SQL
├── form_designer.py  # Concepteur de formulaires
├── templates.py      # Modèles de code
└── project.py        # Gestionnaire de projets
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Soumettre des pull requests

## 📝 Licence

Ce projet est sous licence MIT.

## 👤 Auteur

Eddy Maue

## 🙏 Remerciements

- Inspiré par Visual FoxPro
- Construit avec PyQt6
