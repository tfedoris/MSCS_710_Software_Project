import psutil
import pandas as pd


class ProcessMetricCollector:
    def __init__(self, logger, metrics):
        self.logger = logger
        self.metrics = metrics
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
                    "pid": process.pid,
                    "name": process.name(),
                    "startTime": process.create_time(),
                    "user": process.username(),
                    "status": process.status(),
                    "cpuUserTime": cpu_times.user,
                    "cpuKernelTime": cpu_times.system,
                    "cpuPercent": process.cpu_percent(cpu_collect_int),
                    "memoryPercentUsedByte": process.memory_percent(),
                    "memoryPhysicalUsedByte": p_memory_info.rss,
                    "memoryVirtualUsedByte": p_memory_info.vms,
                    "memoryUniqueUsedByte": p_memory_info.private,
                    "memoryNonPrivateByte": non_private_mem,
                    "memoryPageFault": p_memory_info.num_page_faults,
                    "ioReadCnt": p_io_info.read_count,
                    "ioReadBytes": p_io_info.read_bytes,
                    "ioWriteCnt": p_io_info.write_count,
                    "ioWriteBytes": p_io_info.write_bytes,
                    "threadNum": process.num_threads()
                }
                self.metrics_df.append(metrics_rec, ignore_index=True)
            except psutil.AccessDenied as ad:
                self.logger.error("Access denied to fetch information for {}".format(pid))
                self.logger.error(ad.args[0])

    def get_metrics_recs(self):
        return self.metrics_df
