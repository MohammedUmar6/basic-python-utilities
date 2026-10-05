import csv
import json
import statistics
from datetime import datetime
from typing import Any, Callable, Dict, List, Tuple


def load_csv(path: str) -> List[Dict[str, str]]:
    with open(path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def filter_rows(
    data: List[Dict[str, str]], column: str, predicate: Callable[[str], bool]
) -> List[Dict[str, str]]:
    return [row for row in data if column in row and predicate(row[column])]


def column_stats(data: List[Dict[str, str]], column: str) -> Tuple[float, float, int]:
    numeric_values = []

    for row in data:
        try:
            value = float(row[column])
            numeric_values.append(value)
        except (ValueError, TypeError, KeyError):
            continue

    count = len(numeric_values)

    if count == 0:
        return (0.0, 0.0, 0)

    mean = statistics.mean(numeric_values)
    median = statistics.median(numeric_values)

    return (mean, median, count)


def write_json(data: Any, path: str) -> None:
    with open(path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


class SimpleLogger:
    def __init__(self, path: str = "app.log"):
        self.path = path

    def _write_log(self, level: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"{timestamp} - {level} - {message}\n"

        with open(self.path, mode="a", encoding="utf-8") as file:
            file.write(log_line)

    def info(self, message: str) -> None:
        self._write_log("INFO", message)

    def warning(self, message: str) -> None:
        self._write_log("WARNING", message)

    def error(self, message: str) -> None:
        self._write_log("ERROR", message)


if __name__ == "__main__":
    logger = SimpleLogger()

    try:
        logger.info("Starting CSV processing workflow.")

        data = load_csv("data.csv")
        logger.info(f"CSV loaded successfully. Rows: {len(data)}")

        filtered_data = filter_rows(
            data,
            "Age",
            lambda value: value.replace(".", "", 1).isdigit() and float(value) > 25,
        )

        logger.info(f"Filtering completed. Rows remaining: {len(filtered_data)}")

        mean, median, count = column_stats(data, "Age")

        logger.info(
            f"Age statistics calculated. "
            f"Mean: {mean}, Median: {median}, Count: {count}"
        )

        write_json(filtered_data, "filtered_data.json")
        logger.info("Filtered data written to filtered_data.json")

        logger.info("CSV processing workflow completed successfully.")

    except FileNotFoundError:
        logger.error("The input CSV file was not found.")

    except Exception as error:
        logger.error(f"An unexpected error occurred: {error}")
