import logging
import requests

import config
from random import randint


class Research:
    def __init__(self, file_path: str):
        logging.info(f"Initializing Research class with file path: {file_path}")
        self.path = file_path

    def file_reader(self, has_header: bool = True) -> list[list[int]]:
        logging.info("Starting to read the file")
        try:
            with open(self.path, "r") as file:
                lines = file.readlines()

                if has_header:
                    lines = lines[1:]

                if not lines:
                    raise ValueError("The file has no data!")

                data = []
                for line in lines:
                    stripped_line = line.strip()
                    if not stripped_line:
                        continue
                    split_line = stripped_line.split(",")
                    if len(split_line) != 2 or not all(
                        item.isdigit() for item in split_line
                    ):
                        raise ValueError(
                            "File contains invalid or improperly formatted data"
                        )
                    data.append([int(x) for x in split_line])
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.path} does not exist")
        logging.info("File reading completed successfully")
        return data

    @staticmethod
    def send_telegram_message(message):
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": config.TELEGRAM_CHAT_ID, "text": message}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            logging.info("Telegram message sent successfully")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send Telegram message: {e}")

    class Calculations:
        def __init__(self, data: list[list[int]]):
            logging.info("Initializing Calculations Class")
            self.data = data

        def counts(self) -> tuple[int, int]:
            logging.info("Calculating counts of heads and tails")
            heads_count = sum(row[0] for row in self.data)
            tails_count = sum(row[1] for row in self.data)

            if heads_count == 0 and tails_count == 0:
                raise ValueError(
                    "Total amount of heads and tails is zero, no data to count"
                )

            logging.info("Successfully calculated counts and heads")
            return heads_count, tails_count

        @staticmethod
        def fractions(head_count: int, tails_count: int) -> tuple[float, float]:
            logging.info("Calculating fractions of heads and tails")
            total_amount = head_count + tails_count

            if total_amount == 0:
                raise ValueError("No data to calculate fractions")

            head_percent = (head_count / total_amount) * 100
            tails_percent = (tails_count / total_amount) * 100
            logging.info("Successfully calculated fractions")
            return head_percent, tails_percent


class Analytics(Research.Calculations):
    HEAD = [1, 0]
    TAIL = [0, 1]

    def __init__(self, data: list[list[int]]):
        logging.info(f"Initializing Analytics Class")
        super().__init__(data)

    def predict_random(self, number_of_predictions) -> list[list[int]]:
        logging.info(f"Predicting random values for {number_of_predictions} steps")
        return [
            self.HEAD if randint(0, 1) else self.TAIL
            for _ in range(number_of_predictions)
        ]

    def predict_last(self) -> list[int]:
        logging.info("Predicting last observation")
        if not self.data:
            raise ValueError("No data available to predict the last observation")
        return self.data[-1]

    @staticmethod
    def save_file(data: str, filename: str, extension: str):
        logging.info(f"Saving data to {filename}.{extension}")
        with open(f"{filename}.{extension}", "w") as output_file:
            output_file.write(data)
        logging.info("Data were successfully saved")
