import json
from pathlib import Path
import logging
import logging.config

from gui.main_window import *

# The main python file, used to launch the application. It configures logging
# then launches the PyQT5 app which does the rest of the work. 


def setup_logging():
    """
    Configures the logging settings for the application.
    """
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'fileHandler': {
                'class': 'logging.FileHandler',
                'filename': 'logs/logs.log',  
                'mode': 'a',  
                'formatter': 'detailed',  
            },
        },
        'formatters': {
            'detailed': {
                'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
            },
        },
        'loggers': {
            '': {  
                'handlers': ['fileHandler'],
                'level': 'INFO',  
                'propagate': True, 
            },
        }
    })

def initialise_datafiles():
    base_dir = Path(__file__).resolve().parent
    filenames = ["articles.json", "discarded.json", "archived.json"]
    for filename in filenames:
        path = base_dir / "data" / filename
        if not path.exists():
            empty_file = []
            with open(path, "w") as file:
                json.dump(empty_file, file)
                logging.info(f"Initialised {filename}.")
        else:
            pass


if __name__ == '__main__':
    setup_logging()
    initialise_datafiles()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())