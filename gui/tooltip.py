from PyQt5.QtWidgets import QLabel, QApplication, QWidget
from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor


class ClickableTooltip(QLabel):
    """
    Custom QLabel for tooltips with rounded corners, supports rich text and 
    inks.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip)
        # self.setTextFormat(Qt.RichText)
        # self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.hide()
        self.setStyleSheet("""
            ClickableTooltip {
                font-family: 'Avenir Next';
                font-size: 12pt;
                margin: 8px;
            }
            """)

    def paintEvent(self, event):
        """Draws rounded corners for the tooltip."""
        rectF = QRectF(self.rect())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(rectF, 10, 10)
        painter.fillPath(path, QBrush(QColor("#ffffff")))
        super().paintEvent(event)


class CustomLabel(QLabel):
    """CustomLabel with clickable tooltips showing title, URL, and source."""

    def __init__(self, text, title, url, source, parent, mainWindow):
        super().__init__(text, parent)
        self.title = title
        self.url = url
        self.source = source
        self.mainWindow = mainWindow
        self.tooltipWidget = ClickableTooltip(self)
        self.tooltipWidget.hide()
        self.tooltipVisible = False
        mainWindow.registerCustomLabel(self)

    def mousePressEvent(self, event):
        """Toggles tooltip visibility on click."""
        if self.tooltipVisible:
            self.tooltipWidget.hide()
        else:
            source = f"<span style='color:black;'> - {self.source}</span>"
            tooltipText = f'<a href="{self.url}">{self.title}</a><i>{source}</i>'
            globalPos = self.mapToGlobal(QPoint(10, -30))
            self.tooltipWidget.setText(tooltipText)
            self.tooltipWidget.move(globalPos)
            self.tooltipWidget.show()
        self.tooltipVisible = not self.tooltipVisible
        super().mousePressEvent(event)
