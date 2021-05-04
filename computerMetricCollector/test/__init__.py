import os
from Cryptodome.PublicKey import RSA
from computerMetricCollector.CollectoUtils import get_logger, init_collector, persist_local, persist_database
from computerMetricCollector.config import import_config
from computerMetricCollector.dataCrypto import encrypt_data

if __name__ == "__main__":
    # Test logger
    log_file = "Test.log"
    log_level = "ERROR"
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
        "NetworkMetrics": {
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
    }
    logger.info("Start testing encryption")
    bits = 2048
    key = RSA.generate(bits)
    # Randomly create public private key to be store as csv to ensure reading of encryption key is not a problem.
    encrypt_key = key.publickey().export_key()
    decrypt_key = key.export_key()
    dir_name = os.path.dirname(os.path.dirname(__file__))
    with open(dir_name + "/dataCrypto/ppk/public.pem", "bw+") as public_file:
        public_file.write(encrypt_key)
    with open(dir_name + "/dataCrypto/ppk/public.pem", "r") as public_file:
        encrypt_key = public_file.read()
    with open(dir_name + "/dataCrypto/ppk/private.pem", "bw+") as private_file:
        private_file.write(decrypt_key)
    with open(dir_name + "/dataCrypto/ppk/private.pem", "r") as private_file:
        decrypt_key = private_file.read()

    collector_str = "NetworkMetrics"
    machine_id = "11111111-2222-3333-4444-555555555555"
    datetime_format = "%Y-%m-%d %H:%M:%S"
    logger.debug("Test encryption with " + str(bits) + " bits key")
    logger.debug("Test encryption with public key " + str(bits) + " bits key")
    collector = init_collector(logger, collectors_meta, collector_str, machine_id, datetime_format)
    collector.fetch_metrics()
    encrypt_data(collector, encrypt_key)

    # Test persisting collector data locally
    abs_path = os.path.abspath(__file__)
    root_dir = os.path.dirname(os.path.dirname(abs_path))
    settings = import_config(root_dir)
    persist_local(logger, settings["local_store_dir"], collector)

    # Test persisting collector data to the database
    persist_database(logger, settings["store_remote"], [collector])
