from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, QRectF, QPoint, QTimer
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
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(3)
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
    headline as link and source.
    Attributes:
        article (dict): 
        tooltipWidget (obj): class instance
        delayTimer (obj): PyQT5 timer object, handles delayed show of tooltip so
        on timeout the timer emits a signal to `showTooltip` method
        parent (obj): reference to parent widget, used to hide tooltip on scroll

    """
    def __init__(self, text, article, parent):
        """ Initialise the text, the `CustomTooltip` widget and metadata. """
        super().__init__(text, parent)
        self.article = article
        self.tooltipWidget = ClickableTooltip(self)
        self.tooltipWidget.hide()
        self.delayTimer = QTimer(self)
        self.delayTimer.setSingleShot(True) 
        self.delayTimer.timeout.connect(self.showTooltip)
        self.parent = parent

    def mousePressEvent(self, event):
        """
            Listens for mouse clicks. Calls `prepareTooltip` to get tooltip 
            contents ready and starts times on event. On timeout, the
            'showTooltip' method is called.
        """
        # Listening for mouse click events
        super().mousePressEvent(event)

        # Calling for tooltip contents
        self.prepareTooltip()

        # Starting delay timer for window to appear
        self.delayTimer.start(200)


    def prepareTooltip(self):
        """
            Prepares fresh tooltip on each click by deleting exisint ones and
            composing the tooltip text(s).
        """
        # Deleting tooltips from display, prevents stacking of tooltips
        for i in reversed(range(self.tooltipWidget.layout().count())): 
            self.tooltipWidget.layout().itemAt(i).widget().setParent(None)


    def showTooltip(self):
        """
            Displays the tooltip (usually when 'delayTimer' expires). Positions
            the widget in relation to the parent label (the article text). 
            Makes a record in `MainWindow` parent about active 'tooltipWidget',
            which is used to hide tooltips on global scroll events.
        """
        # Positioning tooltip 
        globalPos = self.mapToGlobal(QPoint(5, -30))
        urls = self.article["url"]
        headlines = self.article["headline"]
        sources = self.article["source"]
        if self.article["grouped"]:
            for url, headline, source in zip(urls, headlines, sources):
                tooltipText = self._composeTooltipText(url, headline, source)
                label = QLabel(tooltipText, self.tooltipWidget)
                label.setFont(self.parent.set_font(13, 38, 105))
                label.setOpenExternalLinks(True)
                self.tooltipWidget.layout().addWidget(label)
        else:
            tooltipText = self._composeTooltipText(urls, headlines, sources)
            label = QLabel(tooltipText, self.tooltipWidget)
            label.setFont(self.parent.set_font(13, 38, spacing=105))
            label.setOpenExternalLinks(True)
            self.tooltipWidget.layout().addWidget(label)

        self.tooltipWidget.move(globalPos)
        self.tooltipWidget.show()

        # Notifying `MainWindow` on active tooltip
        self.parent.activeTooltip = self.tooltipWidget


    def _composeTooltipText(self, url, headline, source):
        """ Responsible for formattin and composing the tooltip text. """
        # Formatting tooltip meta-data
        # link_style = "color:blue; text-decoration:none;"
        info_style = "color:black; margin-left: 5px;"
        italic_style = "font-style:italic;"

        # # Composing tooltip text
        # if self.article["grouped"]:
        #     urls = self.article["url"]
        #     headlines = self.article["headline"]
        #     sources = self.article["source"]
        #     tooltipText = ""
        #     for url, headline, source in zip(urls, headlines, sources):
        #         tooltipText += f"""
        #         <div>
        #             <a href='{url}'>{headline}</a>
        #             <span style='{info_style}'>
        #                 - <span style='{italic_style}'>{source}</span>
        #             </span>
        #         </div>
        #         """
        # else:
        tooltipText = f"""
        <a href='{url}'>{headline}</a>
        <span style='{info_style}'>
            - <span style='{italic_style}'>{source}</span>
        </span>
        """
        return tooltipText.strip()

