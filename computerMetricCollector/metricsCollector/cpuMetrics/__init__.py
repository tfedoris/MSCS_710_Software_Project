import pandas as pd
from cpuinfo import cpuinfo
from datetime import datetime
from computerMetricCollector.metricsCollector import Collector


class CPUMetrics(Collector):
    def __init__(self, logger, machine_id, metrics, metrics_to_encrypt, datetime_format, url):
        self.is_fetched = False
        self.to_stored = False
        self.logger = logger
        self.machine_id = machine_id
        self.datetime_format = datetime_format
        self.metrics_to_encrypt = metrics_to_encrypt
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.remote_url = url

    def fetch_metrics(self):
        """
        This function fetch the metrics to be store in the database
        :return:
        """
        self.logger.info("Is CPU metrics fetched: " + str(self.is_fetched))
        if not self.is_fetched:
            self.logger.info("Fetch for CPU metrics")
            info = cpuinfo.get_cpu_info()
            metrics_rec = {
                "machine_id": self.machine_id,
                "entry_time": datetime.now().strftime(self.datetime_format),
                "brand": info.get("brand_raw"),
                "vendor": info.get("vendor_id_raw"),
                "architecture": info.get("arch"),
                "bits": info.get("bits"),
                "hz_advertise": info.get("hz_advertised")[0],
                "hz_actual": info.get("hz_actual")[0],
                "core_count": info.get("count")
            }
            self.metrics_df = self.metrics_df.append(metrics_rec, ignore_index=True)
            self.metrics_df = self.metrics_df.reset_index(drop=True)
            self.is_fetched = True
            self.to_stored = True
        else:
            self.logger.info("No fetch for CPU metrics")

    def get_metrics_df(self):
        """
        This function return the metrics data frame in collector instance
        :return: metrics data frame create from fetch metrics function
        """
        self.logger.info("Get metrics dataframe for CPU metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        """
        This function resets the metrics data frame and enable the instance to fetch again
        :return:
        """
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
        self.is_fetched = False
