# editor.py
"""Module pour l'éditeur de code avec coloration syntaxique"""

from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PyQt6.QtCore import Qt, QRect, QSize, pyqtSignal, QRegularExpression
from PyQt6.QtGui import (QColor, QTextCharFormat, QFont, QPainter,
                         QSyntaxHighlighter, QTextCursor, QFontMetricsF,
                         QTextFormat)

from theme import ModernTheme


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