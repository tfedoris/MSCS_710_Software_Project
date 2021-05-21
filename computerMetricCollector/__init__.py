import argparse
import multiprocessing
import os
import sys
from time import sleep
from datetime import datetime, timedelta
from computerMetricCollector.CollectorUtils import (
    get_logger, init_collector, collect_metrics, create_computer_collector
)
from computerMetricCollector.config import import_config
from computerMetricCollector.crypto import get_key


if __name__ == "__main__":
    print("Start Computer Metric Collector.")
    # Set path to load settings
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        root_dir = os.path.dirname(os.path.dirname(sys.executable))
        multiprocessing.freeze_support()
    else:
        root_dir = os.path.dirname(os.path.abspath(__file__))

    # Defines arguments to be passed in when running the program
    parser = argparse.ArgumentParser(description="Initiate Collector to collect metrics")
    parser.add_argument("-t", "--test", required=False,
                        help="Boolean value to enable collector to run in test mode",
                        default=False)
    parser.add_argument("-rid", "--registration_id", required=False,
                        help="String value represent registration id of the user. If not pass as arguement the " +
                             "program will ask for it.",
                        default=None)
    parser.add_argument("-l", "--local_store", required=False,
                        help="Boolean value to determine whether or not to store the performance data locally",
                        default=None)
    args = parser.parse_args()
    is_testing = args.test
    reg_id = args.registration_id
    is_local_store = args.local_store

    settings = import_config(root_dir)
    # If not settings is provide
    if len(settings.keys()) == 0:
        sys.exit(1)

    if reg_id is None:
        reg_id = input("Input your registration ID: ")
    settings["registration_id"] = reg_id
    if is_local_store is None:
        is_local_store = input("Store metrics locally as well (enter \"True\" or \"False\"): ")
    if is_local_store.lower() == "true":
        is_local_store = True
    else:
        is_local_store = False
    settings["to_store_local"] = is_local_store

    log_file = root_dir + "\\log\\" + settings.get("log_file")
    logger = get_logger(log_file, settings.get("log_level"), settings.get("log_rotate_time"),
                        settings.get("log_backup_cnt"))
    logger.debug("Root directory: " + root_dir)
    logger.info("Create logger instance")
    logger.debug("Testing mode: " + str(is_testing))
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
        sys.exit(1)
    else:
        collected_counter = 1
        encryption_key = get_key(logger, settings.get("registration_id"), settings.get("public_key_url"))
        while True:
            print("Start collection " + str(collected_counter))
            logger.info("Start collection " + str(collected_counter))

            if encryption_key is not None:
                logger.info("Encryption key file is found")
                collect_metrics(logger, settings, encryption_key, collectors)
                print("Finish collection " + str(collected_counter))
                logger.info("Finish collection " + str(collected_counter))
                collected_counter = collected_counter + 1

                if is_testing:
                    logger.info("Test run finish. The program will terminate")
                    sys.exit(0)

                logger.debug("Begin sleeping for " + str(settings.get("sleep_time_sec")) + " second(s)")
                next_collect_time = datetime.now() + timedelta(seconds=settings.get("sleep_time_sec"))
                print("Next collection time " + next_collect_time.strftime(datetime_format))
                sleep(settings.get("sleep_time_sec"))
            else:
                logger.error("Fail to fetch public key with registration id " + settings.get("registration_id"))
                logger.error("Please provide correct registration id.")
                sys.exit(1)
            # Reload settings for the next run
            logger.info("Reload settings")
            settings = import_config(root_dir)
            settings["registration_id"] = reg_id
            settings["to_store_local"] = is_local_store
