# qt-themes

This is a collection of themes for Qt in Python.

The color schemes are applied with a QPalette which avoids the conflicts that can
happen when using stylesheets.

![Header](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/header.png)

## Installation

Install using pip:
```shell
pip install qt-themes
```

## Usage

Apply a theme for the QApplication:
```python
from PySide6 import QtWidgets
import qt_themes

app = QtWidgets.QApplication()
qt_themes.set_theme('nord')
widget = QtWidgets.QWidget()
widget.show()
app.exec()
```

Get a color from a theme:
```python
import qt_themes

theme = qt_themes.get_theme('atom_one')
green = theme.green
```

Additional themes can be provided using the environment variable `QT_THEMES`.

## Themes

These are some of the themes that are included in the package.

<details>
<summary>One Dark Two</summary>

<https://github.com/beatreichenbach/one_dark_two>

![One Dark Two](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/one_dark_two.png)

</details>

<details>
<summary>Monokai</summary>

<https://monokai.pro>

![Monokai](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/monokai.png)

</details>

<details>
<summary>Nord</summary>

<https://nordtheme.com>

![Nord](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/nord.png)

</details>

<details>
<summary>Catppuccin</summary>

<https://catppuccin.com>

![Catppuccin Latte](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/catppuccin_latte.png)
![Catppuccin Frappe](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/catppuccin_frappe.png)
![Catppuccin Macchiato](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/catppuccin_macchiato.png)
![Catppuccin Mocha](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/catppuccin_mocha.png)

</details>

<details>
<summary>Atom One</summary>

<https://atom.io>

![Atom One](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/atom_one.png)

</details>

<details>
<summary>GitHub</summary>

<https://github.com>

![GitHub Dark](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/github_dark.png)
![GitHub Light](https://raw.githubusercontent.com/beatreichenbach/qt-themes/refs/heads/main/.github/assets/github_light.png)

</details>

## Contributing

To contribute please refer to the [Contributing Guide](CONTRIBUTING.md).

## License

MIT License. Copyright 2024 - Beat Reichenbach.
See the [License file](LICENSE) for details.
