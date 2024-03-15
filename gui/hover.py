from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QSize
import sys

class LoadingSpinner(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)  # Adjust window size as needed
        self.setWindowTitle('Spinner Example')

        # Make the background transparent
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")

        # Create and configure the spinner label
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        # Load and configure the spinner GIF
        self.spinner = QMovie("/Users/gabbai/news_ai/gui/resources/transp.gif")
        self.label.setMovie(self.spinner)
        self.spinner.setScaledSize(QSize(50, 50))
        self.spinner.start()

        # To adjust the spinner size directly, you might need to resize the GIF or use a QLabel size that fits your needs

        self.show()

def main():
    app = QApplication(sys.argv)
    ex = LoadingSpinner()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
