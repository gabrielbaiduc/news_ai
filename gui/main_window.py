import sys
import logging

import requests
import keyring
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QApplication, QTabWidget, QWidget, QVBoxLayout, 
    QHBoxLayout, QScrollArea, QSizePolicy, QLineEdit, QPushButton, QSpacerItem
)
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import Qt, QEvent, QSize

from gui.widgets import CustomLabel
from gui.backend import ArticleProcessor
from config.settings import kr_system, kr_username

# This module wraps most of the application logic. 
# The MainWindow handles the GUI elements and handles the backcend logic on
# a separate thread. The 3 stages of the GUI are the:
#   1) the landing screen: contains a welcome message and data-entry 
#       protocols. It handles secret keys with keyring that uses OS specific 
#       secure key storage like 'Keychain'
#   2) the loading screen: dynamic loading screen that informs users on the 
#       status of the backend process. While on the loading screen the backend 
#       thread runs the scraping, summarising and other logic to prep articles
#       for display.
#   3) the main screen: displays the articles in a tabbed format. This window
#       implements some custom widgets to display a clickable tooltip for each
#       summary.

# ToDo:
# 1) Clear up `init_main_article`
# 2) Merge the `api` and `noapi` landing and start button logic
# 3) Add welcome text
# 4) Add error messages to the UI when clicking `Start` and API is invalid or 
#   not entered
# 5) Add option to change API key once saved

