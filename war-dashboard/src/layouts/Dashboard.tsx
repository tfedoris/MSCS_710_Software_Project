import DataFilter from "components/atoms/DataFilter";
import MachineSelector from "components/atoms/MachineSelector";
import React, { ReactElement } from "react";
import { useStyles } from "themes/DynamicDrawerTheme";
import SyncIcon from "@material-ui/icons/Sync";
import { Grid, IconButton, Slide, Typography } from "@material-ui/core";
import { Tooltip } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import { Endpoint } from "utilities/API";
import RefreshButton from "components/atoms/RefreshButton";
import moment from "moment";
import CPUMetricsPieChart from "components/organisms/CPUMetricsPieChart";
import MemoryMetricsPieChart from "components/organisms/MemoryMetricsPieChart";
import ProcessesMetricsTable from "components/organisms/ProcessesMetricsTable";
import { Fade } from "@material-ui/core";

const KB = 0.001;
const MB = 1e-6;

interface Props {
  user_id: string;
}

export default function Dashboard(props: Props): ReactElement {
  const classes = useStyles();

  const [selectedMachineId, setSelectedMachineId] = React.useState("");
  const [refresh, toggleRefresh] = React.useState(false);

  const [machineInfo, setMachineInfo] = React.useState({} as any);
  const [processesData, setProcessesData] = React.useState([] as any);
  const [filteredProcessesData, setFilteredProcessesData] = React.useState(
    [] as any
  );

  const [selectedTimeframe, setSelectedTimeframe] = React.useState({
    start: moment().format("YYYY-MM-DDTHH:mm:ss"),
    end: moment().format("YYYY-MM-DDTHH:mm:ss"),
  });

  React.useEffect(() => {
    console.log("Timeframe: ", selectedTimeframe);
  }, [selectedTimeframe]);

  const handleTimeframeChange = (timeframe: any) => {
    setSelectedTimeframe(timeframe);
  };

  React.useEffect(() => {
    var isCancelled = false;

    const fetchData = async () => {
      const machineInfoRequest = axios.post(Endpoint.MachineInfo, {
        user_id: props.user_id,
        machine_id: selectedMachineId,
      });
      const processesDataRequest = axios.post(Endpoint.ProcessesData, {
        user_id: props.user_id,
        machine_id: selectedMachineId,
      });
      await axios.all([machineInfoRequest, processesDataRequest]).then(
        axios.spread(function (machineInfoResponse, processesDataResponse) {
          if (!isCancelled) {
            setMachineInfo(machineInfoResponse.data.data[0] || {});
            setProcessesData(processesDataResponse.data.data);
          }
        })
      );
    };

    if (props.user_id && selectedMachineId !== "") {
      fetchData();
    }

    return () => {
      isCancelled = true;
      return;
    };
  }, [props.user_id, selectedMachineId]);

  React.useEffect(() => {
    if (!processesData) return;
    const filtered = processesData?.filter((data: any) => {
      const date = moment(data.entry_time).utc().format("YYYY-MM-DDTHH:mm:ss");
      console.log(
        `${selectedTimeframe.start} <= ${date} <= ${
          selectedTimeframe.end
        }: ${moment(date).isBetween(
          selectedTimeframe.start,
          selectedTimeframe.end
        )}`
      );
      return moment(date).isBetween(
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
        <Grid container spacing={3}>
          <Grid item xs={12} lg={6}>
            <MachineSelector
              userId={props.user_id}
              onChange={(value: string) => {
                setSelectedMachineId(value);
              }}
            />
          </Grid>
          <Grid item xs={10} lg={5}>
            <DataFilter refresh={refresh} onChange={handleTimeframeChange} />
          </Grid>
          <Grid item xs={2} lg={1}>
            <RefreshButton onToggleRefresh={() => toggleRefresh(!refresh)} />
          </Grid>
          <Slide
            direction="right"
            in={filteredProcessesData.length > 0}
            mountOnEnter
            unmountOnExit
          >
            <Grid item xs={12} lg={6}>
              <div style={{ paddingBottom: 10 }}>
                <Typography variant="h5">CPU Utilization</Typography>
              </div>
              <div style={{ height: 400 }}>
                <CPUMetricsPieChart data={filteredProcessesData} />
              </div>
            </Grid>
          </Slide>
          <Slide
            direction="left"
            in={filteredProcessesData.length > 0}
            mountOnEnter
            unmountOnExit
          >
            <Grid item xs={12} lg={6}>
              <div style={{ paddingBottom: 10 }}>
                <Typography variant="h5">Memory Utilization</Typography>
              </div>
              <div style={{ height: 400 }}>
                <MemoryMetricsPieChart data={filteredProcessesData} />
              </div>
            </Grid>
          </Slide>
          <Slide
            direction="up"
            in={filteredProcessesData.length > 0}
            mountOnEnter
            unmountOnExit
          >
            <Grid item lg={12}>
              <ProcessesMetricsTable rows={filteredProcessesData} />
            </Grid>
          </Slide>
        </Grid>
      </div>
    </>
  );
}
