import pandas as pd
from cpuinfo import cpuinfo
from datetime import datetime


class CPUMetrics:
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
        self.logger.info("Is CPU metrics fetched: " + str(self.is_fetched))
        if not self.is_fetched:
            self.logger.info("Fetch for CPU metrics")
            info = cpuinfo.get_cpu_info()
            metrics_rec = {
                "MachineId": self.machine_id,
                "EntryDatetime": datetime.now().strftime(self.datetime_format),
                "Brand": info.get("brand_raw"),
                "Vendor": info.get("vendor_id_raw"),
                "Arch": info.get("arch"),
                "Bits": info.get("bits"),
                "HZAdvertise": info.get("hz_advertised")[0],
                "HZActual": info.get("hz_actual")[0],
                "Count": info.get("count")
            }
            self.metrics_df = self.metrics_df.append(metrics_rec, ignore_index=True)
            self.metrics_df = self.metrics_df.reset_index(drop=True)
            self.is_fetched = True
            self.to_stored = True
        else:
            self.logger.info("No fetch for CPU metrics")

    def get_metrics_df(self):
        self.logger.info("Get metrics dataframe for CPU metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
