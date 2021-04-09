from ctypes import WinError
from datetime import datetime
import pandas as pd
import psutil


class DiskMetrics:
    def __init__(self, logger, machine_id, metrics, datetime_format):
        self.is_fetched = False
        self.logger = logger
        self.machine_id = machine_id
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)

    def fetch_metrics(self):
        disks = psutil.disk_partitions()
        try:
            for disk in disks:
                usage = psutil.disk_usage(disk.device)
                metric = {
                    "MachineID": self.machine_id,
                    "DiskName": disk,
                    "EntryDatetime": datetime.now().strftime(self.datetime_format),
                    "Total": usage.total,
                    "Free": usage.free,
                    "Used": usage.used,
                    "Percent": usage.percent
                }
                self.metrics_df.append(metric, ignore_index=True)
        except PermissionError as pe:
            self.logger.warning("Permission denied to get disk data")
            self.logger.warning(pe)
        except Exception as e:
            self.logger.error(e)

    def get_metrics_df(self):
        return self.metrics_df


class DiskIOMetrics:
    def __init__(self, logger, machine_id, metrics, datetime_format):
        self.is_fetched = False
        self.logger = logger
        self.machine_id = machine_id
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)

    def fetch_metrics(self):
        disks_io = psutil.disk_io_counters(perdisk=True)
        for disk in disks_io.keys():
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

    def get_metrics_df(self):
        return self.metrics_df
