from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor


class ClickableTooltip(QWidget):
    """ 
    Custom QWidget. Handles the appearence and behaviour of the clickable 
    tooltip window. This window contains information about the original article
    and summary.
    """
    def __init__(self, parent=None):
        """ Initialise a Popup style window with a vertical layout. """
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 10, 5, 10)
        self.setLayout(layout)
        self.adjustSize() # Adjusts window size

    def paintEvent(self, event):
        """ Redraws the clickable tooltip window with rounded corners. """
        rectF = QRectF(self.rect())
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(rectF, 10, 10)
        painter.fillPath(path, QBrush(QColor("#ffffff")))
        super().paintEvent(event)


class CustomLabel(QLabel):
    """
    Custom QLabel. This is the main container for the article summary.
    The custom funcionality handles the `ClicableTooltip` window that shows
    article related meta information.
    """
    def __init__(self, text, article, parent):
        """ Initialise the text, the `CustomTooltip` widget and metadata. """
        super().__init__(text, parent)
        self.article = article
        self.tooltipWidget = ClickableTooltip(self)
        self.tooltipWidget.hide()

    def mousePressEvent(self, event):
        """ 
        Event listener. With each click on the main QLabel a tooltip text is 
        composed and added to the tooltip. A useful property of `ClickableTooltip`
        is the `Qt.Popup` window flag which ensures that the tooltip window 
        disappears whenever we click outside of it. This behaviour eliminates
        the need to listed for multiple click-events, then manually show or hide
        the tooltip, resulting in much cleaner code. A downside is that the 
        tooltip draws focus so scrolling is disabled and we must first 
        "click away" the tooltip before other actions are permitted within
        the app.
        """
        # Listening for mouse click
        super().mousePressEvent(event)

        # Deleting tooltips text
        # This code ensures that the tooltip associated with each main QLabel is 
        # refreshed with each click, without this the tooltip text would 
        # accumulate within the tooltip window.
        for i in reversed(range(self.tooltipWidget.layout().count())): 
            self.tooltipWidget.layout().itemAt(i).widget().setParent(None)

        # Composing the tooltip text
        tooltipText = self._composeTooltipText()

        # Calculating position of tooltip window
        globalPos = self.mapToGlobal(QPoint(5, -30))

        # Adding tooltip text to tooltip window, enabling external links
        label = QLabel(tooltipText, self.tooltipWidget)
        label.setOpenExternalLinks(True)

        # Adding tooltip text to layout within tooltip window
        self.tooltipWidget.layout().addWidget(label)

        # Positioning the tooltip window 
        self.tooltipWidget.move(globalPos)

        # Showing the tooltip window
        self.tooltipWidget.show()

    def _composeTooltipText(self):
        """ Responsible for formattin and composing the tooltip text. """
        # Formatting tooltip meta-data
        link_style = "color:blue; text-decoration:none;"
        info_style = "color:black; margin-left: 5px;"
        italic_style = "font-style:italic;"

        # Composing tooltip text
        tooltipText = f"""
        <a href='{self.article["url"]}'>{self.article["headline"]}</a>
        <span style='{info_style}'>
            - <span style='{italic_style}'>{self.article["source"]}</span>
            - {self.article["bodycount"]}
            - {self.article["summarycount"]}
            - {self.article["relativesize"]}%
        </span>
        """
        return tooltipText.strip()

