import DataFilter from "components/atoms/DataFilter";
import MachineSelector from "components/atoms/MachineSelector";
import React, { ReactElement } from "react";
import { useStyles } from "themes/DynamicDrawerTheme";
import SyncIcon from "@material-ui/icons/Sync";
import { IconButton } from "@material-ui/core";
import { Tooltip } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import { Endpoint } from "utilities/API";
import RefreshButton from "components/atoms/RefreshButton";
import moment from "moment";
import CPUMetricsPieChart from "components/organisms/CPUMetricsPieChart";
import MemoryMetricsPieChart from "components/organisms/MemoryMetricsPieChart";
import ProcessesMetricsTable from "components/organisms/ProcessesMetricsTable";

const KB = 0.001;
const MB = 1e-6;

interface Props {
  registrationId: string;
}

export default function Dashboard(props: Props): ReactElement {
  const classes = useStyles();

  const [selectedMachineId, setSelectedMachineId] = React.useState("");
  const [refresh, toggleRefresh] = React.useState(false);

  const [machineInfo, setMachineInfo] = React.useState({} as any);
  const [cpuMetrics, setCpuMetrics] = React.useState([] as any);
  const [memoryMetrics, setMemoryMetrics] = React.useState([] as any);
  const [processesData, setProcessesData] = React.useState([] as any);
  const [filteredProcessesData, setFilteredProcessesData] = React.useState(
    [] as any
  );

  const [selectedTimeframe, setSelectedTimeframe] = React.useState({
    start: moment().format(),
    end: moment().format(),
  });

  const handleTimeframeChange = (timeframe: any) => {
    setSelectedTimeframe(timeframe);
  };

  React.useEffect(() => {
    var isCancelled = false;

    const fetchData = async () => {
      const machineInfoRequest = axios.post(Endpoint.MachineInfo, {
        registration_id: props.registrationId,
        machine_id: selectedMachineId,
      });
      const cpuMetricsRequest = axios.post(Endpoint.CPUUtilization, {
        registration_id: props.registrationId,
        machine_id: selectedMachineId,
      });
      const memoryMetricsRequest = axios.post(Endpoint.MemoryUtilization, {
        registration_id: props.registrationId,
        machine_id: selectedMachineId,
      });
      const processesDataRequest = axios.post(Endpoint.ProcessesData, {
        registration_id: props.registrationId,
        machine_id: selectedMachineId,
      });

      await axios
        .all([
          machineInfoRequest,
          cpuMetricsRequest,
          memoryMetricsRequest,
          processesDataRequest,
        ])
        .then(
          axios.spread(function (
            machineInfoResponse,
            cpuMetricsResponse,
            memoryMetricsResponse,
            processesDataResponse
          ) {
            if (!isCancelled) {
              setMachineInfo(machineInfoResponse.data.data[0] || {});
              setCpuMetrics(cpuMetricsResponse.data.data || []);
              console.log("CPU Metrics: ", cpuMetricsResponse.data.data);
              setMemoryMetrics(memoryMetricsResponse.data.data || []);
              setProcessesData(processesDataResponse.data.data);
            }
          })
        );
    };

    if (props.registrationId !== "[LOADING...]" && selectedMachineId !== "") {
      fetchData();
    }

    return () => {
      isCancelled = true;
      return;
    };
  }, [props.registrationId, selectedMachineId]);

  React.useEffect(() => {
    const filtered = processesData.filter((data: any) => {
      return moment(data.entry_time).isBetween(
        selectedTimeframe.start,
        selectedTimeframe.end
      );
    });
    console.log(filtered);

    const summed = Object.values(
      filtered.reduce((a: any, curr: any) => {
        if (!a[curr.name]) a[curr.name] = Object.assign({}, curr);
        else {
          a[curr.name].cpu_percent += curr.cpu_percent;
          a[curr.name].memory_physical_used_byte +=
            curr.memory_physical_used_byte;
          a[curr.name].memory_virtual_bsed_byte +=
            curr.memory_virtual_bsed_byte;
          a[curr.name].io_read_count += curr.io_read_count;
          a[curr.name].io_read_bytes += curr.io_read_bytes;
          a[curr.name].io_write_count += curr.io_write_count;
          a[curr.name].io_write_bytes += curr.io_write_bytes;
          a[curr.name].thread_num += curr.thread_num;
        }
        return a;
      }, {})
    );
    console.log(summed);

    console.log(machineInfo);

    const averaged = summed.map((entry: any) => {
      var averagedObj = Object.assign({}, entry);
      const count = filtered.filter(
        (obj: any) => obj.name === entry.name
      ).length;
      averagedObj.cpu_percent =
        entry.cpu_percent / count / machineInfo.core_count;
      console.log(machineInfo.core_count);
      averagedObj.memory_physical_used_byte =
        (entry.memory_physical_used_byte / count) * MB;
      averagedObj.memory_virtual_bsed_byte =
        (entry.memory_virtual_bsed_byte / count) * MB;
      averagedObj.io_read_count = entry.io_read_count / count;
      averagedObj.io_read_bytes = (entry.io_read_bytes / count) * MB;
      averagedObj.io_write_count = entry.io_write_count / count;
      averagedObj.io_write_bytes = (entry.io_write_bytes / count) * MB;
      averagedObj.thread_num = entry.thread_num / count;
      return averagedObj;
    });
    console.log("Averaged: ", averaged);

    setFilteredProcessesData(averaged);
  }, [processesData, selectedTimeframe, machineInfo]);

  return (
    <>
      <div className={classes.drawerHeader}>
        <DataFilter refresh={refresh} onChange={handleTimeframeChange} />
        <MachineSelector
          registrationId={props.registrationId}
          onChange={(value: string) => {
            setSelectedMachineId(value);
          }}
        />
        <RefreshButton onToggleRefresh={() => toggleRefresh(!refresh)} />
      </div>
      <div>
        <div style={{ height: 400 }}>
          <CPUMetricsPieChart data={filteredProcessesData} />
        </div>
        <div style={{ height: 400 }}>
          <MemoryMetricsPieChart data={filteredProcessesData} />
        </div>
      </div>
      <div>
        <ProcessesMetricsTable rows={filteredProcessesData} />
      </div>
    </>
  );
}
