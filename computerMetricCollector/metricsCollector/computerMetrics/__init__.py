import platform
from datetime import datetime
import pandas as pd
import subprocess


def get_computer_id(logger):
    """
    This function fetch the computer id of the host machine
    :param logger: logger to log the process
    :return: string value represent the computer id
    """
    logger.info("Getting computer id")
    uuid_output = subprocess.check_output("wmic csproduct get UUID")
    uuid = str(uuid_output).split('\\r\\r\\n')[1].strip()
    logger.debug("Computer id: " + uuid)
    logger.info("End getting computer id")
    return uuid


class ComputerMetrics:
    """
    Computer metrics class will collect computer data
    """
    def __init__(self, logger, metrics, metrics_to_encrypt, datetime_format, url):
        """
        :param logger: logger instance to log the process
        :param metrics: list of metrics use to create the metrics data frame
        :param metrics_to_encrypt: list of metrics use to select columns to encrypt
        :param datetime_format: date format to parse datetime to string
        :param url: URL of api to store the computer metrics data
        """
        self.is_fetched = False
        self.to_stored = False
        self.logger = logger
        self.metrics_to_encrypt = metrics_to_encrypt
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.machine_id = get_computer_id(self.logger)
        self.datetime_format = datetime_format
        self.remote_url = url

    def fetch_metrics(self):
        """
        This function fetch the metrics to be store in the database
        :return:
        """
        self.logger.info("Is computer metrics fetched: " + str(self.is_fetched))
        if not self.is_fetched:
            self.logger.info("Fetch for computer metrics")
            machine_info = platform.uname()
            metrics = {
                "machine_id": self.machine_id,
                "entry_time": datetime.now().strftime(self.datetime_format),
                "machine_name": machine_info.node,
                "system_name": machine_info.system,
                "version": machine_info.version,
                "machine_type": machine_info.machine
            }
            self.metrics_df = self.metrics_df.append(metrics, ignore_index=True)
            self.metrics_df = self.metrics_df.reset_index(drop=True)
            self.is_fetched = True
            self.to_stored = True
        else:
            self.logger.info("No fetch for computer metrics")

    def get_metrics_df(self):
        """
        This function return the metrics data frame in collector instance
        :return: metrics data frame create from fetch metrics function
        """
        self.logger.info("Get metrics dataframe for computer metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        """
        This function resets the metrics data frame and enable the instance to fetch again
        :return:
        """
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
        self.is_fetched = False
