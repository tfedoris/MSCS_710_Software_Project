import pandas as pd
import psutil
from datetime import datetime
from computerMetricCollector.metricsCollector import Collector


class DiskMetrics(Collector):
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
        self.logger.info("Start fetching for disk metrics")
        disks = psutil.disk_partitions()
        for disk in disks:
            self.logger.debug("Fetch desk: " + disk.device)
            if disk.opts == "rw,fixed":
                usage = psutil.disk_usage(disk.device)
                metric = {
                    "machine_id": self.machine_id,
                    "entry_time": datetime.now().strftime(self.datetime_format),
                    "disk_name": disk.device,
                    "total_bytes": usage.total,
                    "free_bytes": usage.free,
                    "used_bytes": usage.used,
                    "percent": usage.percent
                }
                self.metrics_df = self.metrics_df.append(metric, ignore_index=True)
                self.metrics_df = self.metrics_df.reset_index(drop=True)
            else:
                self.logger.debug("Avoid fetching desk: " + disk.device + " with mount option: " + disk.opts)
        self.logger.info("End fetching for disk metrics")
        self.is_fetched = True
        self.to_stored = True

    def get_metrics_df(self):
        """
        This function return the metrics data frame in collector instance
        :return: metrics data frame create from fetch metrics function
        """
        self.logger.info("Get metrics dataframe for disk metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        """
        This function resets the metrics data frame and enable the instance to fetch again
        :return:
        """
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
        self.is_fetched = False


class DiskIOMetrics(Collector):
    def __init__(self, logger, machine_id, metrics, metrics_to_encrypt, datetime_format, url):
        self.is_fetched = False
        self.to_stored = True
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
        self.logger.info("Start fetching for disk io metrics")
        disks_io = psutil.disk_io_counters(perdisk=True)
        for disk in disks_io.keys():
            self.logger.debug("Fetch for disk io metrics for disk: " + disk)
            io = disks_io.get(disk)
            metrics = {
                "machine_id": self.machine_id,
                "entry_time": datetime.now().strftime(self.datetime_format),
                "disk_name": disk,
                "count_read": io.read_count,
                "count_write": io.write_count,
                "bytes_read": io.read_bytes,
                "bytes_write": io.write_bytes,
                "time_read_in_milli": io.read_time,
                "time_write_in_milli": io.write_time
            }
            self.metrics_df = self.metrics_df.append(metrics, ignore_index=True)
            self.metrics_df = self.metrics_df.reset_index(drop=True)
        self.logger.info("End fetching for disk io metrics")
        self.is_fetched = True
        self.to_stored = True

    def get_metrics_df(self):
        """
        This function return the metrics data frame in collector instance
        :return: metrics data frame create from fetch metrics function
        """
        self.logger.info("Get metrics dataframe for disk io metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        """
        This function resets the metrics data frame and enable the instance to fetch again
        :return:
        """
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
        self.is_fetched = False
