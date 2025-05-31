import sys
import os
import sqlite3
import json
import pickle
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


class ModernTheme:
    """Thème moderne pour l'interface"""

    COLORS = {
        'background': '#1e1e1e',
        'panel': '#252526',
        'border': '#3e3e42',
        'text': '#cccccc',
        'text_secondary': '#858585',
        'accent': '#007acc',
        'accent_hover': '#1a8ad4',
        'error': '#f44747',
        'success': '#4ec9b0',
        'warning': '#dcdcaa',
        'selection': '#264f78'
    }

    @staticmethod
    def get_stylesheet():
        """Retourner la feuille de style complète"""
        return f"""
        /* Global */
        QWidget {{
            background-color: {ModernTheme.COLORS['background']};
            color: {ModernTheme.COLORS['text']};
            font-family: 'Segoe UI', 'Ubuntu', sans-serif;
            font-size: 13px;
        }}

        /* Menus */
        QMenuBar {{
            background-color: {ModernTheme.COLORS['panel']};
            border-bottom: 1px solid {ModernTheme.COLORS['border']};
            padding: 2px;
        }}

        QMenuBar::item:selected {{
            background-color: {ModernTheme.COLORS['accent']};
        }}

        QMenu {{
            background-color: {ModernTheme.COLORS['panel']};
            border: 1px solid {ModernTheme.COLORS['border']};
        }}

        QMenu::item:selected {{
            background-color: {ModernTheme.COLORS['accent']};
        }}

        /* Barres d'outils */
        QToolBar {{
            background-color: {ModernTheme.COLORS['panel']};
            border-bottom: 1px solid {ModernTheme.COLORS['border']};
            padding: 4px;
            spacing: 2px;
        }}

        QToolButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 3px;
            padding: 4px 8px;
            margin: 2px;
        }}

        QToolButton:hover {{
            background-color: {ModernTheme.COLORS['accent']};
            border-color: {ModernTheme.COLORS['accent_hover']};
        }}

        /* Éditeur de texte */
        QPlainTextEdit, QTextEdit {{
            background-color: {ModernTheme.COLORS['background']};
            border: 1px solid {ModernTheme.COLORS['border']};
            selection-background-color: {ModernTheme.COLORS['selection']};
            font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 14px;
        }}

        /* Tabs */
        QTabWidget::pane {{
            border: 1px solid {ModernTheme.COLORS['border']};
            background-color: {ModernTheme.COLORS['background']};
        }}

        QTabBar::tab {{
            background-color: {ModernTheme.COLORS['panel']};
            padding: 8px 16px;
            margin-right: 2px;
            border: 1px solid {ModernTheme.COLORS['border']};
            border-bottom: none;
        }}

        QTabBar::tab:selected {{
            background-color: {ModernTheme.COLORS['background']};
            border-bottom: 1px solid {ModernTheme.COLORS['background']};
        }}

        /* Arbres et listes */
        QTreeWidget, QListWidget, QTableWidget {{
            background-color: {ModernTheme.COLORS['panel']};
            border: 1px solid {ModernTheme.COLORS['border']};
            outline: none;
        }}

        QTreeWidget::item:selected, QListWidget::item:selected {{
            background-color: {ModernTheme.COLORS['accent']};
        }}

        QTreeWidget::item:hover, QListWidget::item:hover {{
            background-color: {ModernTheme.COLORS['selection']};
        }}

        /* Boutons */
        QPushButton {{
            background-color: {ModernTheme.COLORS['accent']};
            border: none;
            border-radius: 3px;
            padding: 6px 16px;
            font-weight: 500;
        }}

        QPushButton:hover {{
            background-color: {ModernTheme.COLORS['accent_hover']};
        }}

        QPushButton:pressed {{
            background-color: {ModernTheme.COLORS['selection']};
        }}

        /* Champs de saisie */
        QLineEdit, QComboBox, QSpinBox {{
            background-color: {ModernTheme.COLORS['panel']};
            border: 1px solid {ModernTheme.COLORS['border']};
            border-radius: 3px;
            padding: 4px 8px;
        }}

        QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
            border-color: {ModernTheme.COLORS['accent']};
        }}

        /* Scrollbars */
        QScrollBar:vertical {{
            background-color: {ModernTheme.COLORS['background']};
            width: 12px;
            border: none;
        }}

        QScrollBar::handle:vertical {{
            background-color: {ModernTheme.COLORS['border']};
            border-radius: 6px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {ModernTheme.COLORS['text_secondary']};
        }}

        /* GroupBox */
        QGroupBox {{
            border: 1px solid {ModernTheme.COLORS['border']};
            border-radius: 5px;
            margin-top: 10px;
            padding-top: 10px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}

        /* Splitters */
        QSplitter::handle {{
            background-color: {ModernTheme.COLORS['border']};
        }}

        QSplitter::handle:hover {{
            background-color: {ModernTheme.COLORS['accent']};
        }}

        /* Status bar */
        QStatusBar {{
            background-color: {ModernTheme.COLORS['panel']};
            border-top: 1px solid {ModernTheme.COLORS['border']};
        }}

        /* Labels spéciaux */
        QLabel[role="header"] {{
            font-size: 16px;
            font-weight: bold;
            color: {ModernTheme.COLORS['accent']};
            padding: 8px 0;
        }}
        """


