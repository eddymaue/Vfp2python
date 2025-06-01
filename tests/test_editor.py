# tests/test_editor.py
"""Tests pour le module editor"""

import sys
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Ajouter le dossier src au path
sys.path.insert(0, '../src')

from editor import ModernCodeEditor, PythonHighlighter


@pytest.fixture(scope='session')
def qapp():
    """Créer une instance QApplication pour les tests"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
    app.quit()


class TestModernCodeEditor:
    """Tests pour ModernCodeEditor"""
    
    def test_editor_creation(self, qapp):
        """Test de création de l'éditeur"""
        editor = ModernCodeEditor()
        assert editor is not None
        assert editor.isReadOnly() is False
        
    def test_editor_set_text(self, qapp):
        """Test d'insertion de texte"""
        editor = ModernCodeEditor()
        test_text = "print('Hello, World!')"
        editor.setPlainText(test_text)
        assert editor.toPlainText() == test_text
        
    def test_line_numbers(self, qapp):
        """Test des numéros de ligne"""
        editor = ModernCodeEditor()
        editor.setPlainText("Line 1\nLine 2\nLine 3")
        assert editor.blockCount() == 3
        
    def test_syntax_highlighter(self, qapp):
        """Test du highlighter"""
        editor = ModernCodeEditor()
        assert editor.highlighter is not None
        assert isinstance(editor.highlighter, PythonHighlighter)


class TestPythonHighlighter:
    """Tests pour PythonHighlighter"""
    
    def test_keywords(self):
        """Test de la liste des mots-clés"""
        highlighter = PythonHighlighter()
        assert 'def' in highlighter.keywords
        assert 'class' in highlighter.keywords
        assert 'if' in highlighter.keywords
        assert 'for' in highlighter.keywords