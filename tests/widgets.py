import os

from PySide6 import QtGui, QtWidgets, QtCore
import qt_themes
from tests import application


class WidgetControls(QtWidgets.QWidget):
    style_changed: QtCore.Signal = QtCore.Signal(str)
    theme_changed: QtCore.Signal = QtCore.Signal(str)
    disabled: QtCore.Signal = QtCore.Signal(bool)
    screenshot_requested: QtCore.Signal = QtCore.Signal()
    screenshot_all_requested: QtCore.Signal = QtCore.Signal()

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(QtCore.QMargins())
        self.setLayout(layout)

        # Style Dropdown
        style_label = QtWidgets.QLabel('Style:')
        layout.addWidget(style_label)
        style_combobox = QtWidgets.QComboBox()
        style_combobox.addItems(QtWidgets.QStyleFactory.keys())
        style = 'fusion'
        QtWidgets.QApplication.setStyle(style)
        style_combobox.setCurrentText(style)
        style_combobox.currentTextChanged.connect(self.style_changed.emit)
        layout.addWidget(style_combobox)

        # Theme Dropdown
        theme_label = QtWidgets.QLabel('Theme:')
        layout.addWidget(theme_label)
        self.theme_combo = QtWidgets.QComboBox()
        names = ['default']
        names.extend(qt_themes.get_themes().keys())
        self.theme_combo.addItems(names)
        self.theme_combo.currentTextChanged.connect(self.theme_changed.emit)
        layout.addWidget(self.theme_combo)
        layout.addStretch()

        # Disable
        disable_button = QtWidgets.QCheckBox('Disable')
        disable_button.toggled.connect(self.disabled.emit)
        layout.addWidget(disable_button)

        # Screenshot
        screenshot_button = QtWidgets.QPushButton('Screenshot')
        screenshot_button.clicked.connect(self.screenshot_requested)
        layout.addWidget(screenshot_button)

        screenshot_button = QtWidgets.QPushButton('Screenshot All')
        screenshot_button.clicked.connect(self.screenshot_all_requested)
        layout.addWidget(screenshot_button)

    def set_theme(self, theme: str) -> None:
        self.theme_combo.setCurrentText(theme)


