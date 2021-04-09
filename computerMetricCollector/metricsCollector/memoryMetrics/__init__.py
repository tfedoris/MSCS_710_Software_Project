import psutil
import pandas as pd
from datetime import datetime


class MemoryMetrics:
    def __init__(self, logger, machine_id, metrics, datetime_format):
        self.is_fetched = False
        self.logger = logger
        self.macine_id = machine_id
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)

    def fetch_metrics(self):
        virtual_mem = psutil.virtual_memory()
        swap_mem = psutil.swap_memory()
        memory_metrics = {
            "MachineId": self.macine_id,
            "EntryDatetime": datetime.now().strftime(self.datetime_format),
            "MemoryTotal": virtual_mem.total,
            "MemoryAvailable": virtual_mem.available,
            "MemoryUsed": virtual_mem.used,
            "MemoryUsedPercent": virtual_mem.percent,
            "SwapTotal": swap_mem.total,
            "SwapFree": swap_mem.used,
            "SwapUsed": swap_mem.free,
            "SwapPercent": swap_mem.percent,
            "SwapBytesIn": swap_mem.sin,
            "SwapBytesOut": swap_mem.sout,
        }
        self.metrics_df.append(memory_metrics, ignore_index=True)

    def get_metrics_df(self):
        return self.metrics_df
