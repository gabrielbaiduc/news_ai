import sys
import logging

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QApplication, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QScrollArea, QSizePolicy
)
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt, QEvent, QSize

from gui.tooltip import CustomLabel
from gui.backend import ArticleProcessor

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("News-AI")
        self.setGeometry(100, 100, 800, 1000)

        self.status_label = QLabel("Initializing")
        font = QFont()
        font.setFamily("Avenir Next")
        font.setPointSize(20)
        self.status_label.setFont(font)
        self.status_label.setStyleSheet("color: #979797;")

        self.spinner_label = QLabel()
        self.spinner_movie = QMovie("/Users/gabbai/news_ai/gui/resources/transp.gif")
        self.spinner_label.setMovie(self.spinner_movie)
        self.spinner_movie.start()
        self.spinner_movie.setScaledSize(QSize(40, 40))

        self.layout = QHBoxLayout()
        self.layout.addStretch(5)    
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.spinner_label)
        self.layout.addStretch(5)    

        self.container_widget = QWidget()
        self.container_widget.setLayout(self.layout)
        self.setCentralWidget(self.container_widget)

        self.start_background_task()

        self.setStyleSheet("""
            QTabWidget::pane { 
                border: none;
            }
            QTabBar::tab {
                border: none;
                padding: 20px;
            }
            QTabBar::tab:selected {
                color: gray;
            }
            QTabBar::tab:hover {
                color: gray;
            }
        """)

        self.customLabelInstances = []
        QApplication.instance().installEventFilter(self)

    def registerCustomLabel(self, customLabel):
        self.customLabelInstances.append(customLabel)

    def getAllCustomLabelInstances(self):
        return self.customLabelInstances

    def eventFilter(self, source, event):
        if event.type() == QEvent.WindowDeactivate and source is self:
            self.hideAllTooltips()
        return super().eventFilter(source, event)

    def hideAllTooltips(self):
        for customLabel in self.getAllCustomLabelInstances():
            customLabel.tooltipWidget.hide()

    def start_background_task(self):
        self.thread = ArticleProcessor()
        self.thread.status_update.connect(self.update_status)
        self.thread.finished.connect(self.scraping_finished)
        self.thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def scraping_finished(self, articles):
        self.takeCentralWidget() # Clear widgets from loading page
        self.tabs = QTabWidget() # Create tabs
        self.setCentralWidget(self.tabs)
        font_for_tabs = QFont()
        font_for_tabs.setFamily("Avenir Next")
        font_for_tabs.setPointSize(12)
        font_for_tabs.setWeight(20)
        font_for_tabs.setLetterSpacing(QFont.PercentageSpacing, 110)
        self.tabs.tabBar().setFont(font_for_tabs)

        for category in articles:
            # Create tab widget
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.setAlignment(Qt.AlignCenter)
            tab_layout.setContentsMargins(85, 35, 85, 35)
            tab_layout.setSpacing(20)

            content_widget = QWidget()
            content_widget.setLayout(tab_layout)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(content_widget)

            layout = QVBoxLayout(tab)
            layout.addWidget(scroll_area)
            self.tabs.addTab(scroll_area, f"{category}")


            for article in articles[category]:
                summary = article["summary"]
                headline = article["headline"]
                url = article["url"]
                source = article["source"]
                bodycount = article["bodycount"]
                relsize = article["relativesize"]
                # load main text and tooltip fillers onto widget
                label = CustomLabel(summary, headline, url, source, bodycount, 
                                    relsize, content_widget, self)
                # two lines that prevent horizontal and vertical overflow
                label.setWordWrap(True) 
                label.setSizePolicy(QSizePolicy.Expanding, 
                                        QSizePolicy.Expanding) 
                font = QFont()
                font.setFamily("Avenir Next")
                font.setPointSize(14)
                font.setLetterSpacing(QFont.PercentageSpacing, 105)
                # font.setWeight(15)
                label.setFont(font)
                tab_layout.addWidget(label)



