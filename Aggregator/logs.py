import logging
from logging.handlers import RotatingFileHandler
import os

log_directory = "./logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, "app.log")

# Create a logger
logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO)  # Set the logging level

# Create a file handler that logs even debug messages
handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(handler)