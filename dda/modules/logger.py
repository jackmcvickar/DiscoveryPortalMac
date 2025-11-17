import os
import configparser
import logging

def load_config():
    config = configparser.ConfigParser()
    # Go up one directory from modules/ to reach dda/config.ini
    config.read(os.path.join(os.path.dirname(__file__), "..", "config.ini"))
    return config

def setup_logger(name="dda"):
    cfg = load_config()
    logs_path = cfg["paths"]["logs_path"]

    os.makedirs(logs_path, exist_ok=True)
    log_file = os.path.join(logs_path, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(fh)

    return logger

def main():
    logger = setup_logger()
    logger.info("Logger initialized and ready.")
    print("📝 Logger is writing to config-defined logs directory.")

if __name__ == "__main__":
    main()
# end of script