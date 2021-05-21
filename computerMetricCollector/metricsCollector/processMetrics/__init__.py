import psutil
import pandas as pd
from datetime import datetime
from computerMetricCollector.metricsCollector import Collector


class ProcessMetrics(Collector):
    def __init__(self, logger, machine_id, metrics, metrics_to_encrypt, datetime_format, url):
        self.is_stored = False
        self.is_stored_locally = False
        self.logger = logger
        self.machine_id = machine_id
        self.metrics_to_encrypt = metrics_to_encrypt
        self.datetime_format = datetime_format
        self.metrics_df = pd.DataFrame(columns=metrics)
        self.remote_url = url

    def fetch_metrics(self):
        """
        This function fetch the metrics to be store in the database
        :return:
        """
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
                    "machine_id": self.machine_id,
                    "entry_time": datetime.now().strftime(self.datetime_format),
                    "pid": process.pid,
                    "name": process.name(),
                    "start_time": process.create_time(),
                    "start_user": process.username(),
                    "process_status": process.status(),
                    "cpu_user_time": cpu_times.user,
                    "cpu_kernel_time": cpu_times.system,
                    "cpu_percent": process.cpu_percent(cpu_collect_int),
                    "memory_percent_used_byte": process.memory_percent(),
                    "memory_physical_used_byte": p_memory_info.rss,
                    "memory_virtual_used_byte": p_memory_info.vms,
                    "memory_unique_used_byte": p_memory_info.private,
                    "memory_page_fault": p_memory_info.num_page_faults,
                    "io_read_count": p_io_info.read_count,
                    "io_read_bytes": p_io_info.read_bytes,
                    "io_write_count": p_io_info.write_count,
                    "io_write_bytes": p_io_info.write_bytes,
                    "thread_num": process.num_threads()
                }
                self.metrics_df = self.metrics_df.append(metrics_rec, ignore_index=True)
                self.metrics_df = self.metrics_df.reset_index(drop=True)
            except psutil.AccessDenied as ad:
                self.logger.warning("Access denied to fetch process metrics for pid {}".format(str(pid)))
                self.logger.warning(ad)
            except psutil.NoSuchProcess as nsp:
                self.logger.warning("No process found for pid {}".format(str(pid)))
                self.logger.warning(nsp)
            except Exception as e:
                self.logger.error(e)
        self.logger.info("End fetching for process metrics")

    def get_metrics_df(self):
        """
        This function return the metrics data frame in collector instance
        :return: metrics data frame create from fetch metrics function
        """
        self.logger.info("Get metrics dataframe for network metrics")
        return self.metrics_df

    def reset_metrics_df(self):
        """
        This function resets the metrics data frame and enable the instance to fetch again
        :return:
        """
        self.logger.info("Reset in memory dataframe for collector " + type(self).__name__)
        self.metrics_df = pd.DataFrame(columns=self.metrics_df.columns)
        self.is_stored = False
        self.is_stored_locally = False
