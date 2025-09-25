import os


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError(
        "Telegram bot token or chat ID is not set in environment variables"
    )

DATA_FILE_PATH = "../ex01/data.csv"
NUM_OF_STEPS = 3
REPORT_FILE_NAME = "report"
REPORT_FILE_EXTENSION = "txt"
LOGGING_FILE_NAME = "analytics.log"
REPORT_TEMPLATE = (
    "Report\n\n"
    "We have made {} observations from tossing a coin: {} of them were tails and {} of them were heads.\n"
    "The probabilities are {:.2f}% and {:.2f}%, respectively. Our forecast is that in the next {} observations\n"
    "we will have: {} tail and {} heads."
)
