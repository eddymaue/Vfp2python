# fix_all_pyqt6.py
"""Script complet pour corriger tous les problèmes PyQt6"""

import os
import re

def fix_imports(content):
    """Corriger les imports PyQt6"""
    
    # Déplacer QAction de QtWidgets vers QtGui
    content = re.sub(
        r'from PyQt6\.QtWidgets import (.*?)QAction(.*?)(?=\n)',
        lambda m: f'from PyQt6.QtWidgets import {m.group(1).replace("QAction,", "").replace(", QAction", "").replace("QAction", "")}{m.group(2)}',
        content
    )
    
    # Ajouter QAction à QtGui si nécessaire
    if 'QAction' in content and 'from PyQt6.QtGui import' in content:
        content = re.sub(
            r'(from PyQt6\.QtGui import .*?)(\n)',
            lambda m: m.group(1) + (', QAction' if 'QAction' not in m.group(1) else '') + m.group(2),
            content
        )
    elif 'QAction' in content:
        # Ajouter l'import QtGui si pas présent
        content = re.sub(
            r'(from PyQt6\.QtCore import.*?\n)',
            r'\1from PyQt6.QtGui import QAction\n',
            content
        )
    
    # Déplacer QRegularExpression de QtGui vers QtCore
    content = re.sub(
        r'from PyQt6\.QtGui import (.*?)QRegularExpression(.*?)(?=\n)',
        lambda m: f'from PyQt6.QtGui import {m.group(1).replace("QRegularExpression,", "").replace(", QRegularExpression", "").replace("QRegularExpression", "")}{m.group(2)}',
        content
    )
    
    # Ajouter QRegularExpression à QtCore si nécessaire
    if 'QRegularExpression' in content and 'from PyQt6.QtCore import' in content:
        content = re.sub(
            r'(from PyQt6\.QtCore import .*?)(\n)',
            lambda m: m.group(1) + (', QRegularExpression' if 'QRegularExpression' not in m.group(1) else '') + m.group(2),
            content
        )
    
    return content

def fix_enums(content):
    """Corriger tous les enums PyQt6"""
    
    replacements = {
        # Qt enums
        r'\bQt\.AlignLeft\b': 'Qt.AlignmentFlag.AlignLeft',
        r'\bQt\.AlignRight\b': 'Qt.AlignmentFlag.AlignRight',
        r'\bQt\.AlignCenter\b': 'Qt.AlignmentFlag.AlignCenter',
        r'\bQt\.AlignTop\b': 'Qt.AlignmentFlag.AlignTop',
        r'\bQt\.AlignBottom\b': 'Qt.AlignmentFlag.AlignBottom',
        r'\bQt\.AlignHCenter\b': 'Qt.AlignmentFlag.AlignHCenter',
        r'\bQt\.AlignVCenter\b': 'Qt.AlignmentFlag.AlignVCenter',
        
        # Mouse buttons
        r'\bQt\.LeftButton\b': 'Qt.MouseButton.LeftButton',
        r'\bQt\.RightButton\b': 'Qt.MouseButton.RightButton',
        r'\bQt\.MiddleButton\b': 'Qt.MouseButton.MiddleButton',
        
        # Keyboard modifiers
        r'\bQt\.ShiftModifier\b': 'Qt.KeyboardModifier.ShiftModifier',
        r'\bQt\.ControlModifier\b': 'Qt.KeyboardModifier.ControlModifier',
        r'\bQt\.AltModifier\b': 'Qt.KeyboardModifier.AltModifier',
        
        # Dialog buttons
        r'\bQMessageBox\.Yes\b': 'QMessageBox.StandardButton.Yes',
        r'\bQMessageBox\.No\b': 'QMessageBox.StandardButton.No',
        r'\bQMessageBox\.Ok\b': 'QMessageBox.StandardButton.Ok',
        r'\bQMessageBox\.Cancel\b': 'QMessageBox.StandardButton.Cancel',
        
        # DialogButtonBox
        r'\bQDialogButtonBox\.Ok\b': 'QDialogButtonBox.StandardButton.Ok',
        r'\bQDialogButtonBox\.Cancel\b': 'QDialogButtonBox.StandardButton.Cancel',
        
        # Dialog codes
        r'\bQDialog\.Accepted\b': 'QDialog.DialogCode.Accepted',
        r'\bQDialog\.Rejected\b': 'QDialog.DialogCode.Rejected',
        
        # Orientations
        r'\bQt\.Horizontal\b': 'Qt.Orientation.Horizontal',
        r'\bQt\.Vertical\b': 'Qt.Orientation.Vertical',
        
        # Context menu policy
        r'\bQt\.CustomContextMenu\b': 'Qt.ContextMenuPolicy.CustomContextMenu',
        
        # Item data role
        r'\bQt\.UserRole\b': 'Qt.ItemDataRole.UserRole',
        
        # Selection modes
        r'\bQListWidget\.MultiSelection\b': 'QListWidget.SelectionMode.MultiSelection',
        r'\bQTableWidget\.SelectRows\b': 'QTableWidget.SelectionBehavior.SelectRows',
        
        # Event types
        r'\bQEvent\.MouseButtonPress\b': 'QEvent.Type.MouseButtonPress',
        r'\bQEvent\.MouseMove\b': 'QEvent.Type.MouseMove',
        
        # Text format
        r'\bQTextFormat\.FullWidthSelection\b': 'QTextFormat.Property.FullWidthSelection',
        
        # Cursor move operation
        r'\bQTextCursor\.End\b': 'QTextCursor.MoveOperation.End',
        
        # Font weight
        r'\bQFont\.Bold\b': 'QFont.Weight.Bold',
        
        # Style hints
        r'\bQFont\.Monospace\b': 'QFont.StyleHint.Monospace',
        
        # exec_ to exec
        r'\.exec_\(\)': '.exec()',
    }
    
    for old, new in replacements.items():
        content = re.sub(old, new, content)
    
    return content

def fix_file(filepath):
    """Corriger un fichier Python"""
    print(f"Vérification de {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Corriger les imports
        content = fix_imports(content)
        
        # Corriger les enums
        content = fix_enums(content)
        
        # Sauvegarder si modifié
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Corrigé: {filepath}")
            return True
        else:
            print(f"  - Aucune modification nécessaire")
            return False
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        return False

def main():
    """Corriger tous les fichiers Python dans src/"""
    src_dir = 'src'
    
    if not os.path.exists(src_dir):
        print(f"Erreur: Le dossier '{src_dir}' n'existe pas!")
        print("Assurez-vous d'exécuter ce script depuis le dossier racine du projet.")
        return
    
    fixed_count = 0
    files_to_fix = [
        'main.py', 'theme.py', 'editor.py', 'database.py',
        'console.py', 'sql_builder.py', 'form_designer.py',
        'templates.py', 'project.py'
    ]
    
    print("Correction des fichiers PyQt6...\n")
    
    for filename in files_to_fix:
        filepath = os.path.join(src_dir, filename)
        if os.path.exists(filepath):
            if fix_file(filepath):
                fixed_count += 1
        else:
            print(f"  ⚠ Fichier non trouvé: {filepath}")
    
    print(f"\n{fixed_count} fichiers corrigés sur {len(files_to_fix)}")
    print("\nTerminé! Vous pouvez maintenant lancer: python src/main.py")

if __name__ == '__main__':
    main()