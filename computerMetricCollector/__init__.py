import argparse
import os
from time import sleep
from computerMetricCollector.CollectoUtils import get_logger, init_collector, collect_metrics
from computerMetricCollector.metricsCollector.computerMetrics import ComputerMetrics
from computerMetricCollector.config import import_config
from computerMetricCollector.crypto import read_key

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
    settings = import_config(root_dir)
    if len(settings.keys()) == 0:
        exit(1)
    log_file = root_dir + "\\log\\" + settings.get("log_file")
    logger = get_logger(log_file, settings.get("log_level"), settings.get("log_rotate_time"),
                        settings.get("log_backup_cnt"))
    logger.info("Create logger instance")
    logger.debug("Testing mode: " + str(is_test))
    logger.info("Extract metadata from configuration to start collecting metrics")
    collectors_meta = settings.get("collectors")
    datetime_format = settings.get("date_time_format")
    logger.info("Start collecting system information")
    collectors = []
    to_collect = []
    # Collect computer metrics separate since it is called different and require to call first
    com_metrics_to_collect = collectors_meta["ComputerMetrics"]["metrics"]
    com_metrics_to_encrypt = collectors_meta["ComputerMetrics"]["metrics_to_encrypt"]
    com_url = collectors_meta["ComputerMetrics"]["url"]
    computer_collector = ComputerMetrics(logger, com_metrics_to_collect, com_metrics_to_encrypt, datetime_format, com_url)
    computer_collector.fetch_metrics()
    # Computer Metrics does not need to be fetch again
    del collectors_meta["ComputerMetrics"]
    logger.info("Start instantiate collector for hardware and running process")
    for collector_str in collectors_meta.keys():
        collector = init_collector(logger, collectors_meta, collector_str, computer_collector.machine_id,
                                   datetime_format)
        if collector is not None:
            to_collect.append(True)
            collectors.append(collector)
    if True not in to_collect:
        logger.error("No collector found. Please ensure metrics collector code exist.")
        exit(1)
    else:
        collected_counter = 0
        while True:
            print("Start collection " + str(collected_counter))
            key_file = os.path.dirname(os.path.abspath(__file__)) + "\\" + settings["encryption_key_file"]
            if os.path.exists(key_file):
                encryption_key = read_key(key_file)
                logger.info("Encryption key file is found")
                collect_metrics(logger, settings, encryption_key, collectors, computer_collector)
                for c in collectors:
                    c.reset_metrics_df()
                print("Finish collection " + str(collected_counter))
                collected_counter = collected_counter + 1
                sleep(settings.get("sleep_time_sec"))
                if is_test:
                    logger.info("Test run finish. The program will terminate")
                    exit(0)
            else:
                logger.error("Encryption key file is not found. Please follow readme to extract encryption key and " +
                             "instruction to import to the collector.")
                logger.error(key_file)
                exit(1)
