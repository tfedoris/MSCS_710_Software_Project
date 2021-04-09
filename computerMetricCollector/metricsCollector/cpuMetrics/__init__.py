import pandas as pd
from cpuinfo import cpuinfo
from datetime import datetime


class CPUMetrics:
    def __init__(self, logger, machine_id, metrics, datetime_format):
        self.is_fetched = False
        self.logger = logger
        self.machine_id = machine_id
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)

    def fetch_metrics(self):
        if not self.is_fetched:
            info = cpuinfo.get_cpu_info()
            metrics_rec = {
                "MachineId": self.machine_id,
                "EntryDatetime": datetime.now().strftime(self.datetime_format),
                "Brand": info.get("brand_raw"),
                "Vendor": info.get("vendor_id_raw"),
                "Arch": info.get("arch"),
                "Bits": info.get("bits"),
                "HZAdvertise": info.get("hz_advertised"),
                "HZActual": info.get("hz_actual"),
                "Count": info.get("count")
            }
            self.metrics_df.append(metrics_rec, ignore_index=True)

    def get_metrics_df(self):
        return self.metrics_df
