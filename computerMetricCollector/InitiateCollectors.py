import os
import config
import logging
from time import sleep
from logging.handlers import TimedRotatingFileHandler
from computerMetricCollector.metricsCollector.computerMetrics import ComputerMetrics
from computerMetricCollector.metricsCollector.cpuMetrics import CPUMetrics
from computerMetricCollector.metricsCollector.diskMetrics import DiskMetrics, DiskIOMetrics
from computerMetricCollector.metricsCollector.memoryMetrics import MemoryMetrics
from computerMetricCollector.metricsCollector.networkMetrics import NetworkMetrics
from computerMetricCollector.metricsCollector.processMetrics import ProcessMetrics



def get_logger(file, log_level, rotateTime, backup_cnt):
    logger = logging.getLogger(__name__)
    log_handler = TimedRotatingFileHandler(filename=file, when=rotateTime, interval=1,
                                           backupCount=backup_cnt)
    logger.setLevel(log_level)
    format_str = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    log_handler.setFormatter(logging.Formatter(format_str))
    logger.addHandler(log_handler)
    return logger


if __name__ == "__main__":
    abs_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(abs_path)
    settings = config.import_config(root_dir)
    log_file = root_dir + "\\log\\" + settings.get("log_file")
    logger = get_logger(log_file, settings.get("log_level"), settings.get("log_rotate_time"),
                        settings.get("log_backup_cnt"))
    collectors_meta = settings.get("collectors")
    datetime_format = settings.get("date_time_format")
    computer_collector = ComputerMetrics(logger, collectors_meta.get("ComputerMetrics"))
    collectors = []
    del collectors_meta["ComputerMetrics"]
    for metrics_to_collect in collectors_meta.keys():
        collect_class = globals()[metrics_to_collect]
        collect_class_metrics = collectors_meta[metrics_to_collect]["metrics"]
        collector = collect_class(logger, computer_collector.machine_id, collect_class_metrics, datetime_format)
        collectors.append(collector)

    while True:
        for collector in collectors:
            collector.fetch_metrics()
        for collector in collectors:
            print(collector.get_metrics_df())
        sleep(settings.get("sleep_time_sec"))
