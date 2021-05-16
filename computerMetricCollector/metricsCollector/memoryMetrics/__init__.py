import psutil
import pandas as pd
from datetime import datetime
from computerMetricCollector.metricsCollector import Collector


class MemoryMetrics(Collector):
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
        self.logger.info("Start fetching for memory metrics")
        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()
        memory_metrics = {
            "machine_id": self.machine_id,
            "entry_time": datetime.now().strftime(self.datetime_format),
            "memory_total": virtual_mem.total,
            "memory_available": virtual_mem.available,
            "memory_used": virtual_mem.used,
            "memory_used_percent": virtual_mem.percent,
            "swap_total": swap_mem.total,
            "swap_free": swap_mem.used,
            "swap_used": swap_mem.free,
            "swap_percent": swap_mem.percent,
            "swap_byte_in": swap_mem.sin,
            "swap_byte_out": swap_mem.sout,
        }
        self.metrics_df = self.metrics_df.append(memory_metrics, ignore_index=True)
        self.metrics_df = self.metrics_df.reset_index(drop=True)
        self.logger.info("End fetching for memory metrics")
        self.is_fetched = True
        self.to_stored = True

    def get_metrics_df(self):
        """
        This function return the metrics data frame in collector instance
        :return: metrics data frame create from fetch metrics function
        """
        self.logger.info("Get metrics dataframe for memory metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        """
        This function resets the metrics data frame and enable the instance to fetch again
        :return:
        """
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
        self.is_fetched = False
