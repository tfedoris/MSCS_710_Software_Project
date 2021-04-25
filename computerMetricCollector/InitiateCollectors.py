import os
import config
import logging
import argparse
from psutil import AccessDenied
from time import sleep
from logging.handlers import TimedRotatingFileHandler
from computerMetricCollector.dataCrypto import encrypt_data
from computerMetricCollector.dbConnector import MYSQLConnector
from computerMetricCollector.metricsCollector import store_local, store_to_database
from computerMetricCollector.metricsCollector.computerMetrics import ComputerMetrics
from computerMetricCollector.metricsCollector.cpuMetrics import CPUMetrics
from computerMetricCollector.metricsCollector.memoryMetrics import MemoryMetrics
from computerMetricCollector.metricsCollector.diskMetrics import DiskMetrics, DiskIOMetrics
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
    # Defines arguments to be passed in when running the program
    parser = argparse.ArgumentParser(description="Initiate Collector to collect metrics")
    parser.add_argument("-t", "--test", required=False,
                        help="Boolean value to enable collector to run in test mode",
                        default=False)
    args = parser.parse_args()
    is_test = args.test

    abs_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(abs_path)
    settings = config.import_config(root_dir)
    log_file = root_dir + "\\log\\" + settings.get("log_file")
    logger = get_logger(log_file, settings.get("log_level"), settings.get("log_rotate_time"),
                        settings.get("log_backup_cnt"))
    logger.info("Beginning to collect computer metrics from localhost")
    collectors_meta = settings.get("collectors")
    datetime_format = settings.get("date_time_format")
    metrics_to_collect = collectors_meta["ComputerMetrics"]["metrics"]
    metrics_to_encrypt = collectors_meta["ComputerMetrics"]["metrics_to_encrypt"]
    logger.info("Start collecting system information")
    computer_collector = ComputerMetrics(logger, metrics_to_collect, metrics_to_encrypt, datetime_format)
    computer_collector.fetch_metrics()
    collectors = []
    # Computer Metrics does not need to be fetch again
    del collectors_meta["ComputerMetrics"]
    to_collect = []
    counter = 0
    for collector_str in collectors_meta.keys():
        if globals().get(collector_str):
            collect_class = globals()[collector_str]
            metrics_to_collect = collectors_meta[collector_str]["metrics"]
            metrics_to_encrypt = collectors_meta[collector_str]["metrics_to_encrypt"]
            table = collectors_meta[collector_str]["table"]
            collector = collect_class(logger, computer_collector.machine_id, metrics_to_collect, metrics_to_encrypt,
                                      datetime_format, table)
            collectors.append(collector)
            to_collect.append(True)
        else:
            logger.warning("Collector " + metrics_to_collect + " can not be found.")
            to_collect.append(False)
    collectors.append(computer_collector)
    if True not in to_collect:
        logger.error("No collector found. Exit. Please ensure metrics collector code exist.")
    else:
        while True:
            db_connector = MYSQLConnector(settings["database"])
            key_file = os.path.dirname(os.path.abspath(__file__)) + "\\" + settings["encryption_key_file"]
            if os.path.exists(key_file):
                logger.info("Encryption key file is found")
                transaction = None
                try:
                    logger.info("Begin fetching computer metrics data and encrypting the data")
                    for collector in collectors:
                        collector.fetch_metrics()
                        encrypt_data(collector, key_file)
                    encrypt_data(computer_collector, key_file)
                    logger.info("End fetching computer metrics data and encrypting the data")

                    logger.info("Begin persisting fetch metrics")
                    logger.debug("To store metrics on local " + str(settings["to_store_local"]))
                    if settings["to_store_local"]:
                        csv_name = settings["local_store_dir"] + type(computer_collector).__name__ + ".csv"
                        store_local(computer_collector, csv_name)
                        for collector in collectors:
                            logger.info("Begin storing " + type(collector).__name__)
                            csv_name = settings["local_store_dir"] + type(collector).__name__ + ".csv"
                            store_local(collector, csv_name)
                            logger.info("End storing " + type(collector).__name__)
                    else:
                        db_engine = db_connector.get_engine()
                        with db_engine.connect() as conn:
                            logger.debug("Store on to host " + db_connector.host + " into database " + db_connector.db_name)
                            conn.auto_commit = False
                            transaction = conn.begin()
                            store_to_database(computer_collector, conn)
                            for collector in collectors:
                                logger.info("Begin store " + type(collector).__name__)
                                store_to_database(collector, conn)
                                transaction.commit()
                except AccessDenied as ad:
                    logger.error("Access denied to fetch information for {}".format(str(collector)))
                    logger.error(ad)
                    if transaction is not None:
                        transaction.rollback()
                except FileNotFoundError as fnfe:
                    logger.error("Dependent file not found.")
                    logger.error(fnfe)
                except Exception as e:
                    if transaction is not None:
                        transaction.rollback()
                    logger.error(e.args[0])
                finally:
                    if is_test:
                        break
                    counter = counter + 1
                    print("Finish " + str(counter))
                    sleep(settings.get("sleep_time_sec"))
            else:
                logger.error("Encryption key file is not found")
                logger.error(key_file)