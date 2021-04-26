import platform
from datetime import datetime
import pandas as pd
import subprocess
from computerMetricCollector.dataCrypto import encrypt_data


def get_computer_id(logger):
    logger.info("Getting computer id")
    uuid_output = subprocess.check_output("wmic csproduct get UUID")
    uuid = str(uuid_output).split('\\r\\r\\n')[1].strip()
    logger.info("End getting computer id")
    return uuid


class ComputerMetrics:
    def __init__(self, logger, metrics, metrics_to_encrypt, datetime_format):
        self.is_fetched = False
        self.to_stored = False
        self.logger = logger
        self.metrics_to_encrypt = metrics_to_encrypt
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.machine_id = get_computer_id(self.logger)
        self.datetime_format = datetime_format

    def fetch_metrics(self):
        self.logger.info("Is computer metrics fetched: " + str(self.is_fetched))
        if not self.is_fetched:
            self.logger.info("Fetch for computer metrics")
            machine_info = platform.uname()
            metrics = {
                "MachineID": self.machine_id,
                "EntryDatetime": datetime.now().strftime(self.datetime_format),
                "MachineName": machine_info.node,
                "System": machine_info.system,
                "Version": machine_info.version,
                "MachineType": machine_info.machine
            }
            self.metrics_df = self.metrics_df.append(metrics, ignore_index=True)
            self.is_fetched = True
            self.to_stored = True
        else:
            self.logger.info("No fetch for computer metrics")

    def get_metrics_df(self):
        self.logger.info("Get metrics dataframe for computer metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
