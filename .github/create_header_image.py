import os.path
from collections.abc import Sequence

from PySide6 import QtCore, QtGui, QtWidgets


class MaskedPixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(
        self,
        pixmap: QtGui.QPixmap | QtGui.QImage,
        parent: QtWidgets.QGraphicsItem | None = None,
    ) -> None:
        super().__init__(parent)
        self.setPixmap(pixmap)
        self.pixmap = pixmap

        self._offset = 0
        self._shear = 100
        self._orientation = QtCore.Qt.Orientation.Horizontal

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionGraphicsItem,
        widget: QtWidgets.QWidget | None = None,
    ) -> None:
        painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        painter.setClipPath(self._shear_path())
        super().paint(painter, option, widget)

    def _shear_path(self) -> QtGui.QPainterPath:
        rect = self.pixmap.rect()
        path = QtGui.QPainterPath()
        if self._orientation == QtCore.Qt.Orientation.Horizontal:
            path.moveTo(QtCore.QPointF(self._offset, 0))
            path.lineTo(QtCore.QPointF(self._offset - self._shear, rect.height()))
            path.lineTo(QtCore.QPointF(rect.width(), rect.height()))
            path.lineTo(QtCore.QPointF(rect.width(), 0))
        else:
            path.moveTo(QtCore.QPointF(0, self._offset))
            path.lineTo(QtCore.QPointF(rect.width(), self._offset - self._shear))
            path.lineTo(QtCore.QPointF(rect.width(), rect.height()))
            path.lineTo(QtCore.QPointF(0, rect.height()))
        path.closeSubpath()
        return path

    def set_offset(self, offset: int) -> None:
        self._offset = offset

    def set_shear(self, shear: int) -> None:
        self._shear = shear

    def set_orientation(self, orientation: QtCore.Qt.Orientation) -> None:
        self._orientation = orientation


def create_header_image(
    paths: Sequence[str],
    output_path: str,
    shadow_radius: int = 32,
    shadow_offset: QtCore.QPoint = QtCore.QPoint(0, 4),
) -> None:
    if not paths:
        raise ValueError('paths cannot be empty')

    QtWidgets.QApplication()

    # Graphics View
    view = QtWidgets.QGraphicsView()
    view.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

    # Graphics Scene
    rect = QtGui.QPixmap(paths[0]).rect()
    scene = QtWidgets.QGraphicsScene()
    scene_rect = QtCore.QRect(
        int((-shadow_radius + shadow_offset.x()) / 2),
        int((-shadow_radius + shadow_offset.y()) / 2),
        rect.width() + shadow_radius,
        rect.height() + shadow_radius,
    )
    scene.setSceneRect(scene_rect)
    view.setScene(scene)

    # Drop Shadow
    drop_shadow = QtWidgets.QGraphicsDropShadowEffect()
    drop_shadow.setOffset(shadow_offset)
    drop_shadow.setBlurRadius(shadow_radius)
    drop_shadow.setColor(QtGui.QColorConstants.Black)

    # Masked Images
    for i, path in enumerate(paths):
        pixmap = QtGui.QPixmap(path)
        if i == 0:
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            item.setGraphicsEffect(drop_shadow)
        else:
            item = MaskedPixmapItem(pixmap)
            shear = 300
            offset = int((pixmap.rect().width() + shear) / len(paths) * i)
            item.set_offset(offset)
            item.set_shear(shear)
        scene.addItem(item)

    # Save Scene to image
    image = QtGui.QImage(
        scene_rect.width(), scene_rect.height(), QtGui.QImage.Format.Format_ARGB32
    )
    image.fill(QtCore.Qt.GlobalColor.transparent)
    painter = QtGui.QPainter(image)
    scene.render(painter, target=QtCore.QRectF(image.rect()), source=scene_rect)
    painter.end()
    image.save(output_path)


def create_theme_header_image() -> None:
    assets_dir = os.path.realpath('./assets')
    themes = (
        'catppuccin_latte',
        'one_dark_two',
        'monokai',
        'catppuccin_frappe',
        'atom_one',
        'nord',
    )
    paths = []
    for theme in themes:
        paths.append(os.path.join(assets_dir, f'{theme}.png'))
    create_header_image(paths, os.path.join(assets_dir, 'header.png'))


if __name__ == '__main__':
    create_theme_header_image()
