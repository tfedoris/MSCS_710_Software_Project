CREATE DATABASE IF NOT EXISTS warproject
/*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE warproject;

DROP TABLE IF EXISTS map_user_machine;
DROP TABLE IF EXISTS cpu_metrics;
DROP TABLE IF EXISTS disk_metrics;
DROP TABLE IF EXISTS disk_io_metrics;
DROP TABLE IF EXISTS memory_metrics;
DROP TABLE IF EXISTS network_metrics;
DROP TABLE IF EXISTS processes_metrics;
DROP TABLE IF EXISTS client_machine;

CREATE TABLE client_machine (
	machine_id VARCHAR(40)
    , entry_time DATETIME
    , machine_name VARBINARY(128)
    , system_name VARBINARY(32)
    , version VARBINARY(32)
    , machine_type VARBINARY(16)
    , nounce VARBINARY(36)
    , session_key VARBINARY(512)
    , primary key (machine_id)
);

CREATE TABLE cpu_metrics (
	machine_id VARCHAR(40)
    , entry_time DATETIME
    , brand VARBINARY(128)
    , vendor VARBINARY(64)
    , architecture VARBINARY(36)
    , bits VARBINARY(4)
    , hz_advertise VARBINARY(32)
    , hz_actual VARBINARY(32)
    , core_count VARBINARY(4)
    , nonce VARBINARY(36)
    , session_key VARBINARY(512)
    , primary key (machine_id, brand)
);

CREATE TABLE disk_metrics(
	machine_id VARCHAR(40)
    , entry_time DATETIME
	, disk_name VARBINARY(16)
	, total_bytes VARBINARY(32)
	, free_bytes VARBINARY(32)
	, used_bytes VARBINARY(32)
	, percent VARBINARY(16)
    , nonce VARBINARY(36)
    , session_key VARBINARY(512)
    , primary key (machine_id, nonce)
);

CREATE TABLE disk_io_metrics (
	machine_id VARCHAR(40)
    , entry_time DATETIME
    , disk_name VARBINARY(16)
    , count_read VARBINARY(16)
    , count_write VARBINARY(16)
    , bytes_read VARBINARY(192)
    , bytes_write VARBINARY(192)
    , time_read_in_milli VARBINARY(8)
    , time_write_in_milli VARBINARY(8)
    , nonce VARBINARY(36)
    , session_key VARBINARY(512)
    , primary key (machine_id, nonce)
);

CREATE TABLE memory_metrics(
	machine_id VARCHAR(40)
    , entry_time DATETIME
	, memory_total VARBINARY (32)
	, memory_available VARBINARY (32)
	, memory_used VARBINARY (32)
	, memory_user_percent VARBINARY (16)
	, swap_total VARBINARY (32)
	, swap_free VARBINARY (32)
	, swap_used VARBINARY (32)
	, swap_percent VARBINARY (16)
	, swap_byte_int VARBINARY (8)
	, swap_byte_out VARBINARY (8)
    , nonce VARBINARY(36)
    , session_key VARBINARY(512)
    , primary key (machine_id, nonce)
);

CREATE TABLE network_metrics (
	machine_id VARCHAR(40)
    , entry_time DATETIME
	, network_interface VARBINARY(256)
	, bytes_send VARBINARY(24)
	, bytes_receive VARBINARY(24)
	, error_bytes_receive VARBINARY(24)
	, error_bytes_send VARBINARY(24)
	, packet_sent VARBINARY(16)
	, packet_receive VARBINARY(16)
	, packet_receive_drop VARBINARY(12)
	, packet_send_drop VARBINARY(12)
    , nonce VARBINARY(36)
    , session_key VARBINARY(512)
    , primary key (machine_id, nonce)
);

CREATE TABLE processes_metrics (
	machine_id VARCHAR(40)
    , entry_time DATETIME
	, pid VARBINARY(16)
	, name VARBINARY(256)
	, start_time VARBINARY(48)
	, start_user VARBINARY(384)
	, status VARBINARY(24)
	, cpu_user_time VARBINARY(48)
	, cpu_kernel_time VARBINARY(48)
	, cpu_percent VARBINARY(16)
	, memory_percent_used_byte VARBINARY(64)
	, memory_physical_used_byte VARBINARY(28)
	, memory_virtual_bsed_byte VARBINARY(28)
	, memory_unique_used_byte VARBINARY(28)
	, memory_page_fault VARBINARY(24)
	, io_read_count VARBINARY(24)
	, io_read_bytes VARBINARY(28)
	, io_write_count VARBINARY(24)
	, io_write_bytes VARBINARY(28)
	, thread_num VARBINARY(8)
    , nonce VARBINARY(36)
    , session_key VARBINARY(512)
    , primary key (machine_id, nonce)
);

CREATE TABLE map_user_machine (
  user_id varchar(40) NOT NULL
  , machine_id varchar(40) NOT NULL
  , last_update_time datetime DEFAULT NULL
  , PRIMARY KEY (user_id,machine_id)
  , CONSTRAINT map_user_uid FOREIGN KEY (user_id) REFERENCES `user` (user_id)
  , CONSTRAINT map_user_machine_id FOREIGN KEY (machine_id) REFERENCES client_machine (machine_id)
);