class WidgetGallery(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Controls
        self.controls = WidgetControls()
        self.controls.style_changed.connect(self._set_style)
        self.controls.theme_changed.connect(self._set_theme)
        self.controls.disabled.connect(self._set_disabled)
        self.controls.screenshot_requested.connect(self._screenshot)
        self.controls.screenshot_all_requested.connect(self._screenshot_all)
        layout.addWidget(self.controls)

        # Widgets
        widget_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(widget_layout)

        # Components
        component_widget = QtWidgets.QWidget()
        component_layout = QtWidgets.QVBoxLayout()
        component_widget.setLayout(component_layout)

        # Buttons
        button_group = QtWidgets.QGroupBox('Buttons')
        button_group.setCheckable(True)
        component_layout.addWidget(button_group)
        button_layout = QtWidgets.QGridLayout()
        button_group.setLayout(button_layout)

        # Push Buttons
        push_button_group = QtWidgets.QGroupBox('Push Buttons')
        push_button_group.setFlat(True)
        button_layout.addWidget(push_button_group, 0, 0)
        push_button_layout = QtWidgets.QHBoxLayout()
        push_button_group.setLayout(push_button_layout)

        button = QtWidgets.QPushButton('Normal')
        push_button_layout.addWidget(button)

        button = QtWidgets.QPushButton('Checkable')
        button.setCheckable(True)
        button.setChecked(True)
        push_button_layout.addWidget(button)

        button = QtWidgets.QPushButton('Flat')
        button.setFlat(True)
        push_button_layout.addWidget(button)

        # Tool Buttons
        tool_button_group = QtWidgets.QGroupBox('Tool Buttons')
        tool_button_group.setFlat(True)
        button_layout.addWidget(tool_button_group, 1, 0)
        tool_button_layout = QtWidgets.QHBoxLayout()
        tool_button_group.setLayout(tool_button_layout)

        button = QtWidgets.QToolButton()
        button.setText('Normal')
        tool_button_layout.addWidget(button)

        button = QtWidgets.QToolButton()
        button.setText('Menu')
        menu = QtWidgets.QMenu(self)
        menu.addActions(tuple(QtGui.QAction(f'Action {i + 1}', self) for i in range(3)))
        button.setMenu(menu)
        button.setPopupMode(QtWidgets.QToolButton.ToolButtonPopupMode.InstantPopup)
        tool_button_layout.addWidget(button)

        button = QtWidgets.QToolButton()
        button.setText('Icon')
        icon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_FileIcon)
        button.setIcon(icon)
        tool_button_layout.addWidget(button)

        # Checkbox Buttons

        checkbox_group = QtWidgets.QGroupBox('Checkbox Buttons')
        checkbox_group.setFlat(True)
        button_layout.addWidget(checkbox_group, 0, 1)
        checkbox_layout = QtWidgets.QHBoxLayout()
        checkbox_group.setLayout(checkbox_layout)

        button = QtWidgets.QCheckBox()
        checkbox_layout.addWidget(button)

        button = QtWidgets.QCheckBox()
        button.setChecked(True)
        checkbox_layout.addWidget(button)

        button = QtWidgets.QCheckBox()
        button.setCheckState(QtCore.Qt.CheckState.PartiallyChecked)
        checkbox_layout.addWidget(button)

        # Radio Buttons
        radio_group = QtWidgets.QGroupBox('Radio Buttons')
        radio_group.setFlat(True)
        button_layout.addWidget(radio_group, 1, 1)
        radio_layout = QtWidgets.QHBoxLayout()
        radio_group.setLayout(radio_layout)

        button = QtWidgets.QRadioButton()
        radio_layout.addWidget(button)

        button = QtWidgets.QRadioButton()
        button.setChecked(True)
        radio_layout.addWidget(button)

        # Inputs
        input_group = QtWidgets.QGroupBox('Inputs')
        input_group.setCheckable(True)
        component_layout.addWidget(input_group)
        input_layout = QtWidgets.QVBoxLayout()
        input_group.setLayout(input_layout)

        line_edit = QtWidgets.QLineEdit()
        line_edit.setPlaceholderText('Placeholder ...')
        input_layout.addWidget(line_edit)

        spin_box = QtWidgets.QSpinBox()
        input_layout.addWidget(spin_box)

        combo_box = QtWidgets.QComboBox()
        combo_box.addItems(tuple(f'Item {i + 1}' for i in range(5)))
        input_layout.addWidget(combo_box)

        slider = QtWidgets.QSlider()
        slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        input_layout.addWidget(slider)

        date_time_edit = QtWidgets.QDateTimeEdit()
        input_layout.addWidget(date_time_edit)

        # Display Widgets

        display_group = QtWidgets.QGroupBox('Display')
        display_group.setCheckable(True)
        component_layout.addWidget(display_group)
        display_layout = QtWidgets.QVBoxLayout()
        display_group.setLayout(display_layout)

        button = QtWidgets.QPushButton('ToolTip')
        button.setToolTip('This is a tooltip.')
        display_layout.addWidget(button)

        button = QtWidgets.QPushButton('Default')
        button.setAutoDefault(True)
        button.setDefault(True)
        display_layout.addWidget(button)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        display_layout.addWidget(line)

        progress = QtWidgets.QProgressBar()
        progress.setMaximum(0)
        progress.setTextVisible(False)
        display_layout.addWidget(progress)

        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        display_layout.addWidget(line)

        progress = QtWidgets.QProgressBar()
        progress.setValue(10)
        display_layout.addWidget(progress)

        # Splitter
        splitter = QtWidgets.QSplitter()
        splitter.addWidget(input_group)
        splitter.addWidget(display_group)
        component_layout.addWidget(splitter)

        # Extra

        extra_widget = QtWidgets.QWidget()
        extra_layout = QtWidgets.QVBoxLayout()
        extra_widget.setLayout(extra_layout)

        tool_bar = QtWidgets.QToolBar()
        for i in range(3):
            action = QtGui.QAction(f'Action {i + 1}', parent=self)
            tool_bar.addAction(action)
            tool_bar.addSeparator()
        extra_layout.addWidget(tool_bar)

        date_edit = QtWidgets.QCalendarWidget()
        extra_layout.addWidget(date_edit)

        label = QtWidgets.QLabel('<a href="https://www.qt.io/">Link</a>')
        extra_layout.addWidget(label)

        # Tabs

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(component_widget, 'Components')
        self.tab_widget.addTab(extra_widget, 'Extra')
        widget_layout.addWidget(self.tab_widget)

        # Views

        self.view_widget = QtWidgets.QWidget()
        view_layout = QtWidgets.QVBoxLayout()
        self.view_widget.setLayout(view_layout)
        widget_layout.addWidget(self.view_widget)

        # Tree
        tree_widget = QtWidgets.QTreeWidget()
        tree_widget.setHeaderLabels(('Name', 'Value'))
        for i in range(5):
            item = QtWidgets.QTreeWidgetItem(('Item', f'{i + 1}'))
            for h in range(3):
                item.addChild(QtWidgets.QTreeWidgetItem((f'Child {h + 1}', f'{i + 1}')))
            tree_widget.addTopLevelItem(item)
        view_layout.addWidget(tree_widget)

        # Table
        table_widget = QtWidgets.QTableWidget(25, 3)
        table_widget.horizontalHeader().setStretchLastSection(True)
        table_widget.setAlternatingRowColors(True)
        table_widget.setHorizontalHeaderLabels(('Name', 'Value', 'Type'))
        for i in range(25):
            for j in range(3):
                item = QtWidgets.QTableWidgetItem()
                item.setText(f'Item_{i}_{j}')
                table_widget.setItem(i, j, item)
        view_layout.addWidget(table_widget)

    def _screenshot(self) -> None:
        theme = self.controls.theme_combo.currentText()
        path = os.path.join('..', '.github', 'assets', f'{theme}.png')
        pixmap = self.grab()
        pixmap.save(path)

    def _screenshot_all(self) -> None:
        combo = self.controls.theme_combo
        combo.blockSignals(True)
        for i in range(combo.count()):
            combo.setCurrentIndex(i)
            theme = combo.currentText()
            self._set_theme(theme)
            QtWidgets.QApplication.processEvents()

            path = os.path.join('..', '.github', 'assets', f'{theme}.png')
            pixmap = self.grab()
            pixmap.save(path)
        combo.blockSignals(False)

    def _set_disabled(self, disabled: bool) -> None:
        self.tab_widget.setEnabled(not disabled)
        self.view_widget.setEnabled(not disabled)

    @staticmethod
    def _set_style(style: str) -> None:
        app = QtWidgets.QApplication.instance()
        if isinstance(app, QtWidgets.QApplication):
            app.setStyle(style)

    @staticmethod
    def _set_theme(theme: str) -> None:
        if theme == 'default':
            theme = None
        qt_themes.set_theme(theme, style=None)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle('Widget Gallery')
        self.resize(1280, 720)

        # Menu Bar
        menu_bar = QtWidgets.QMenuBar(parent=self)
        for menu in ('File', 'Edit', 'View', 'Help'):
            sub_menu = menu_bar.addMenu(menu)
            for text in ('New', 'Open', 'Save'):
                sub_menu.addAction(text)
                sub_menu.addSection('Section')
        self.setMenuBar(menu_bar)

        # Central Widget
        widget_gallery = WidgetGallery()
        self.setCentralWidget(widget_gallery)

        # Status Bar
        status_bar = QtWidgets.QStatusBar()
        status_bar.showMessage('Status Bar')
        self.setStatusBar(status_bar)


def test_widgets() -> None:
    with application():
        window = MainWindow()
        window.show()


if __name__ == '__main__':
    test_widgets()
