# templates.py
"""Module pour les modèles de code Python"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QSplitter,
                           QListWidget, QTextEdit, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from theme import ModernTheme
from editor import PythonHighlighter


class CodeTemplates(QDialog):
    """Modèles de code Python"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modèles de code")
        self.resize(700, 500)

        self.setStyleSheet(ModernTheme.get_stylesheet())

        self.templates = {
            "Connexion à la base": '''# Connexion à une base de données SQLite
import sqlite3

# Connexion
conn = sqlite3.connect('ma_base.db')
cursor = conn.cursor()

# Utilisation
try:
    cursor.execute("SELECT * FROM ma_table")
    results = cursor.fetchall()
    for row in results:
        print(row)
finally:
    conn.close()
''',

            "Création de table": '''# Créer une nouvelle table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT UNIQUE,
        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()
''',

            "Insertion de données": '''# Insérer des données
client = ('Dupont', 'Jean', 'jean.dupont@email.com')
cursor.execute("""
    INSERT INTO clients (nom, prenom, email) 
    VALUES (?, ?, ?)
""", client)
conn.commit()

# Insertion multiple
clients = [
    ('Martin', 'Marie', 'marie.martin@email.com'),
    ('Bernard', 'Paul', 'paul.bernard@email.com'),
]
cursor.executemany("""
    INSERT INTO clients (nom, prenom, email) 
    VALUES (?, ?, ?)
""", clients)
conn.commit()
''',

            "Mise à jour": '''# Mettre à jour des données
cursor.execute("""
    UPDATE clients 
    SET email = ? 
    WHERE id = ?
""", ('nouveau.email@example.com', 1))
conn.commit()
''',

            "Suppression": '''# Supprimer des données
cursor.execute("DELETE FROM clients WHERE id = ?", (1,))
conn.commit()
''',

            "Transaction": '''# Utiliser des transactions
try:
    conn.execute("BEGIN")

    # Plusieurs opérations
    cursor.execute("INSERT INTO comptes (client_id, solde) VALUES (?, ?)", (1, 1000))
    cursor.execute("UPDATE clients SET actif = 1 WHERE id = ?", (1,))

    conn.commit()
    print("Transaction réussie")

except Exception as e:
    conn.rollback()
    print(f"Erreur, annulation: {e}")
''',

            "Requête avec jointure": '''# Jointure entre tables
cursor.execute("""
    SELECT c.nom, c.prenom, co.numero, co.solde
    FROM clients c
    JOIN comptes co ON c.id = co.client_id
    WHERE co.solde > ?
""", (1000,))

for row in cursor.fetchall():
    print(f"{row[0]} {row[1]}: Compte {row[2]}, Solde: {row[3]}€")
''',

            "Export CSV": '''# Exporter vers CSV
import csv

cursor.execute("SELECT * FROM clients")
with open('export_clients.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # En-têtes
    writer.writerow([description[0] for description in cursor.description])

    # Données
    writer.writerows(cursor.fetchall())
''',

            "Import CSV": '''# Importer depuis CSV
import csv

with open('clients.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        cursor.execute("""
            INSERT INTO clients (nom, prenom, email) 
            VALUES (:nom, :prenom, :email)
        """, row)

    conn.commit()
''',

            "Classe modèle": '''# Classe pour gérer une table
class Client:
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def create(self, nom, prenom, email):
        """Créer un nouveau client"""
        self.cursor.execute("""
            INSERT INTO clients (nom, prenom, email) 
            VALUES (?, ?, ?)
        """, (nom, prenom, email))
        self.conn.commit()
        return self.cursor.lastrowid

    def find(self, id):
        """Trouver un client par ID"""
        self.cursor.execute("SELECT * FROM clients WHERE id = ?", (id,))
        return self.cursor.fetchone()

    def update(self, id, **kwargs):
        """Mettre à jour un client"""
        fields = ', '.join(f"{k} = ?" for k in kwargs.keys())
        values = list(kwargs.values()) + [id]

        self.cursor.execute(f"""
            UPDATE clients SET {fields} WHERE id = ?
        """, values)
        self.conn.commit()

    def delete(self, id):
        """Supprimer un client"""
        self.cursor.execute("DELETE FROM clients WHERE id = ?", (id,))
        self.conn.commit()

    def all(self):
        """Obtenir tous les clients"""
        self.cursor.execute("SELECT * FROM clients")
        return self.cursor.fetchall()

# Utilisation
client_model = Client(conn)
new_id = client_model.create("Durand", "Sophie", "sophie@email.com")
print(f"Nouveau client créé avec l'ID: {new_id}")
'''
        }

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Liste des modèles
        self.template_list = QListWidget()
        self.template_list.addItems(self.templates.keys())
        self.template_list.currentTextChanged.connect(self.show_template)

        # Aperçu du code
        self.code_preview = QTextEdit()
        self.code_preview.setReadOnly(True)
        self.code_preview.setFont(QFont('Consolas', 10))

        # Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.template_list)
        splitter.addWidget(self.code_preview)
        splitter.setSizes([200, 500])

        # Boutons
        buttons_layout = QHBoxLayout()

        insert_btn = QPushButton("Insérer dans l'éditeur")
        insert_btn.clicked.connect(self.accept)

        copy_btn = QPushButton("Copier")
        copy_btn.clicked.connect(self.copy_code)

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(insert_btn)
        buttons_layout.addWidget(copy_btn)
        buttons_layout.addWidget(close_btn)

        layout.addWidget(splitter)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Sélectionner le premier modèle
        if self.template_list.count() > 0:
            self.template_list.setCurrentRow(0)

    def show_template(self, template_name):
        """Afficher le modèle sélectionné"""
        if template_name in self.templates:
            self.code_preview.setPlainText(self.templates[template_name])

            # Coloration syntaxique
            highlighter = PythonHighlighter(self.code_preview.document())

    def copy_code(self):
        """Copier le code dans le presse-papier"""
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.code_preview.toPlainText())

    def get_selected_code(self):
        """Obtenir le code sélectionné"""
        return self.code_preview.toPlainText()