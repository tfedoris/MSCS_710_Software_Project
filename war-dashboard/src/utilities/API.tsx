export enum Endpoint {
  MachineInfo = "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-user-machine-info",
  CPUUtilization = "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-user-cpu-utilization",
  MemoryUtilization = "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-user-memory-utilization",
  ProcessesData = "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-data-for-processes-table",
  ClientMachines = "https://ytp3g6j58c.execute-api.us-east-2.amazonaws.com/test/get-client-machines",
}

export interface ProcessesData {
  entry_time: Date;
  pid: number;
  name: string;
  process_status: string;
  cpu_percent: number;
  memory_physical_used_byte: number;
  memory_virtual_bsed_byte: number;
  io_read_count: number;
  io_read_bytes: number;
  io_write_count: number;
  io_write_bytes: number;
  thread_num: number;
}

export interface MachineInfo {
  entry_time: Date;
  machine_name: string;
  system_name: string;
  version: string;
  machine_type: string;
  brand: string;
  hz_actual: number;
  core_count: number;
  memory_total: number;
}

export interface CPUUtilization {
  entry_time: Date;
  name: string;
  cpu_percent: number;
}

export interface MemoryUtilization {
  entry_time: Date;
  name: string;
  memory_physical_used_byte: number;
}
