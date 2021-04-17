# from ctypes import WinError
from datetime import datetime
import pandas as pd
import psutil


class DiskMetrics:
    def __init__(self, logger, machine_id, metrics, datetime_format, table):
        self.is_fetched = False
        self.to_stored = False
        self.logger = logger
        self.machine_id = machine_id
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.store_table = table

    def fetch_metrics(self):
        self.logger.info("Start fetching for disk metrics")
        disks = psutil.disk_partitions()
        for disk in disks:
            self.logger.debug("Fetch desk: " + disk.device)
            if disk.opts == "rw,fixed":
                usage = psutil.disk_usage(disk.device)
                metric = {
                    "MachineID": self.machine_id,
                    "DiskName": disk.device,
                    "EntryDatetime": datetime.now().strftime(self.datetime_format),
                    "Total": usage.total,
                    "Free": usage.free,
                    "Used": usage.used,
                    "Percent": usage.percent
                }
                self.metrics_df = self.metrics_df.append(metric, ignore_index=True)
            else:
                self.logger.debug("Avoid fetching desk: " + disk.device + " with mount option: " + disk.opts)
        self.logger.info("End fetching for disk metrics")
        self.is_fetched = True
        self.to_stored = True

    def get_metrics_df(self):
        self.logger.info("Get metrics dataframe for disk metrics")
        return self.metrics_df


class DiskIOMetrics:
    def __init__(self, logger, machine_id, metrics, datetime_format, table):
        self.is_fetched = False
        self.to_stored = True
        self.logger = logger
        self.machine_id = machine_id
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.store_table = table

    def fetch_metrics(self):
        self.logger.info("Start fetching for disk io metrics")
        disks_io = psutil.disk_io_counters(perdisk=True)
        for disk in disks_io.keys():
            self.logger.debug("Fetch for disk io metrics for disk: " + disk)
            io = disks_io.get(disk)
            metrics = {
                "MachineId": self.machine_id,
                "DiskName": disk,
                "EntryDatetime": datetime.now().strftime(self.datetime_format),
                "CountRead": io.read_count,
                "CountWrite": io.write_count,
                "BytesRead": io.read_bytes,
                "BytesWrite": io.write_bytes,
                "TimeReadInMilli": io.read_time,
                "TimeWriteInMilli": io.write_time
            }
            self.metrics_df.append(metrics, ignore_index=True)
        self.logger.info("End fetching for disk io metrics")
        self.is_fetched = True
        self.to_stored = True

    def get_metrics_df(self):
        self.logger.info("Get metrics dataframe for disk io metrics")
        return self.metrics_df
