import logging

import config
import analytics


def generate_report():
    logging.info("Starting report generation")
    # Read data using Research class
    research = analytics.Research(config.DATA_FILE_PATH)
    data = research.file_reader()

    # Perform calculations
    calculations = research.Calculations(data)
    heads, tails = calculations.counts()
    head_fraction, tails_fraction = calculations.fractions(heads, tails)

    # Generate predictions
    analytics_obj = analytics.Analytics(data)
    random_predictions = analytics_obj.predict_random(config.NUM_OF_STEPS)

    # Prepare forecast summary
    forecast_heads = sum(item[0] for item in random_predictions)
    forecast_tails = sum(item[1] for item in random_predictions)

    # Prepare the report using the template
    report = config.REPORT_TEMPLATE.format(
        len(data),
        tails,
        heads,
        tails_fraction,
        head_fraction,
        config.NUM_OF_STEPS,
        forecast_tails,
        forecast_heads,
    )

    # Save the report to a file
    analytics_obj.save_file(
        report, config.REPORT_FILE_NAME, config.REPORT_FILE_EXTENSION
    )

    analytics.Research.send_telegram_message("The report has been successfully created")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        filename=config.LOGGING_FILE_NAME,
        filemode="w",
        format="%(asctime)s %(message)s",
    )
    try:
        generate_report()
    except Exception as e:
        logging.error(f"[ERROR]: {e}")
        analytics.Research.send_telegram_message(
            "The report hasn’t been created due to an error"
        )
        print(f"An error occurred: {e}")
