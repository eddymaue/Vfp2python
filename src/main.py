# main.py
"""PyFoxPro IDE - Fichier principal"""

import sys
import os
import sqlite3
import io
import contextlib
import traceback

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                           QHBoxLayout, QSplitter, QTabWidget, QLabel,
                           QToolBar, QFileDialog, QMessageBox, QAction, QStyle)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

# Import des modules
from theme import ModernTheme
from editor import ModernCodeEditor
from database import ModernDatabaseExplorer, ModernDataBrowser
from console import OutputConsole
from sql_builder import SQLQueryBuilder
from form_designer import FormDesigner
from templates import CodeTemplates
from project import ProjectManager


class EnhancedVFPIDE(QMainWindow):
    """IDE complet avec toutes les fonctionnalités"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyFoxPro IDE - Édition Complète")
        self.setGeometry(100, 100, 1600, 900)

        # Appliquer le thème
        self.setStyleSheet(ModernTheme.get_stylesheet())

        # Initialiser l'IDE de base
        self.init_base_ui()

        # Ajouter les nouvelles fonctionnalités
        self.add_project_manager()
        self.add_menu_items()

    def init_base_ui(self):
        """Initialiser l'interface de base"""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Créer les menus et barres d'outils
        self.create_menus()
        self.create_toolbar()

        # Splitter principal
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Explorateur de base de données
        explorer_widget = QWidget()
        explorer_layout = QVBoxLayout()
        explorer_layout.setContentsMargins(8, 8, 8, 8)

        explorer_label = QLabel("EXPLORATEUR DE DONNÉES")
        explorer_label.setStyleSheet(f"""
            font-size: 11px;
            font-weight: bold;
            color: {ModernTheme.COLORS['text_secondary']};
            padding: 4px 0;
        """)

        self.db_explorer = ModernDatabaseExplorer()
        self.db_explorer.itemDoubleClicked.connect(self.on_table_double_click)

        explorer_layout.addWidget(explorer_label)
        explorer_layout.addWidget(self.db_explorer)
        explorer_widget.setLayout(explorer_layout)

        # Zone d'édition centrale
        editor_splitter = QSplitter(Qt.Orientation.Vertical)

        # Tabs pour les éditeurs
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.setMovable(True)
        self.editor_tabs.tabCloseRequested.connect(self.close_tab)

        # Ajouter un premier éditeur
        self.add_new_editor()

        # Zone de sortie
        output_widget = QWidget()
        output_layout = QVBoxLayout()
        output_layout.setContentsMargins(0, 0, 0, 0)

        self.output_tabs = QTabWidget()

        self.console = OutputConsole()
        self.output_tabs.addTab(self.console, "SORTIE")

        self.data_browser = ModernDataBrowser()
        self.output_tabs.addTab(self.data_browser, "DONNÉES")

        output_layout.addWidget(self.output_tabs)
        output_widget.setLayout(output_layout)

        editor_splitter.addWidget(self.editor_tabs)
        editor_splitter.addWidget(output_widget)
        editor_splitter.setSizes([600, 200])

        self.main_splitter.addWidget(explorer_widget)
        self.main_splitter.addWidget(editor_splitter)
        self.main_splitter.setSizes([250, 1150])

        main_layout.addWidget(self.main_splitter)
        central_widget.setLayout(main_layout)

        self.create_status_bar()

    def add_project_manager(self):
        """Ajouter le gestionnaire de projets"""
        self.project_manager = ProjectManager()
        self.project_manager.file_opened.connect(self.open_file_from_path)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_manager)

    def add_menu_items(self):
        """Ajouter les nouveaux éléments de menu"""
        # Menu Outils
        tools_menu = self.menuBar().addMenu('Outils')

        sql_builder_action = QAction('Générateur de requêtes SQL', self)
        sql_builder_action.triggered.connect(self.open_sql_builder)
        tools_menu.addAction(sql_builder_action)

        form_designer_action = QAction('Concepteur de formulaires', self)
        form_designer_action.triggered.connect(self.open_form_designer)
        tools_menu.addAction(form_designer_action)

        templates_action = QAction('Modèles de code', self)
        templates_action.triggered.connect(self.open_templates)
        tools_menu.addAction(templates_action)

        # Ajouter à la barre d'outils
        toolbar = self.findChild(QToolBar)
        if toolbar:
            toolbar.addSeparator()

            sql_btn = QAction('🔍 SQL', self)
            sql_btn.setToolTip('Générateur de requêtes SQL')
            sql_btn.triggered.connect(self.open_sql_builder)
            toolbar.addAction(sql_btn)

            form_btn = QAction('📋 Forms', self)
            form_btn.setToolTip('Concepteur de formulaires')
            form_btn.triggered.connect(self.open_form_designer)
            toolbar.addAction(form_btn)

            template_btn = QAction('📝 Modèles', self)
            template_btn.setToolTip('Modèles de code')
            template_btn.triggered.connect(self.open_templates)
            toolbar.addAction(template_btn)

    def open_sql_builder(self):
        """Ouvrir le générateur SQL"""
        if self.db_explorer.db_connection:
            dialog = SQLQueryBuilder(self.db_explorer.db_connection, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Insérer le SQL dans l'éditeur actuel
                current_editor = self.editor_tabs.currentWidget()
                if isinstance(current_editor, ModernCodeEditor):
                    cursor = current_editor.textCursor()
                    cursor.insertText(dialog.get_sql())
        else:
            QMessageBox.warning(self, "Attention", "Veuillez d'abord connecter une base de données")

    def open_form_designer(self):
        """Ouvrir le concepteur de formulaires"""
        designer = FormDesigner(self)
        designer.show()

    def open_templates(self):
        """Ouvrir les modèles de code"""
        dialog = CodeTemplates(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Insérer le code dans l'éditeur
            current_editor = self.editor_tabs.currentWidget()
            if isinstance(current_editor, ModernCodeEditor):
                cursor = current_editor.textCursor()
                cursor.insertText(dialog.get_selected_code())

    def open_file_from_path(self, file_path):
        """Ouvrir un fichier depuis un chemin"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            filename = os.path.basename(file_path)

            # Vérifier si le fichier est déjà ouvert
            for i in range(self.editor_tabs.count()):
                if self.editor_tabs.tabText(i) == filename:
                    self.editor_tabs.setCurrentIndex(i)
                    return

            # Créer un nouvel onglet
            self.add_new_editor(filename, content)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir le fichier: {e}")

    def create_menus(self):
        """Créer les menus"""
        menubar = self.menuBar()

        # Menu Fichier
        file_menu = menubar.addMenu('Fichier')

        new_action = QAction('Nouveau fichier', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.add_new_editor)
        file_menu.addAction(new_action)

        open_action = QAction('Ouvrir...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        save_action = QAction('Enregistrer', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()

        exit_action = QAction('Quitter', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Base de données
        db_menu = menubar.addMenu('Base de données')

        connect_db = QAction('Connecter...', self)
        connect_db.triggered.connect(self.connect_database)
        db_menu.addAction(connect_db)

        # Menu Exécuter
        run_menu = menubar.addMenu('Exécuter')

        run_action = QAction('Exécuter le script', self)
        run_action.setShortcut('F5')
        run_action.triggered.connect(self.run_code)
        run_menu.addAction(run_action)

    def create_toolbar(self):
        """Créer la barre d'outils"""
        toolbar = self.addToolBar('Principal')
        toolbar.setMovable(False)

        # Actions de base
        new_action = QAction('📄 Nouveau', self)
        new_action.triggered.connect(self.add_new_editor)

        open_action = QAction('📂 Ouvrir', self)
        open_action.triggered.connect(self.open_file)

        save_action = QAction('💾 Enregistrer', self)
        save_action.triggered.connect(self.save_file)

        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addSeparator()

        run_action = QAction('▶️ Exécuter', self)
        run_action.triggered.connect(self.run_code)

        toolbar.addAction(run_action)

    def create_status_bar(self):
        """Créer la barre de statut"""
        status = self.statusBar()
        status.setStyleSheet(f"""
            QStatusBar {{
                background-color: {ModernTheme.COLORS['accent']};
                color: white;
                font-size: 12px;
            }}
        """)

        self.status_db = QLabel(' 🗄️ Aucune base connectée ')
        self.status_line = QLabel(' Ln 1, Col 1 ')

        status.addWidget(self.status_db)
        status.addPermanentWidget(self.status_line)

    def add_new_editor(self, filename="sans_titre.py", content=""):
        """Ajouter un nouvel éditeur"""
        editor = ModernCodeEditor()
        if content:
            editor.setPlainText(content)

        index = self.editor_tabs.addTab(editor, filename)
        self.editor_tabs.setCurrentIndex(index)

        editor.cursorPositionChanged.connect(self.update_cursor_position)

    def close_tab(self, index):
        """Fermer un onglet"""
        if self.editor_tabs.count() > 1:
            self.editor_tabs.removeTab(index)

    def open_file(self):
        """Ouvrir un fichier"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir un fichier",
            "",
            "Python Files (*.py);;All Files (*)"
        )

        if file_path:
            self.open_file_from_path(file_path)

    def save_file(self):
        """Enregistrer le fichier courant"""
        current_editor = self.editor_tabs.currentWidget()
        if isinstance(current_editor, ModernCodeEditor):
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Enregistrer le fichier",
                "",
                "Python Files (*.py);;All Files (*)"
            )

            if file_path:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(current_editor.toPlainText())

                    filename = os.path.basename(file_path)
                    self.editor_tabs.setTabText(self.editor_tabs.currentIndex(), filename)

                except Exception as e:
                    QMessageBox.critical(self, "Erreur", f"Impossible d'enregistrer: {e}")

    def connect_database(self):
        """Connecter une base de données"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner une base de données",
            "",
            "SQLite Database (*.db *.sqlite);;All Files (*)"
        )

        if file_path:
            if self.db_explorer.connect_database(file_path):
                self.console.write_output(f"✓ Base de données connectée: {file_path}", 'success')
                self.status_db.setText(f' 🗄️ {os.path.basename(file_path)} ')

    def on_table_double_click(self, item, column):
        """Double-clic sur une table"""
        if item.parent() and item.parent().text(0) == "📁 Tables":
            table_name = item.text(0)[2:]
            if self.db_explorer.db_connection:
                self.data_browser.load_table(self.db_explorer.db_connection, table_name)
                self.output_tabs.setCurrentWidget(self.data_browser)
                self.console.write_output(f"✓ Table '{table_name}' chargée", 'success')

    def update_cursor_position(self):
        """Mettre à jour la position du curseur"""
        editor = self.sender()
        if isinstance(editor, ModernCodeEditor):
            cursor = editor.textCursor()
            line = cursor.blockNumber() + 1
            col = cursor.columnNumber() + 1
            self.status_line.setText(f' Ln {line}, Col {col} ')

    def run_code(self):
        """Exécuter le code Python"""
        current_editor = self.editor_tabs.currentWidget()
        if isinstance(current_editor, ModernCodeEditor):
            code = current_editor.toPlainText()

            self.output_tabs.setCurrentWidget(self.console)
            self.console.write_output("▶ Exécution du script...", 'info')

            output_buffer = io.StringIO()

            globals_dict = {
                'db': self.db_explorer.db_connection,
                'sqlite3': sqlite3,
                '__name__': '__main__'
            }

            try:
                with contextlib.redirect_stdout(output_buffer):
                    exec(code, globals_dict)

                output = output_buffer.getvalue()
                if output:
                    self.console.write_output(output, 'info')
                self.console.write_output("✓ Script exécuté avec succès", 'success')

            except Exception as e:
                self.console.write_output(f"✗ Erreur: {str(e)}", 'error')
                self.console.write_output(traceback.format_exc(), 'error')


def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Utiliser l'IDE complet
    ide = EnhancedVFPIDE()
    ide.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()