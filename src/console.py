# console.py
"""Module pour la console de sortie"""

from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QTextCursor

from theme import ModernTheme


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