# Initialising logging and keyring constants
logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Entry point for the aplication.
    """
    def __init__(self):
        super().__init__()
        # Set window size and title on open
        self.setWindowTitle("News-AI")
        self.setGeometry(100, 100, 800, 1000)

        # Installing scrolling event filter to hide tooltips on scroll
        QApplication.instance().installEventFilter(self)
        self.activeTooltip = None

        # API key check ahead of UI init
        self.check_for_api()
        # keyring.delete_password(kr_system, kr_username)


    def check_for_api(self):
        """ Checks for auth key then initializes UI """ 
        self.api_key = keyring.get_password(kr_system, kr_username)
        self.init_landing()


    def init_landing(self):
        """ Unified landing page initialization. """
        # Set container widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_v_layout = QVBoxLayout(main_widget)
        self.configure_layout(main_v_layout)

        # Add UI components
        self.add_welcome_label(main_v_layout, api_key_exists=bool(self.api_key))
        if not self.api_key:
            self.add_api_input(main_v_layout)
        self.add_start_button(main_v_layout)


    def configure_layout(self, layout):
        """Configure layout alignment and margins."""
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(50, 0, 50, 0)
        layout.setSpacing(20)


    def add_welcome_label(self, layout, api_key_exists):
        """Add a welcome label to the layout."""
        text = ("Welcome to News-AI" if not api_key_exists 
            else "Welcome back to News-AI")
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(self.set_font(20))
        label.setStyleSheet("color: #979797;")
        layout.addWidget(label)


    def add_api_input(self, layout):
        """Add API key input field to the layout."""
        self.api_input = QLineEdit()
        self.api_input.setEchoMode(QLineEdit.Password)
        self.api_input.setPlaceholderText("Enter your OpenAI API key here...")
        self.api_input.setFont(self.set_font(14))
        self.api_input.setFixedSize(400, 35)  # Set fixed size for input field
        self.api_input.setStyleSheet("padding: 5px; border-radius: 10px;")

        # Center the input field with a horizontal layout
        api_input_h_layout = QHBoxLayout()
        api_input_h_layout.addWidget(self.api_input)
        api_input_h_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(api_input_h_layout)

        # Add a label for displaying errors under the API input
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.error_label) 


    def add_start_button(self, layout):
        """Add a start button to the layout with a fixed size."""
        button = QPushButton("Start")
        button.setFont(self.set_font(16))
        button.setStyleSheet("""
            QPushButton {
             color: #979797; 
             border: 1px solid gray; 
             border-radius: 15px; 
             padding: 5px; }

            QPushButton:hover {
             background-color: gray; 
            }
             """)
        button_h_layout = QHBoxLayout()
        
        # This will center the button within the horizontal layout
        button_h_layout.addStretch()
        button_h_layout.addWidget(button)
        button_h_layout.addStretch()
        
        # Set the fixed size of the button (width, height)
        button.setFixedSize(175, 40)  
        
        button.clicked.connect(self.start_application)
        layout.addLayout(button_h_layout)


    def start_application(self):
        """Unified method to handle Start button click."""
        # If API key is not set, try to get it from the input field
        if not self.api_key:
            entered_api_key = self.api_input.text().strip()
            if entered_api_key:
                if self.check_api_key(entered_api_key):
                    self.api_key = entered_api_key
                    keyring.set_password(kr_system, kr_username, self.api_key)
                    self.init_loading_screen()
                    self.start_background_task()
                else:
                    self.error_label.setText(
                        f"API Key invalid! Enter a valid OpenAI API Key.")
            else:
                self.error_label.setText("You must enter an OpenAI API Key.")
        else:
            self.init_loading_screen()
            self.start_background_task()


    def check_api_key(self, api_key):
        """ 
        Handles auth key validation 

        Params:
            api_key (str): the api key
        """
        # Initialise the target url and auth key
        url = "https://api.openai.com/v1/models"
        headers = {"Authorization": f"Bearer {api_key}"}

        # Attempt to connect return True only if `200` False otherwise 
        try:
            response = requests.head(url, headers=headers)
            if response.status_code == 200:
                return True
            else:
                print(response.status_code)
                return False
        except requests.exceptions.RequestException as error:
            return False


    def start_background_task(self):
        """ 
        Handles the background thread and its connections to the main window
        """
        # Initialising Thread instance
        self.thread = ArticleProcessor()

        # Connecting thread to status labels
        self.thread.status_update.connect(self.update_status)

        # Connecting thread to main article window
        self.thread.finished.connect(self.init_main_article)

        # Starting background thread
        self.thread.start()


    def update_status(self, message):
        """ 
        Handles status updates between the background thread and loading 
        screen.

        Params:
            message (str): the new status message
        """
        self.status_label.setText(message)


    def init_loading_screen(self):
        """ Handles the loading screen after start. """
        # Clearing landing UI
        self.takeCentralWidget()

        # Creating container widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Setting horizontal layout
        main_h_layout = QHBoxLayout(main_widget)

        # Creating and styling status msg
        self.status_label = QLabel("Initializing")
        self.status_label.setFont(self.set_font(20))
        self.status_label.setStyleSheet("color: #979797;")

        # Creating and styling spinner animation
        spinner_label = QLabel()
        spinner_movie = QMovie("/Users/gabbai/news_ai/gui/resources/loader.gif")
        spinner_label.setMovie(spinner_movie)
        spinner_movie.setScaledSize(QSize(40, 40))
        spinner_movie.start()

        # Positioning status msg and spinner animation
        main_h_layout.addStretch(1)
        main_h_layout.addWidget(self.status_label)
        main_h_layout.addWidget(spinner_label)
        main_h_layout.addStretch(1)


    def init_main_article(self, articles):
        """
        Handles the main article display screen.
        """
        self.takeCentralWidget()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.setStyleSheet("""
                QTabWidget::pane {
                    border: none;
                }
                QTabBar::tab {
                    border: none;
                    padding: 20px;
                }
                QTabBar::tab:selected, QTabBar::tab:hover {
                    color: gray;
                }
            """)
        self.tabs.tabBar().setFont(self.set_font(12, 20, 110))

        for category in articles:
            tab = QWidget()
            tab_layout = QVBoxLayout(tab)
            tab_layout.setContentsMargins(85, 35, 85, 35)
            tab_layout.setSpacing(20)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(tab)
            self.tabs.addTab(scroll_area, f"{category}")

            for article in articles[category]:
                label = CustomLabel(article["summary"], article, self)
                label.setWordWrap(True)
                label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                label.setFont(self.set_font(14))
                tab_layout.addWidget(label)


    def set_font(self, size, weight=None, spacing=None, family="Avenir Next"):
        """ 
        Handles font styling. Default family is 'Avenir Next'. It creates a font
        objet that can be styled and passed to widgets as the main argument for
        the 'setFont' method.
        Params:
            size (int): size in points
            weight (int): weight in points, may be (str) like 'light'
            spacing (int): spacing in %, eg.: 110%
            family (str): font family.
        Return:
            font (object): PyQT5 object that handles font styling

        """
        # Creating font object and assigning values to it's size and family        
        font = QFont()
        font.setFamily(family)
        font.setPointSize(size)

        # Setting weight if specified
        if weight:
            font.setWeight(weight)
        # Setting spacing (in %) if specified
        if spacing:
            font.setLetterSpacing(QFont.PercentageSpacing, spacing)

        # Returning font object
        return font


    def eventFilter(self, source, event):
        """
            Method that listents for scroll events globally and hides active
            tooltip on event.
        """
        if event.type() == QEvent.Wheel and self.activeTooltip:
            self.activeTooltip.hide()
            self.activeTooltip = None
        return super().eventFilter(source, event)