import logging
from datetime import datetime

from psutil import AccessDenied
from logging.handlers import TimedRotatingFileHandler
from computerMetricCollector.crypto import encrypt_data
from computerMetricCollector.metricsCollector.StorageAPI import store_local, store_to_database, register_machine
from computerMetricCollector.metricsCollector.computerMetrics import ComputerMetrics
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
    log_handler = TimedRotatingFileHandler(filename=file, when=rotate_time, interval=1, backupCount=backup_cnt)
    logger_instance.setLevel(log_level)
    format_str = "%(asctime)s - %(filename)s - %(lineno)d  - %(levelname)s - %(message)s"
    log_handler.setFormatter(logging.Formatter(format_str))
    logger_instance.addHandler(log_handler)
    return logger_instance


def init_collector(logger, collectors_meta, collector_name, machine_id, datetime_format):
    """
    This function instantiate a collector child class based the given input
    :param logger: the logger instance for writing the state of the software
    :param collectors_meta: dictionary of meta data of the collector use to create the collector instance
    :param collector_name: name of the collector to instantiate
    :param machine_id: id of the machine to associate with each collector
    :param datetime_format: datetime format used to parse datetime object
    :return:
    """
    collector_instance = None
    logger.debug("Start instantiate collector for " + collector_name)
    if globals().get(collector_name):
        collect_class = globals()[collector_name]
        metrics_to_collect = collectors_meta[collector_name]["metrics"]
        metrics_to_encrypt = collectors_meta[collector_name]["metrics_to_encrypt"]
        url = collectors_meta[collector_name]["url"]
        collector_instance = collect_class(logger, machine_id, metrics_to_collect, metrics_to_encrypt,
                                           datetime_format, url)
        logger.debug("End instantiate collector for " + collector_name)
    else:
        logger.warning("Collector " + collector_name + " is not supported yet.")
    return collector_instance


def persist_local(logger, file_path, collectors):
    """
    This function prepare to store the collected data frames to local directory
    :param logger: the logger instance for writing the state of the software
    :param file_path: file path of the directory to store the csv
    :param collector: collector with the data frame to store
    :return:
    """
    logger.info("Begin storing performance data locally.")
    for c in collectors:
        csv_name = file_path + type(c).__name__ + ".csv"
        store_local(c, csv_name)
    logger.info("end storing performance data locally.")


def persist_database(logger, config, encrypt_key, collectors):
    """
    THis function prepare to store each collector in the list of collectors to the remote database based on the
    configured values
    :param logger: the logger instance for writing the state of the software
    :param config: dictionary of configured values
    :param collectors: list of collectors to store
    :return:
    """
    reg_id = config.get("registration_id")
    register_url = config.get("register_url")
    now = datetime.now().strftime(config.get("date_time_format"))
    machine_id = collectors[0].machine_id
    register_machine(logger, register_url, reg_id, machine_id, now)
    if reg_id is not None and reg_id != "":
        for collector in collectors:
            store_to_database(collector, reg_id)
    else:
        logger.error("Missing register key")
        logger.error("Registration ID: " + str(reg_id))


def reset_collectors(logger, collectors):
    logger.info("Reset fetched and persisted collector to prepare for next round of collection")
    for c in collectors:
        if c.is_stored and c.is_stored_locally:
            c.reset_metrics_df()


def create_computer_collector(logger, collectors_meta, datetime_format):
    """
    This function instantiated a collector object for the computer metrics collector
    :param logger: the logger instance for writing the state of the software
    :param collectors_meta: dictionary of meta data for creating computer metrics collector
    :param datetime_format: datetime format used to parse datetime object
    :return:
    """
    com_metrics_to_collect = collectors_meta["ComputerMetrics"]["metrics"]
    com_metrics_to_encrypt = collectors_meta["ComputerMetrics"]["metrics_to_encrypt"]
    com_url = collectors_meta["ComputerMetrics"]["url"]
    computer_collector = ComputerMetrics(logger, com_metrics_to_collect, com_metrics_to_encrypt, datetime_format,
                                         com_url)
    return computer_collector


def collect_metrics(logger, settings, encrypt_key, collectors):
    """
    This function fetch, encrypted and persist metrics data for each collector in the collector list. It will first
    fetch and encrypt for each collector. Then, the data is persist to either local or remote database depending on
    the configured value
    :param logger: the logger instance for writing the state of the software
    :param settings: dictionary of configured values
    :param encrypt_key: public key use in the encryption
    :param collectors: list of collectors
    :return:
    """
    try:
        logger.info("Begin fetching metrics data from other collects")
        print("Start fetching metrics data")
        for c in collectors:
            c.fetch_metrics()
        print("End fetching metrics data")
        logger.info("End fetching metrics data")
        logger.info("Begin persisting fetched metrics")
        logger.debug("To store metrics on local: " + str(settings["to_store_local"]))
        # Store a copy of metrics data if the user want them.
        if settings["to_store_local"]:
            print("Start storing metrics data to local data directory")
            persist_local(logger, settings.get("root_dir") + settings["local_store_dir"], collectors)
            print("End storing metrics data to local data directory")

        print("Start storing metrics data to remote database")
        persist_database(logger, settings, encrypt_key, collectors)
        print("End storing metrics data to remote database")
        logger.info("Finish persisting fetched metrics")

        reset_collectors(logger, collectors)
    except AccessDenied as ad:
        logger.error("Access denied for fetch data from psutil library")
        logger.error(ad)
    except FileNotFoundError as fnfe:
        logger.error("Dependent file not found.")
        logger.error(fnfe)
    except Exception as e:
        logger.error(e.args[0])
