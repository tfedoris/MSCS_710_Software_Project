import os
from Cryptodome.PublicKey import RSA
from computerMetricCollector.InitiateCollectors import get_logger, init_collector, persist_local, persist_database
from computerMetricCollector.config import import_config
from computerMetricCollector.dataCrypto import encrypt_data

if __name__ == "__main__":
    # Test logger
    log_file = "Test.log"
    log_level = "Error"
    rotate_time = "midnight"
    backup_cnt = 10
    logger = get_logger(log_file, log_level, rotate_time, backup_cnt)
    logger.debug("Test debug message")
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")
    logger.fatal("Test fatal message")

    # Test creating collectors to collect metrics
    collectors_meta = {
      "table": "",
      "metrics_to_encrypt": [
        "NetworkInterface",
        "ByteSend",
        "ByteReceived",
        "ErrorByteReceived",
        "ErrorByteSend",
        "PacketSend",
        "PacketReceived",
        "PacketReceivedDrop",
        "PacketSendDrop"
      ],
      "metrics": [
        "MachineId",
        "EntryDatetime",
        "NetworkInterface",
        "ByteSend",
        "ByteReceived",
        "ErrorByteReceived",
        "ErrorByteSend",
        "PacketSend",
        "PacketReceived",
        "PacketReceivedDrop",
        "PacketSendDrop",
        "Nonce",
        "SessionKey"
      ]
    }
    bits = 2048
    key = RSA.generate(bits)
    encrypt_key = key.publickey().export_key()
    decrypt_key = key.export_key()
    collector_str = "NetworkMetrics"
    machine_id = "11111111-2222-3333-4444-555555555555"
    datetime_format = "%Y-%m-%d %H:%M:%S"
    collector = init_collector(logger, collectors_meta, collector_str, machine_id, datetime_format)
    collector.fetch_metrics()
    encrypt_data(collector, encrypt_key)

    # Test persisting collector data locally
    abs_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(os.path.dirname(abs_path))
    settings = import_config(root_dir)
    persist_local(logger, settings["local_store_dir"], collector)

    # Test persisting collector data to the database
    persist_database(logger, settings["database"], [collector])