class PythonHighlighter(QSyntaxHighlighter):
    """Coloration syntaxique pour Python"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # Formats
        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor('#569cd6'))
        self.keyword_format.setFontWeight(QFont.Weight.Bold)

        self.string_format = QTextCharFormat()
        self.string_format.setForeground(QColor('#ce9178'))

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor('#6a9955'))
        self.comment_format.setFontItalic(True)

        self.function_format = QTextCharFormat()
        self.function_format.setForeground(QColor('#dcdcaa'))

        self.number_format = QTextCharFormat()
        self.number_format.setForeground(QColor('#b5cea8'))

        self.class_format = QTextCharFormat()
        self.class_format.setForeground(QColor('#4ec9b0'))

        # Mots-clés Python
        self.keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'finally', 'for', 'from',
            'global', 'if', 'import', 'in', 'is', 'lambda', 'not',
            'or', 'pass', 'raise', 'return', 'try', 'while', 'with',
            'yield', 'None', 'True', 'False', 'self'
        ]

    def highlightBlock(self, text):
        """Colorer un bloc de texte"""
        # Mots-clés
        for keyword in self.keywords:
            pattern = f'\\b{keyword}\\b'
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)

            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), self.keyword_format)

        # Chaînes entre guillemets simples
        expression = QRegularExpression("'[^']*'")
        match_iterator = expression.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)

        # Chaînes entre guillemets doubles
        expression = QRegularExpression('"[^"]*"')
        match_iterator = expression.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.string_format)

        # Commentaires
        expression = QRegularExpression('#[^\n]*')
        match_iterator = expression.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.comment_format)

        # Nombres
        expression = QRegularExpression(r'\b\d+\.?\d*\b')
        match_iterator = expression.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.number_format)

        # Fonctions
        expression = QRegularExpression(r'\b[A-Za-z_][A-Za-z0-9_]*(?=\()')
        match_iterator = expression.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), self.function_format)

        # Classes
        expression = QRegularExpression(r'\bclass\s+([A-Za-z_][A-Za-z0-9_]*)')
        match_iterator = expression.globalMatch(text)
        while match_iterator.hasNext():
            match = match_iterator.next()
            self.setFormat(match.capturedStart(1), match.capturedLength(1), self.class_format)


class LineNumberArea(QWidget):
    """Zone pour afficher les numéros de ligne"""

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class ModernCodeEditor(QPlainTextEdit):
    """Éditeur de code avec numéros de ligne et coloration syntaxique"""

    def __init__(self):
        super().__init__()

        # Zone des numéros de ligne
        self.line_number_area = LineNumberArea(self)

        # Connexions
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # Configuration
        self.update_line_number_area_width(0)
        self.highlight_current_line()

        # Coloration syntaxique
        self.highlighter = PythonHighlighter(self.document())

        # Police
        font = QFont('Consolas', 11)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)

        # Tab
        self.setTabStopDistance(QFontMetricsF(font).horizontalAdvance(' ') * 4)

    def line_number_area_width(self):
        """Calculer la largeur de la zone des numéros"""
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits + 10
        return space

    def update_line_number_area_width(self, _):
        """Mettre à jour la largeur"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        """Mettre à jour la zone"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        """Redimensionner"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(),
                                                self.line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        """Surligner la ligne courante"""
        extra_selections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            line_color = QColor(ModernTheme.COLORS['selection'])

            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        """Dessiner les numéros de ligne"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(ModernTheme.COLORS['panel']))

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        painter.setPen(QColor(ModernTheme.COLORS['text_secondary']))

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, top, self.line_number_area.width() - 5,
                                 self.fontMetrics().height(),
                                 Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1


class ModernDatabaseExplorer(QTreeWidget):
    """Explorateur de base de données moderne"""

    def __init__(self):
        super().__init__()
        self.db_connection = None

        # Configuration
        self.setHeaderHidden(True)
        self.setAnimated(True)

        # Style
        self.setStyleSheet(f"""
            QTreeWidget {{
                border: none;
                background-color: {ModernTheme.COLORS['panel']};
                padding: 4px;
            }}
            QTreeWidget::item {{
                padding: 4px;
            }}
            QTreeWidget::item:hover {{
                background-color: {ModernTheme.COLORS['selection']};
            }}
            QTreeWidget::item:selected {{
                background-color: {ModernTheme.COLORS['accent']};
            }}
        """)

        # Menu contextuel
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def connect_database(self, db_path):
        """Se connecter à une base de données"""
        try:
            self.db_connection = sqlite3.connect(db_path)
            self.refresh()
            return True
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de se connecter: {str(e)}")
            return False

    def refresh(self):
        """Rafraîchir l'arbre"""
        self.clear()

        if not self.db_connection:
            return

        # Nœud racine
        root = QTreeWidgetItem(self, ["📊 Base de données"])
        root.setExpanded(True)

        # Tables
        tables_node = QTreeWidgetItem(root, ["📁 Tables"])
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")

        for table in cursor.fetchall():
            table_item = QTreeWidgetItem(tables_node, [f"📋 {table[0]}"])

            # Ajouter les colonnes
            cursor.execute(f"PRAGMA table_info({table[0]})")
            columns = cursor.fetchall()

            for col in columns:
                col_text = f"• {col[1]} ({col[2]})"
                if col[5]:  # Primary key
                    col_text = f"🔑 {col[1]} ({col[2]})"

                QTreeWidgetItem(table_item, [col_text])

        tables_node.setExpanded(True)

    def show_context_menu(self, position):
        """Afficher le menu contextuel"""
        item = self.itemAt(position)
        if not item:
            return

        menu = QMenu(self)

        # Actions selon le type d'élément
        if item.text(0).startswith("📋"):
            table_name = item.text(0)[2:]

            view_action = QAction("👁️ Voir les données", self)
            view_action.triggered.connect(lambda: self.view_table_data(table_name))
            menu.addAction(view_action)

            export_action = QAction("💾 Exporter en CSV", self)
            export_action.triggered.connect(lambda: self.export_table_csv(table_name))
            menu.addAction(export_action)

        menu.exec(self.mapToGlobal(position))

    def view_table_data(self, table_name):
        """Voir les données d'une table"""
        # Émettre un signal ou appeler une méthode parent
        pass

    def export_table_csv(self, table_name):
        """Exporter une table en CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            f"Exporter {table_name}",
            f"{table_name}.csv",
            "CSV Files (*.csv)"
        )

        if file_path:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")

                import csv
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)

                    # En-têtes
                    writer.writerow([desc[0] for desc in cursor.description])

                    # Données
                    writer.writerows(cursor.fetchall())

                QMessageBox.information(self, "Succès", f"Table exportée vers {file_path}")

            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'export: {str(e)}")


class ModernDataBrowser(QTableWidget):
    """Navigateur de données moderne"""

    def __init__(self):
        super().__init__()

        # Configuration
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Style
        self.setStyleSheet(f"""
            QTableWidget {{
                border: none;
                gridline-color: {ModernTheme.COLORS['border']};
            }}
            QTableWidget::item {{
                padding: 4px;
            }}
            QTableWidget::item:selected {{
                background-color: {ModernTheme.COLORS['accent']};
            }}
            QHeaderView::section {{
                background-color: {ModernTheme.COLORS['panel']};
                padding: 4px;
                border: none;
                border-right: 1px solid {ModernTheme.COLORS['border']};
                border-bottom: 1px solid {ModernTheme.COLORS['border']};
            }}
        """)

        # Menu contextuel
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def load_table(self, connection, table_name):
        """Charger les données d'une table"""
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")

            # Récupérer les données
            data = cursor.fetchall()

            # Configurer le tableau
            if data:
                self.setRowCount(len(data))
                self.setColumnCount(len(data[0]))

                # En-têtes
                headers = [desc[0] for desc in cursor.description]
                self.setHorizontalHeaderLabels(headers)

                # Données
                for i, row in enumerate(data):
                    for j, value in enumerate(row):
                        item = QTableWidgetItem(str(value) if value is not None else "")
                        self.setItem(i, j, item)

                # Ajuster les colonnes
                self.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {str(e)}")

    def show_context_menu(self, position):
        """Afficher le menu contextuel"""
        menu = QMenu(self)

        copy_action = QAction("📋 Copier", self)
        copy_action.triggered.connect(self.copy_selection)
        menu.addAction(copy_action)

        export_action = QAction("💾 Exporter la sélection", self)
        export_action.triggered.connect(self.export_selection)
        menu.addAction(export_action)

        menu.exec(self.mapToGlobal(position))

    def copy_selection(self):
        """Copier la sélection dans le presse-papier"""
        selection = self.selectedRanges()
        if selection:
            # Récupérer les données sélectionnées
            text = ""
            for range in selection:
                for row in range(range.topRow(), range.bottomRow() + 1):
                    row_data = []
                    for col in range(range.leftColumn(), range.rightColumn() + 1):
                        item = self.item(row, col)
                        row_data.append(item.text() if item else "")
                    text += "\t".join(row_data) + "\n"

            QApplication.clipboard().setText(text)

    def export_selection(self):
        """Exporter la sélection"""
        # Implémenter l'export de la sélection
        pass


