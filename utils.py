import logging

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def log_success(message):
    logging.info(f"✅ {message}")

def log_failure(message):
    logging.error(f"❌ {message}")

def log_warning(message):
    logging.warning(f"⚠️ {message}")
