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

    def scraping_finished(self, processed_articles):
        self.takeCentralWidget() # Clear widgets from loading page
        self.tabs = QTabWidget() # Create tabs
        self.setCentralWidget(self.tabs)
        font_for_tabs = QFont()
        font_for_tabs.setFamily("Avenir Next")
        font_for_tabs.setPointSize(12)
        font_for_tabs.setWeight(20)
        font_for_tabs.setLetterSpacing(QFont.PercentageSpacing, 110)
        self.tabs.tabBar().setFont(font_for_tabs)

        for category, articles in processed_articles.items():
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

            for url, title, summary, source in reversed(articles):
                # load main text and tooltip fillers onto widget
                label = CustomLabel(summary, title, url, source, 
                                    content_widget, self)
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

            self.tabs.addTab(scroll_area, f"{category}")


# TEMPLATE FOR IMPROVEMENT
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         # Initialize the main window
#         self.setWindowTitle("Article Summarizer")
#         self.setGeometry(100, 100, 800, 1000)
        
#         # Initialize UI components
#         self.init_ui_components()
        
#         # Start the background task
#         self.start_background_task()

#         # Custom label instances for tooltips management
#         self.customLabelInstances = []
#         QApplication.instance().installEventFilter(self)

#     def init_ui_components(self):
#         """Initialize the UI components of the MainWindow."""
#         # Status label setup
#         self.status_label = QLabel("Initializing...")
#         self.status_label.setAlignment(Qt.AlignCenter)
#         self.set_custom_font(self.status_label, "Avenir Next", 20)
#         self.setCentralWidget(self.status_label)

#         # Styling
#         self.apply_stylesheet()

#     def apply_stylesheet(self):
#         """Apply CSS stylesheet to the MainWindow."""
#         self.setStyleSheet("""
#             QLabel {
#                 color: white;
#                 font-family: 'Avenir Next';
#                 font-size: 14pt;
#                 letter-spacing: 105%;
#                 margin: 10px;
#             }
#             ...
#         """)

#     def set_custom_font(self, widget, family, point_size):
#         """Set custom font for a given widget."""
#         font = QFont()
#         font.setFamily(family)
#         font.setPointSize(point_size)
#         widget.setFont(font)

#     def registerCustomLabel(self, customLabel):
#         """Register a custom label to manage its tooltips."""
#         self.customLabelInstances.append(customLabel)

#     def getAllCustomLabelInstances(self):
#         """Get all registered custom label instances."""
#         return self.customLabelInstances

#     def eventFilter(self, source, event):
#         """Filter events, particularly for deactivating window tooltips."""
#         if event.type() == QEvent.WindowDeactivate and source is self:
#             self.hideAllTooltips()
#         return super().eventFilter(source, event)

#     def hideAllTooltips(self):
#         """Hide tooltips for all custom labels."""
#         for customLabel in self.getAllCustomLabelInstances():
#             customLabel.tooltipWidget.hide()

#     def start_background_task(self):
#         """Start a background task for article processing."""
#         self.thread = ArticleProcessor()
#         self.thread.status_update.connect(self.update_status)
#         self.thread.finished.connect(self.scraping_finished)
#         self.thread.start()

#     def update_status(self, message):
#         """Update the status label with a message."""
#         self.status_label.setText(message)

#     def scraping_finished(self, processed_articles):
#         """Handle the completion of the background scraping task."""
#         # Clear the central widget
#         self.takeCentralWidget()
#         # Setup tabs for article categories
#         self.setup_tabs(processed_articles)

#     def setup_tabs(self, processed_articles):
#         """Setup tabs for each category of processed articles."""
#         self.tabs = QTabWidget()
#         self.setCentralWidget(self.tabs)

#         for category, articles in processed_articles.items():
#             self.add_category_tab(category, articles)

#     def add_category_tab(self, category, articles):
#         """Add a tab for a specific article category."""
#         tab = QWidget()
#         tab_layout = QVBoxLayout()
#         tab_layout.setAlignment(Qt.AlignCenter)
#         ...

#         self.tabs.addTab(scroll_area, f"{category}")

