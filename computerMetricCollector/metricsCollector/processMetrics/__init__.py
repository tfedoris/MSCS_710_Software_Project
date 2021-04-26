import psutil
import pandas as pd
from datetime import datetime


class ProcessMetrics:
    def __init__(self, logger, machine_id, metrics, metrics_to_encrypt, datetime_format, table):
        self.is_fetch = True
        self.to_stored = True
        self.logger = logger
        self.machine_id = machine_id
        self.metrics_to_encrypt = metrics_to_encrypt
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.store_table = table

    def fetch_metrics(self):
        self.logger.info("Start fetching for process metrics")
        pid_arr = psutil.pids()
        for pid in pid_arr:
            try:
                self.logger.debug("Fetching process metrics for process pid " + str(pid))
                process = psutil.Process(pid)
                self.logger.debug("Fetching process metrics for process name " + process.name())
                p_memory_info = process.memory_info()
                cpu_times = process.cpu_times()
                cpu_collect_int = 0.1
                #    non_private_mem = 0
                p_io_info = process.io_counters()
                metrics_rec = {
                    "MachineId": self.machine_id,
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
                    "MemoryPageFault": p_memory_info.num_page_faults,
                    "IOReadCnt": p_io_info.read_count,
                    "IOReadBytes": p_io_info.read_bytes,
                    "IOWriteCnt": p_io_info.write_count,
                    "IOWriteBytes": p_io_info.write_bytes,
                    "ThreadNum": process.num_threads()
                }
                self.metrics_df = self.metrics_df.append(metrics_rec, ignore_index=True)
            except psutil.AccessDenied as ad:
                self.logger.warning("Access denied to fetch process metrics for pid {}".format(str(pid)))
                self.logger.warning(ad)
            except psutil.NoSuchProcess as nsp:
                self.logger.warning("No process found for pid {}".format(str(pid)))
                self.logger.warning(nsp)
            except Exception as e:
                self.logger.error(e)
        self.logger.info("End fetching for process metrics")
        self.is_fetch = True
        self.to_stored = True

    def get_metrics_df(self):
        self.logger.info("Get metrics dataframe for network metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
