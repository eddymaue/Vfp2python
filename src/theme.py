# theme.py
"""Module pour le thème et les styles de l'interface"""

from PyQt6.QtGui import QColor


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