class OutputConsole(QTextEdit):
    """Console de sortie pour l'exécution"""

    def __init__(self):
        super().__init__()

        # Configuration
        self.setReadOnly(True)
        self.setFont(QFont('Consolas', 10))

        # Style
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {ModernTheme.COLORS['background']};
                border: none;
                padding: 8px;
            }}
        """)

    def write_output(self, text, output_type='info'):
        """Écrire dans la console avec couleur"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        # Format selon le type
        format = QTextCharFormat()

        if output_type == 'error':
            format.setForeground(QColor(ModernTheme.COLORS['error']))
        elif output_type == 'success':
            format.setForeground(QColor(ModernTheme.COLORS['success']))
        elif output_type == 'warning':
            format.setForeground(QColor(ModernTheme.COLORS['warning']))
        else:
            format.setForeground(QColor(ModernTheme.COLORS['text']))

        cursor.insertText(text + '\n', format)

        # Scroll vers le bas
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())


# Suite du code avec SQLQueryBuilder, FormDesigner, etc...
class SQLQueryBuilder(QDialog):
    """Générateur de requêtes SQL visuel"""

    def __init__(self, db_connection, parent=None):
        super().__init__(parent)
        self.db_connection = db_connection
        self.setWindowTitle("Générateur de requêtes SQL")
        self.setModal(True)
        self.resize(800, 600)

        self.setStyleSheet(ModernTheme.get_stylesheet())

        self.init_ui()
        self.load_tables()

    def init_ui(self):
        layout = QVBoxLayout()

        # Section SELECT
        select_group = QGroupBox("SELECT - Colonnes à afficher")
        select_layout = QVBoxLayout()

        self.table_combo = QComboBox()
        self.table_combo.currentTextChanged.connect(self.load_columns)

        self.columns_list = QListWidget()
        self.columns_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)

        select_layout.addWidget(QLabel("Table:"))
        select_layout.addWidget(self.table_combo)
        select_layout.addWidget(QLabel("Colonnes:"))
        select_layout.addWidget(self.columns_list)
        select_group.setLayout(select_layout)

        # Section WHERE
        where_group = QGroupBox("WHERE - Conditions")
        where_layout = QVBoxLayout()

        self.conditions_table = QTableWidget(0, 4)
        self.conditions_table.setHorizontalHeaderLabels(["Colonne", "Opérateur", "Valeur", "ET/OU"])

        add_condition_btn = QPushButton("+ Ajouter une condition")
        add_condition_btn.clicked.connect(self.add_condition)

        where_layout.addWidget(self.conditions_table)
        where_layout.addWidget(add_condition_btn)
        where_group.setLayout(where_layout)

        # Section ORDER BY
        order_group = QGroupBox("ORDER BY - Tri")
        order_layout = QHBoxLayout()

        self.order_column = QComboBox()
        self.order_direction = QComboBox()
        self.order_direction.addItems(["ASC", "DESC"])

        order_layout.addWidget(QLabel("Colonne:"))
        order_layout.addWidget(self.order_column)
        order_layout.addWidget(QLabel("Direction:"))
        order_layout.addWidget(self.order_direction)
        order_group.setLayout(order_layout)

        # Section LIMIT
        limit_group = QGroupBox("LIMIT - Nombre de résultats")
        limit_layout = QHBoxLayout()

        self.limit_spin = QSpinBox()
        self.limit_spin.setMaximum(10000)
        self.limit_spin.setValue(100)

        limit_layout.addWidget(QLabel("Limiter à:"))
        limit_layout.addWidget(self.limit_spin)
        limit_layout.addWidget(QLabel("lignes"))
        limit_layout.addStretch()
        limit_group.setLayout(limit_layout)

        # Aperçu SQL
        preview_group = QGroupBox("Aperçu de la requête SQL")
        preview_layout = QVBoxLayout()

        self.sql_preview = QTextEdit()
        self.sql_preview.setReadOnly(True)
        self.sql_preview.setMaximumHeight(100)
        self.sql_preview.setFont(QFont('Consolas', 10))

        preview_layout.addWidget(self.sql_preview)
        preview_group.setLayout(preview_layout)

        # Boutons
        buttons_layout = QHBoxLayout()

        self.test_btn = QPushButton("Tester la requête")
        self.test_btn.clicked.connect(self.test_query)

        self.insert_btn = QPushButton("Insérer dans l'éditeur")
        self.insert_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(self.test_btn)
        buttons_layout.addWidget(self.insert_btn)
        buttons_layout.addWidget(cancel_btn)

        # Assembler le layout
        layout.addWidget(select_group)
        layout.addWidget(where_group)
        layout.addWidget(order_group)
        layout.addWidget(limit_group)
        layout.addWidget(preview_group)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        # Connecter les signaux pour mettre à jour l'aperçu
        self.columns_list.itemSelectionChanged.connect(self.update_preview)
        self.order_column.currentTextChanged.connect(self.update_preview)
        self.order_direction.currentTextChanged.connect(self.update_preview)
        self.limit_spin.valueChanged.connect(self.update_preview)

    def load_tables(self):
        """Charger la liste des tables"""
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            self.table_combo.addItem(table[0])

    def load_columns(self, table_name):
        """Charger les colonnes d'une table"""
        if not table_name:
            return

        self.columns_list.clear()
        self.order_column.clear()

        cursor = self.db_connection.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        self.columns_list.addItem("*")
        self.order_column.addItem("")

        for col in columns:
            self.columns_list.addItem(col[1])
            self.order_column.addItem(col[1])

        self.update_preview()

    def add_condition(self):
        """Ajouter une ligne de condition"""
        row = self.conditions_table.rowCount()
        self.conditions_table.insertRow(row)

        # Colonne
        col_combo = QComboBox()
        cursor = self.db_connection.cursor()
        table_name = self.table_combo.currentText()
        if table_name:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            for col in columns:
                col_combo.addItem(col[1])

        # Opérateur
        op_combo = QComboBox()
        op_combo.addItems(["=", "!=", ">", "<", ">=", "<=", "LIKE", "IN", "NOT IN"])

        # Valeur
        value_edit = QLineEdit()

        # ET/OU
        and_or_combo = QComboBox()
        and_or_combo.addItems(["ET", "OU"])

        self.conditions_table.setCellWidget(row, 0, col_combo)
        self.conditions_table.setCellWidget(row, 1, op_combo)
        self.conditions_table.setCellWidget(row, 2, value_edit)
        self.conditions_table.setCellWidget(row, 3, and_or_combo)

        # Connecter pour mettre à jour l'aperçu
        col_combo.currentTextChanged.connect(self.update_preview)
        op_combo.currentTextChanged.connect(self.update_preview)
        value_edit.textChanged.connect(self.update_preview)
        and_or_combo.currentTextChanged.connect(self.update_preview)

    def update_preview(self):
        """Mettre à jour l'aperçu SQL"""
        table = self.table_combo.currentText()
        if not table:
            return

        # SELECT
        selected_items = self.columns_list.selectedItems()
        if selected_items:
            columns = ", ".join([item.text() for item in selected_items])
        else:
            columns = "*"

        sql = f"SELECT {columns}\nFROM {table}"

        # WHERE
        conditions = []
        for row in range(self.conditions_table.rowCount()):
            col_widget = self.conditions_table.cellWidget(row, 0)
            op_widget = self.conditions_table.cellWidget(row, 1)
            val_widget = self.conditions_table.cellWidget(row, 2)
            and_or_widget = self.conditions_table.cellWidget(row, 3)

            if col_widget and op_widget and val_widget:
                col = col_widget.currentText()
                op = op_widget.currentText()
                val = val_widget.text()

                if col and val:
                    # Ajouter des guillemets pour les chaînes
                    if op in ["LIKE", "=", "!="] and not val.isdigit():
                        val = f"'{val}'"

                    condition = f"{col} {op} {val}"

                    if row > 0 and and_or_widget:
                        and_or = "AND" if and_or_widget.currentText() == "ET" else "OR"
                        condition = f"{and_or} {condition}"

                    conditions.append(condition)

        if conditions:
            sql += "\nWHERE " + " ".join(conditions)

        # ORDER BY
        order_col = self.order_column.currentText()
        if order_col:
            order_dir = self.order_direction.currentText()
            sql += f"\nORDER BY {order_col} {order_dir}"

        # LIMIT
        limit = self.limit_spin.value()
        if limit > 0:
            sql += f"\nLIMIT {limit}"

        self.sql_preview.setText(sql)

    def test_query(self):
        """Tester la requête"""
        sql = self.sql_preview.toPlainText()
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()

            msg = f"Requête exécutée avec succès!\n{len(results)} lignes retournées."
            QMessageBox.information(self, "Test réussi", msg)

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur dans la requête:\n{str(e)}")

    def get_sql(self):
        """Obtenir la requête SQL générée"""
        return self.sql_preview.toPlainText()


