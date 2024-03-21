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
from config.settings import kr_system, kr_username, app_description

# This module wraps most of the application logic. 
# The MainWindow handles most of the GUI elements and handles the bakcend logic
# with a backend thread. The 3 stages of the GUI are the:
#   1) the landing screen: that contains a welcome message and user-data entry 
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

        # API key check ahead of UI init
        self.check_for_api()


    def check_for_api(self):
        """ Checks for auth key then initialises UI """ 
        self.api_key = keyring.get_password(kr_system, kr_username)

        # Different inits depending on result
        if self.api_key:
            self.init_landing_api()
        else:
            self.init_landing_noapi()


    def init_landing_noapi(self):
        """ 
        Initialising UI when no auth key detected, usually on initial launch.
        """
        # Setting container widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Setting vertical layout
        main_v_layout = QVBoxLayout(main_widget)
        main_v_layout.setAlignment(Qt.AlignCenter)  # Horizontal alignment
        main_v_layout.setContentsMargins(50, 0, 50, 0) # Horizontal margins

        # Centering widgets vertically
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Adding top spacer, contents go between here and bottom spacer
        main_v_layout.addSpacerItem(top_spacer)

        # Adding welcome and introduction
        welcome_label = QLabel("Welcome to News-AI\nCreated by Gabai")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setFont(self.set_font(20))
        main_v_layout.addWidget(welcome_label)

        # Adding input field
        self.api_input = QLineEdit()
        self.api_input.setEchoMode(QLineEdit.Password)
        self.api_input.setPlaceholderText("Enter your OpenAI API key here...")
        main_v_layout.addWidget(self.api_input)

        # Adding Start button
        button = QPushButton("Start")
        button.setFont(self.set_font(14))
        button.clicked.connect(self.start_noapi)
        main_v_layout.addWidget(button)

        # Adding bottom spacer
        main_v_layout.addSpacerItem(bottom_spacer)


    def init_landing_api(self):
        """ Initialising UI when auth key exists. """
        # Setting container widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Setting vertical layout
        main_v_layout = QVBoxLayout(main_widget)
        main_v_layout.setAlignment(Qt.AlignCenter)  # Horizontal alignment
        main_v_layout.setContentsMargins(50, 0, 50, 0) # Horizontal margins


        # Centering widgets vertically
        top_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        bottom_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Adding top spacer, contents go between here and bottom spacer
        main_v_layout.addSpacerItem(top_spacer)

        # Adding welcome and introduction
        welcome_label = QLabel("Welcome to News-AI")
        welcome_label.setStyleSheet("color: #979797;")
        welcome_label.setFont(self.set_font(20))
        welcome_label.setAlignment(Qt.AlignCenter)
        main_v_layout.addWidget(welcome_label)

        # Adding description 
        description_label = QLabel(app_description)
        description_label.setFont(self.set_font(14))
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("color: #979797;")
        main_v_layout.addWidget(description_label)

        # Adding Start button
        button = QPushButton("Start")
        button.setFont(self.set_font(14))
        # button.setMaximumWidth(200)
        button.setStyleSheet("color: #979797;")
        button.clicked.connect(self.start_api)
        button_h_layout = QHBoxLayout()
        button_h_layout.setAlignment(Qt.AlignCenter)
        button_h_layout.addWidget(button)
        main_v_layout.addLayout(button_h_layout)

        # Adding bottom spacer
        main_v_layout.addSpacerItem(bottom_spacer)


        # Adding signature label and signature
        signature_h_layout = QHBoxLayout()
        signature_h_layout.setAlignment(Qt.AlignCenter)
        main_v_layout.addLayout(signature_h_layout)
        signature_label = QLabel("Created by:")
        signature_label.setFont(self.set_font(12))
        signature_label.setAlignment(Qt.AlignCenter)
        signature_h_layout.addWidget(signature_label)
        signature_label = QLabel("Gabai")
        signature_label.setFont(self.set_font(14, family="Brush Script MT"))
        signature_label.setAlignment(Qt.AlignCenter)
        signature_h_layout.addWidget(signature_label)


    def start_noapi(self):
        # Retrieving text from input field
        self.api_key = self.api_input.text()

        # Checking for text
        if not self.api_key:
            print("You must enter an OpenAI API Key.")

        # Pinging OpenAI to validate auth key
        elif not self.check_api_key(self.api_key):
            print("API Key invalid! Enter a valid OpenAI API Key.")

        # Saving auth key and starting program given response is '200'
        else:
            keyring.set_password(system, username, self.api_key)
            self.init_loading_screen()
            self.start_background_task()


    def start_api(self):
        # Pingin OpenAI to validate auth key
        if not self.check_api_key(self.api_key):
            print("API Key invalid! Sorry for the inconvenience")

        # Starting program given response is '200'
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
        # Clearing central widget from previous screen
        self.takeCentralWidget() 

        # Creating 
        self.tabs = QTabWidget() # Create tabs
        self.setCentralWidget(self.tabs)
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
                label = CustomLabel(summary, article, self)
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
