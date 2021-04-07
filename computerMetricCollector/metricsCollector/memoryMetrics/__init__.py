import psutil
import pandas as pd
from datetime import datetime


class MemoryMetrics:
    def __init__(self, metrics, datetime_format):
        self.is_fetched = False
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)

    def fetch_metrics(self):
        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()
        memory_metrics = {
            "entry_datetime": datetime.now().strftime(self.datetime_format),
            "mem_total": virtual_mem.total,
            "mem_available": virtual_mem.available,
            "mem_used": virtual_mem.used,
            "swap_total": swap_mem.total,
            "swap_used": swap_mem.used,
            "swap_free": swap_mem.free,
            "swap_percent": swap_mem.percent,
        }
        self.metrics_df.append(memory_metrics, ignore_index=True)

    def get_metrics_df(self):
        return self.metrics_df
