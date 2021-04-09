import psutil
import pandas as pd
from datetime import datetime


class ProcessMetrics:
    def __init__(self, logger, machine_id, metrics, datetime_format):
        self.logger = logger
        self.machine_id = machine_id
        self.metrics = metrics
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)

    def fetch_metrics(self):
        pid_arr = psutil.pids()
        for pid in pid_arr:
            process = psutil.Process(pid)
            try:
                p_memory_info = process.memory_info()
                non_private_mem = p_memory_info.wset - p_memory_info.private
                cpu_times = process.cpu_times()
                cpu_collect_int = 0.1
                if non_private_mem < 0:
                    non_private_mem = 0
                p_io_info = process.io_counters()
                metrics_rec = {
                    "MachineId"
                    "Pid": process.pid,
                    "Name": process.name(),
                    "StartTime": process.create_time(),
                    "User": process.username(),
                    "EntryDatetime": datetime.now().strftime(self.datetime_format),
                    "Status": process.status(),
                    "CPUUserTime": cpu_times.user,
                    "CPUKernelTime": cpu_times.system,
                    "CPUPercent": process.cpu_percent(cpu_collect_int),
                    "MemoryPercentUsedByte": process.memory_percent(),
                    "MemoryPhysicalUsedByte": p_memory_info.rss,
                    "MemoryVirtualUsedByte": p_memory_info.vms,
                    "MemoryUniqueUsedByte": p_memory_info.private,
                    "MemoryNonPrivateByte": non_private_mem,
                    "MemoryPageFault": p_memory_info.num_page_faults,
                    "IOReadCnt": p_io_info.read_count,
                    "IOReadBytes": p_io_info.read_bytes,
                    "IOWriteCnt": p_io_info.write_count,
                    "IOWriteBytes": p_io_info.write_bytes,
                    "ThreadNum": process.num_threads()
                }
                self.metrics_df.append(metrics_rec, ignore_index=True)
            except psutil.AccessDenied as ad:
                self.logger.error("Access denied to fetch information for {}".format(pid))
                self.logger.error(ad)

    def get_metrics_df(self):
        return self.metrics_df
