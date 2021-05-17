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
    , nonce VARBINARY(36)
    , session_key VARBINARY(1024)
    , primary key (machine_id)
);

CREATE TABLE cpu_metrics (
	machine_id VARCHAR(40)
    , entry_time DATETIME
    , brand VARBINARY(128)
    , vendor VARBINARY(64)
    , architecture VARBINARY(36)
    , bits VARBINARY(4)
    , hz_advertise BIGINT
    , hz_actual BIGINT
    , core_count SMALLINT
    , nonce VARBINARY(36)
    , session_key VARBINARY(1024)
    , primary key (machine_id)
);

CREATE TABLE disk_metrics(
	machine_id VARCHAR(40)
    , entry_time DATETIME
	, disk_name VARBINARY(16)
	, total_bytes BIGINT
	, free_bytes BIGINT
	, used_bytes BIGINT
	, percent DOUBLE
    , nonce VARBINARY(36)
    , session_key VARBINARY(1024)
    , primary key (machine_id, nonce)
);

CREATE TABLE disk_io_metrics (
	machine_id VARCHAR(40)
    , entry_time DATETIME
    , disk_name VARBINARY(16)
    , count_read INTEGER
    , count_write INTEGER
    , bytes_read BIGINT
    , bytes_write BIGINT
    , time_read_in_milli INTEGER
    , time_write_in_milli INTEGER
    , nonce VARBINARY(36)
    , session_key VARBINARY(1024)
    , primary key (machine_id, nonce)
);

CREATE TABLE memory_metrics(
	machine_id VARCHAR(40)
    , entry_time DATETIME
	, memory_total BIGINT
	, memory_available BIGINT
	, memory_used BIGINT
	, memory_user_percent FLOAT
	, swap_total BIGINT
	, swap_free BIGINT
	, swap_used BIGINT
	, swap_percent FLOAT
	, swap_byte_in BIGINT
	, swap_byte_out BIGINT
    , nonce VARBINARY(36)
    , session_key VARBINARY(1024)
    , primary key (machine_id, nonce)
);

CREATE TABLE network_metrics (
	machine_id VARCHAR(40)
    , entry_time DATETIME
	, network_interface VARBINARY(256)
	, bytes_send BIGINT
	, bytes_receive BIGINT
	, error_bytes_receive BIGINT
	, error_bytes_send BIGINT
	, packet_sent INTEGER
	, packet_receive INTEGER
	, packet_receive_drop INTEGER
	, packet_send_drop INTEGER
    , nonce VARBINARY(36)
    , session_key VARBINARY(1024)
    , primary key (machine_id, nonce)
);

CREATE TABLE processes_metrics (
	machine_id VARCHAR(40)
    , entry_time DATETIME
	, pid VARBINARY(16)
	, name VARBINARY(256)
	, start_time VARBINARY(48)
	, start_user VARBINARY(384)
	, process_status VARCHAR(16)
	, cpu_user_time VARBINARY(48)
	, cpu_kernel_time VARBINARY(48)
	, cpu_percent VARBINARY(16)
	, memory_percent_used_byte BIGINT
	, memory_physical_used_byte BIGINT
	, memory_virtual_bsed_byte BIGINT
	, memory_unique_used_byte BIGINT
	, memory_page_fault VARBINARY(24)
	, io_read_count VARBINARY(24)
	, io_read_bytes BIGINT
	, io_write_count VARBINARY(24)
	, io_write_bytes BIGINT
	, thread_num VARBINARY(8)
    , nonce VARBINARY(36)
    , session_key VARBINARY(1024)
    , primary key (machine_id, nonce)
);

CREATE TABLE map_user_machine (
  user_id varchar(40) NOT NULL
  , machine_id varchar(40) NOT NULL
  , last_update_time datetime DEFAULT NULL
  , PRIMARY KEY (user_id, machine_id)
);