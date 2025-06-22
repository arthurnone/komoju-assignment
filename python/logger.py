import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Logs to console
        logging.FileHandler("komoju_assignment.log", mode="a")  # Logs to file
    ]
)

# Create a logger instance
logger = logging.getLogger("komoju-assignment")
