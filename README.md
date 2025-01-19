# qt-theme

This is a collection of themes for Qt in Python.

The color schemes are applied using QPalettes which avoids the conflicts that can happen
when using stylesheets.

## Installation

Install using pip:
```shell
pip install qt-theme
```

## Usage

```python
from PySide6 import QtWidgets
import qt_theme

app = QtWidgets.QApplication()
qt_theme.set_color_scheme('nord')
widget = QtWidgets.QWidget()
widget.show()
app.exec()
```

Additional color schemes can be provided using the environment variable
`QT_COLOR_SCHEMES`.

## Contributing

To contribute please refer to the [Contributing Guide](CONTRIBUTING.md).

## License

MIT License. Copyright 2024 - Beat Reichenbach.
See the [License file](LICENSE) for details.
