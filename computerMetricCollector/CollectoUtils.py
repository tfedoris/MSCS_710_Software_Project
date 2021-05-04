import logging
import requests
from psutil import AccessDenied
from logging.handlers import TimedRotatingFileHandler
from computerMetricCollector.dataCrypto import encrypt_data
from computerMetricCollector.metricsCollector import store_local, store_to_database
from computerMetricCollector.metricsCollector.cpuMetrics import CPUMetrics
from computerMetricCollector.metricsCollector.memoryMetrics import MemoryMetrics
from computerMetricCollector.metricsCollector.diskMetrics import DiskMetrics, DiskIOMetrics
from computerMetricCollector.metricsCollector.networkMetrics import NetworkMetrics
from computerMetricCollector.metricsCollector.processMetrics import ProcessMetrics


def get_logger(file, log_level, rotate_time, backup_cnt):
    """
    This method create the logger that will log the state of computer metrics collector
    :param file: The log file to write the log to
    :param log_level: The level of logger to write
    :param rotate_time: When the log rotates to write to new log file
    :param backup_cnt: The number of historical log to keep
    :return: The logger instance for writing the state of the software
    """
    logger_instance = logging.getLogger(__name__)
    log_handler = TimedRotatingFileHandler(filename=file, when=rotate_time, interval=1,
                                           backupCount=backup_cnt)
    logger_instance.setLevel(log_level)
    format_str = "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
    log_handler.setFormatter(logging.Formatter(format_str))
    logger_instance.addHandler(log_handler)
    logger_instance.info("Create logger instance")
    return logger_instance


def init_collector(logger, collectors_meta, collector_name, machine_id, datetime_format):
    collector_instance = None
    logger.debug("Start instantiate collector for " + collector_name)
    if globals().get(collector_name):
        collect_class = globals()[collector_name]
        metrics_to_collect = collectors_meta[collector_name]["metrics"]
        metrics_to_encrypt = collectors_meta[collector_name]["metrics_to_encrypt"]
        table = collectors_meta[collector_name]["table"]
        collector_instance = collect_class(logger, machine_id, metrics_to_collect, metrics_to_encrypt,
                                           datetime_format, table)
        logger.debug("End instantiate collector for " + collector_name)
    else:
        logger.warning("Collector " + collector_name + " is not supported yet.")
    return collector_instance


def persist_local(logger, file_path, collector):
    logger.info("Begin storing " + type(collector).__name__)
    csv_name = file_path + type(collector).__name__ + ".csv"
    store_local(collector, csv_name)
    logger.info("End storing " + type(collector).__name__)


def persist_database(logger, remote_store_dict, collectors):
    url = remote_store_dict.get("url")
    key = remote_store_dict.get("register_key")
    if (url is not None and key is not None) and (url != "" and key != ""):
        try:
            for collector in collectors:
                metrics_df = collector.get_metrics_df()
                data = metrics_df.to_dict(orient="list")
                post_data = {"key": key, "playload": data}
                requests.post(url, post_data=post_data)
        except Exception as e:
            logger.error(e.args[0])
    else:
        logger.error("Unknown url and/or Unknown register key")
        logger.error("URL: " + str(url))
        logger.error("Register Key: " + str(key))


def collect_metrics(logger, settings, encrypt_key, collectors, computer_collector):
    try:
        logger.info("Encrypt computer metrics")
        encrypt_data(computer_collector, encrypt_key)
        logger.info("Begin fetching metrics data from other collects and encrypting the collected metrics")
        for c in collectors:
            c.fetch_metrics()
            encrypt_data(c, encrypt_key)
        logger.info("End fetching and encrypting metrics data")
        logger.info("Begin persisting fetch metrics")
        logger.debug("To store metrics on local: " + str(settings["to_store_local"]))
        if settings["to_store_local"]:
            persist_local(logger,  settings["local_store_dir"], computer_collector)
            for c in collectors:
                persist_local(logger, settings["local_store_dir"], c)
        else:
            collectors.append(computer_collector)
            persist_database(logger, settings["database"], collectors)
    except AccessDenied as ad:
        logger.error("Access denied for fetch data from psutil library")
        logger.error(ad)
    except FileNotFoundError as fnfe:
        logger.error("Dependent file not found.")
        logger.error(fnfe)
    except Exception as e:
        logger.error(e.args[0])
