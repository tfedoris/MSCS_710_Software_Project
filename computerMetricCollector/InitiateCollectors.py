import os
import config
import logging
from time import sleep
from logging.handlers import TimedRotatingFileHandler
from metricsCollector import MetricsCollector


def get_logger(file, log_level, rotateTime, backup_cnt):
    logger = logging.getLogger(__name__)
    log_handler = TimedRotatingFileHandler(filename=file, when=rotateTime, interval=1,
                                           backupCount=backup_cnt)
    logger.setLevel(log_level)
    format_str = "%(asctime)s - %(filename)s - %(levelname)s - Session %(uuid)s - %(message)s"
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
    all_metrics = {}
    all_statics = {}
    metrics_meta = settings.get("all_metrics")
    for metrics in metrics_meta:
        all_metrics[metrics] = metrics_meta[metrics].get("metrics")
    metrics_collector = MetricsCollector(logger, all_metrics)
    while True:
        metrics_collector.collect_metrics()
        sleep(settings.get("sleep_time_sec"))
