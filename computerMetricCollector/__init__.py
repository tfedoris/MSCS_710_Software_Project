import argparse
import os
from time import sleep
from computerMetricCollector.CollectoUtils import (
    get_logger, init_collector, collect_metrics, create_computer_collector
)
from computerMetricCollector.config import import_config
from computerMetricCollector.crypto import get_key
from computerMetricCollector.test import read_key

if __name__ == "__main__":
    # Defines arguments to be passed in when running the program
    parser = argparse.ArgumentParser(description="Initiate Collector to collect metrics")
    parser.add_argument("-t", "--test", required=False,
                        help="Boolean value to enable collector to run in test mode",
                        default=False)
    args = parser.parse_args()
    is_test = args.test

    # Set path to load settings
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
    computer_collector = create_computer_collector(logger, collectors_meta, datetime_format)
    collectors.append(computer_collector)
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
            encryption_key = get_key(settings.get("registration_id"), settings.get("public_key_url"))

            if encryption_key is not None:
                logger.info("Encryption key file is found")
                collect_metrics(logger, settings, encryption_key, collectors)
                for c in collectors:
                    c.reset_metrics_df()
                print("Finish collection " + str(collected_counter))
                collected_counter = collected_counter + 1
                sleep(settings.get("sleep_time_sec"))
                if is_test:
                    logger.info("Test run finish. The program will terminate")
                    exit(0)
            else:
                logger.error("Fail to fetch public key with registration id " + settings.get("registration_id"))
                logger.error("Please provide correct registration id.")
                exit(1)
            # Reload settings for the next run
            settings = import_config(root_dir)