class FormDesigner(QMainWindow):
    """Concepteur de formulaires drag & drop"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Concepteur de formulaires")
        self.resize(1000, 700)

        self.setStyleSheet(ModernTheme.get_stylesheet())

        self.widgets = []  # Liste des widgets du formulaire
        self.selected_widget = None

        self.init_ui()

    def init_ui(self):
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()

        # Panneau de widgets disponibles
        self.create_widgets_panel()

        # Zone de conception
        self.design_area = FormDesignArea()
        self.design_area.widget_selected.connect(self.on_widget_selected)

        # Panneau de propriétés
        self.create_properties_panel()

        # Assembler
        layout.addWidget(self.widgets_panel, 1)
        layout.addWidget(self.design_area, 3)
        layout.addWidget(self.properties_panel, 1)

        central.setLayout(layout)

        # Barre d'outils
        self.create_toolbar()

    def create_widgets_panel(self):
        """Créer le panneau des widgets disponibles"""
        self.widgets_panel = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Widgets disponibles")
        label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(label)

        # Liste des widgets
        widgets_list = QListWidget()
        widgets_list.setDragEnabled(True)

        widget_types = [
            ("Label", "QLabel"),
            ("Bouton", "QPushButton"),
            ("Champ texte", "QLineEdit"),
            ("Zone de texte", "QTextEdit"),
            ("Case à cocher", "QCheckBox"),
            ("Bouton radio", "QRadioButton"),
            ("Liste déroulante", "QComboBox"),
            ("Sélecteur de date", "QDateEdit"),
            ("Tableau", "QTableWidget"),
            ("Groupe", "QGroupBox")
        ]

        for display_name, class_name in widget_types:
            item = QListWidgetItem(display_name)
            item.setData(Qt.ItemDataRole.UserRole, class_name)
            widgets_list.addItem(item)

        layout.addWidget(widgets_list)
        layout.addStretch()

        self.widgets_panel.setLayout(layout)

    def create_properties_panel(self):
        """Créer le panneau de propriétés"""
        self.properties_panel = QWidget()
        layout = QVBoxLayout()

        label = QLabel("Propriétés")
        label.setStyleSheet("font-weight: bold; padding: 5px;")
        layout.addWidget(label)

        # Table des propriétés
        self.properties_table = QTableWidget()
        self.properties_table.setColumnCount(2)
        self.properties_table.setHorizontalHeaderLabels(["Propriété", "Valeur"])
        self.properties_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(self.properties_table)

        self.properties_panel.setLayout(layout)

    def create_toolbar(self):
        """Créer la barre d'outils"""
        toolbar = self.addToolBar("Outils")

        # Actions
        generate_action = QAction("Générer le code", self)
        generate_action.triggered.connect(self.generate_code)

        preview_action = QAction("Aperçu", self)
        preview_action.triggered.connect(self.preview_form)

        clear_action = QAction("Effacer tout", self)
        clear_action.triggered.connect(self.clear_form)

        toolbar.addAction(generate_action)
        toolbar.addAction(preview_action)
        toolbar.addSeparator()
        toolbar.addAction(clear_action)

    def on_widget_selected(self, widget):
        """Quand un widget est sélectionné"""
        self.selected_widget = widget
        self.update_properties()

    def update_properties(self):
        """Mettre à jour le panneau de propriétés"""
        self.properties_table.setRowCount(0)

        if not self.selected_widget:
            return

        # Propriétés communes
        properties = [
            ("Nom", self.selected_widget.objectName()),
            ("Texte", self.selected_widget.property("text") or ""),
            ("Position X", str(self.selected_widget.x())),
            ("Position Y", str(self.selected_widget.y())),
            ("Largeur", str(self.selected_widget.width())),
            ("Hauteur", str(self.selected_widget.height()))
        ]

        for prop_name, prop_value in properties:
            row = self.properties_table.rowCount()
            self.properties_table.insertRow(row)
            self.properties_table.setItem(row, 0, QTableWidgetItem(prop_name))

            value_item = QTableWidgetItem(str(prop_value))
            self.properties_table.setItem(row, 1, value_item)

    def generate_code(self):
        """Générer le code Python du formulaire"""
        code = """# Formulaire généré automatiquement
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class GeneratedForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulaire généré")
        self.resize(800, 600)

        # Widgets
"""

        for widget in self.design_area.form_widgets:
            widget_type = widget.__class__.__name__
            widget_name = widget.objectName() or f"widget_{id(widget)}"

            code += f"        self.{widget_name} = {widget_type}(self)\n"
            code += f"        self.{widget_name}.setGeometry({widget.x()}, {widget.y()}, {widget.width()}, {widget.height()})\n"

            if hasattr(widget, 'text') and widget.text():
                code += f"        self.{widget_name}.setText('{widget.text()}')\n"

            code += "\n"

        code += """
if __name__ == '__main__':
    app = QApplication([])
    form = GeneratedForm()
    form.show()
    app.exec()
"""

        # Afficher le code
        dialog = QDialog(self)
        dialog.setWindowTitle("Code généré")
        dialog.resize(600, 400)

        layout = QVBoxLayout()

        code_edit = QTextEdit()
        code_edit.setPlainText(code)
        code_edit.setFont(QFont('Consolas', 10))

        copy_btn = QPushButton("Copier dans le presse-papier")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(code))

        layout.addWidget(code_edit)
        layout.addWidget(copy_btn)

        dialog.setLayout(layout)
        dialog.exec()

    def preview_form(self):
        """Aperçu du formulaire"""
        preview = QDialog(self)
        preview.setWindowTitle("Aperçu du formulaire")
        preview.resize(self.design_area.width(), self.design_area.height())

        # Copier les widgets
        for widget in self.design_area.form_widgets:
            widget_type = type(widget)
            new_widget = widget_type(preview)
            new_widget.setGeometry(widget.geometry())

            if hasattr(widget, 'text'):
                new_widget.setText(widget.text())

        preview.exec()

    def clear_form(self):
        """Effacer tous les widgets"""
        reply = QMessageBox.question(self, "Confirmation",
                                     "Effacer tous les widgets?",
                                     QMessageBox.StandardButton.Yes |
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.design_area.clear_widgets()


class FormDesignArea(QWidget):
    """Zone de conception pour le formulaire"""
    widget_selected = pyqtSignal(QWidget)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            FormDesignArea {
                background-color: #f0f0f0;
                border: 2px dashed #999;
            }
        """)

        self.form_widgets = []
        self.selected_widget = None

    def dragEnterEvent(self, event):
        """Accepter le drag"""
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Gérer le drop"""
        widget_class = event.mimeData().text()
        pos = event.position().toPoint()

        # Créer le widget
        widget = self.create_widget(widget_class, pos)
        if widget:
            widget.show()
            self.form_widgets.append(widget)

    def create_widget(self, class_name, pos):
        """Créer un widget à partir du nom de classe"""
        widget_map = {
            "QLabel": lambda: QLabel("Label", self),
            "QPushButton": lambda: QPushButton("Bouton", self),
            "QLineEdit": lambda: QLineEdit(self),
            "QTextEdit": lambda: QTextEdit(self),
            "QCheckBox": lambda: QCheckBox("Case à cocher", self),
            "QRadioButton": lambda: QRadioButton("Option", self),
            "QComboBox": lambda: QComboBox(self),
            "QDateEdit": lambda: QDateEdit(self),
            "QTableWidget": lambda: QTableWidget(3, 3, self),
            "QGroupBox": lambda: QGroupBox("Groupe", self)
        }

        if class_name in widget_map:
            widget = widget_map[class_name]()
            widget.move(pos)
            widget.resize(150, 30)  # Taille par défaut

            # Rendre le widget déplaçable
            widget.installEventFilter(self)

            return widget

        return None

    def eventFilter(self, obj, event):
        """Gérer les événements des widgets"""
        if obj in self.form_widgets:
            if event.type() == QEvent.Type.MouseButtonPress:
                self.selected_widget = obj
                self.widget_selected.emit(obj)
                obj.raise_()

                # Stocker la position de départ
                self.drag_start_pos = event.position().toPoint()

            elif event.type() == QEvent.Type.MouseMove:
                if event.buttons() == Qt.MouseButton.LeftButton and self.selected_widget == obj:
                    # Déplacer le widget
                    new_pos = obj.pos() + event.position().toPoint() - self.drag_start_pos
                    obj.move(new_pos)

        return super().eventFilter(obj, event)

    def clear_widgets(self):
        """Effacer tous les widgets"""
        for widget in self.form_widgets:
            widget.deleteLater()
        self.form_widgets.clear()
        self.selected_widget = None


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
        QApplication.clipboard().setText(self.code_preview.toPlainText())

    def get_selected_code(self):
        """Obtenir le code sélectionné"""
        return self.code_preview.toPlainText()


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

    # Hériter des autres méthodes de base...
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

            import io
            import contextlib

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
                import traceback
                self.console.write_output(traceback.format_exc(), 'error')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    # Utiliser l'IDE complet
    ide = EnhancedVFPIDE()
    ide.show()

    sys.exit(app.exec())