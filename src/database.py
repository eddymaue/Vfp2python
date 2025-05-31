# form_designer.py
"""Module pour le concepteur de formulaires drag & drop"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,
                             QToolBar, QLabel, QDialog, QTextEdit,
                             QPushButton, QMessageBox, QApplication)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QEvent, QMimeData
from PyQt6.QtGui import QFont, QDrag, QAction

from theme import ModernTheme


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
        from PyQt6.QtWidgets import (QLabel, QPushButton, QLineEdit, QTextEdit,
                                     QCheckBox, QRadioButton, QComboBox, QDateEdit,
                                     QTableWidget, QGroupBox)

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