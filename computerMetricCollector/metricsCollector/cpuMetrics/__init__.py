import pandas as pd
from cpuinfo import cpuinfo
from datetime import datetime


class CPUMetrics:
    def __init__(self, metrics, datetime_format):
        self.is_fetched = False
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)

    def fetch_metrics(self):
        if not self.is_fetched:
            info = cpuinfo.get_cpu_info()
            metrics_rec = {
                "entry_datetime": datetime.now().strftime(self.datetime_format),
                "brand": info.get("brand_raw"),
                "vendor": info.get("vendor_id_raw"),
                "arch": info.get("arch"),
                "bits": info.get("bits"),
                "hz_advertise": info.get("hz_advertised"),
                "hz_actual": info.get("hz_actual"),
                "count": info.get("count")
            }
            self.metrics_df.append(metrics_rec, ignore_index=True)
        return self.metrics_df
