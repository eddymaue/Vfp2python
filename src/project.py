# project.py
"""Module pour la gestion de projets"""

import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (QDockWidget, QWidget, QVBoxLayout, QHBoxLayout,
                           QToolBar, QTreeWidget, QTreeWidgetItem, QMenu,
                           QDialog, QFormLayout, QLineEdit, QPushButton,
                           QDialogButtonBox, QFileDialog, QMessageBox,
                           QInputDialog, QStyle)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QAction


class ProjectManager(QDockWidget):
    """Gestionnaire de projets"""
    file_opened = pyqtSignal(str)

    def __init__(self):
        super().__init__("Gestionnaire de projet")

        self.project_path = None
        self.project_data = {
            'name': '',
            'files': [],
            'database': '',
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat()
        }

        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Barre d'outils du projet
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))

        new_project_action = QAction("📁 Nouveau projet", self)
        new_project_action.triggered.connect(self.new_project)

        open_project_action = QAction("📂 Ouvrir projet", self)
        open_project_action.triggered.connect(self.open_project)

        save_project_action = QAction("💾 Sauvegarder", self)
        save_project_action.triggered.connect(self.save_project)

        toolbar.addAction(new_project_action)
        toolbar.addAction(open_project_action)
        toolbar.addAction(save_project_action)

        # Arbre des fichiers
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabel("Fichiers du projet")
        self.file_tree.itemDoubleClicked.connect(self.open_file)

        # Menu contextuel
        self.file_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.show_context_menu)

        layout.addWidget(toolbar)
        layout.addWidget(self.file_tree)

        widget.setLayout(layout)
        self.setWidget(widget)

    def new_project(self):
        """Créer un nouveau projet"""
        dialog = QDialog()
        dialog.setWindowTitle("Nouveau projet")
        dialog.resize(400, 200)

        layout = QFormLayout()

        name_edit = QLineEdit()
        path_edit = QLineEdit()
        path_btn = QPushButton("...")
        path_btn.clicked.connect(lambda: self.select_folder(path_edit))

        path_layout = QHBoxLayout()
        path_layout.addWidget(path_edit)
        path_layout.addWidget(path_btn)

        layout.addRow("Nom du projet:", name_edit)
        layout.addRow("Dossier:", path_layout)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addRow(buttons)
        dialog.setLayout(layout)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            project_name = name_edit.text()
            project_path = path_edit.text()

            if project_name and project_path:
                # Créer le dossier du projet
                full_path = os.path.join(project_path, project_name)
                os.makedirs(full_path, exist_ok=True)

                # Initialiser le projet
                self.project_path = full_path
                self.project_data['name'] = project_name
                self.project_data['files'] = []

                # Créer le fichier projet
                self.save_project()
                self.refresh_tree()

    def open_project(self):
        """Ouvrir un projet existant"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir un projet",
            "",
            "Fichier projet (*.vfpproj);;All Files (*)"
        )

        if file_path:
            self.load_project(file_path)

    def load_project(self, file_path):
        """Charger un projet"""
        try:
            with open(file_path, 'r') as f:
                self.project_data = json.load(f)

            self.project_path = os.path.dirname(file_path)
            self.refresh_tree()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger le projet: {e}")

    def save_project(self):
        """Sauvegarder le projet"""
        if not self.project_path:
            return

        project_file = os.path.join(self.project_path, f"{self.project_data['name']}.vfpproj")
        self.project_data['modified'] = datetime.now().isoformat()

        try:
            with open(project_file, 'w') as f:
                json.dump(self.project_data, f, indent=4)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de sauvegarder: {e}")

    def refresh_tree(self):
        """Rafraîchir l'arbre des fichiers"""
        self.file_tree.clear()

        if not self.project_path:
            return

        # Nœud racine
        root = QTreeWidgetItem(self.file_tree, [self.project_data['name']])
        root.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))

        # Parcourir les fichiers
        for root_dir, dirs, files in os.walk(self.project_path):
            # Ignorer les dossiers cachés
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            rel_dir = os.path.relpath(root_dir, self.project_path)
            if rel_dir == '.':
                parent = root
            else:
                # Créer les nœuds pour les dossiers
                parent = root
                for part in rel_dir.split(os.sep):
                    # Chercher si le nœud existe déjà
                    found = None
                    for i in range(parent.childCount()):
                        if parent.child(i).text(0) == part:
                            found = parent.child(i)
                            break

                    if not found:
                        found = QTreeWidgetItem(parent, [part])
                        found.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))

                    parent = found

            # Ajouter les fichiers
            for file in sorted(files):
                if file.endswith(('.py', '.db', '.sqlite', '.json', '.csv', '.txt')):
                    file_item = QTreeWidgetItem(parent, [file])

                    # Icône selon le type
                    if file.endswith('.py'):
                        file_item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
                    elif file.endswith(('.db', '.sqlite')):
                        file_item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_DriveHDIcon))
                    else:
                        file_item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))

                    # Stocker le chemin complet
                    full_path = os.path.join(root_dir, file)
                    file_item.setData(0, Qt.ItemDataRole.UserRole, full_path)

        root.setExpanded(True)

    def open_file(self, item, column):
        """Ouvrir un fichier"""
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        if file_path and os.path.isfile(file_path):
            self.file_opened.emit(file_path)

    def show_context_menu(self, position):
        """Afficher le menu contextuel"""
        item = self.file_tree.itemAt(position)
        if not item:
            return

        menu = QMenu()

        # Actions selon le type
        file_path = item.data(0, Qt.ItemDataRole.UserRole)

        if file_path and os.path.isfile(file_path):
            open_action = QAction("Ouvrir", self)
            open_action.triggered.connect(lambda: self.file_opened.emit(file_path))
            menu.addAction(open_action)

            delete_action = QAction("Supprimer", self)
            delete_action.triggered.connect(lambda: self.delete_file(file_path))
            menu.addAction(delete_action)

        else:
            # C'est un dossier
            new_file_action = QAction("Nouveau fichier Python", self)
            new_file_action.triggered.connect(self.new_file)
            menu.addAction(new_file_action)

        menu.exec(self.file_tree.mapToGlobal(position))

    def new_file(self):
        """Créer un nouveau fichier"""
        if not self.project_path:
            return

        name, ok = QInputDialog.getText(self, "Nouveau fichier", "Nom du fichier:")
        if ok and name:
            if not name.endswith('.py'):
                name += '.py'

            file_path = os.path.join(self.project_path, name)

            # Créer le fichier avec un modèle de base
            with open(file_path, 'w') as f:
                f.write('''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module: {}
Description: 
Author: 
Date: {}
"""

import sqlite3


def main():
    """Fonction principale"""
    pass


if __name__ == '__main__':
    main()
'''.format(name[:-3], datetime.now().strftime('%Y-%m-%d')))

            self.refresh_tree()
            self.file_opened.emit(file_path)

    def delete_file(self, file_path):
        """Supprimer un fichier"""
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Supprimer {os.path.basename(file_path)} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                os.remove(file_path)
                self.refresh_tree()
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de supprimer: {e}")

    def select_folder(self, line_edit):
        """Sélectionner un dossier"""
        folder = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier")
        if folder:
            line_edit.setText(folder)