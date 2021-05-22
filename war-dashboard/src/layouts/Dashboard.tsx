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

interface Props {
  registrationId: string;
}

export default function Dashboard(props: Props): ReactElement {
  const classes = useStyles();

  const [selectedMachineId, setSelectedMachineId] = React.useState("");
  const [refresh, toggleRefresh] = React.useState(false);

  const [processesData, setProcessesData] = React.useState([] as any);

  const handleTimeframeChange = (timeframe: Object) => {
    console.log(timeframe);
  };

  React.useEffect(() => {
    const fetchData = async () => {
      const processesDataRequest = axios.post(Endpoint.ProcessesData, {
        registration_id: props.registrationId,
        machine_id: selectedMachineId,
      });

      await axios.all([processesDataRequest]).then(
        axios.spread(function (processesDataResponse) {
          console.log(processesDataResponse.data.data);
        })
      );
    };

    if (props.registrationId !== "[LOADING...]" && selectedMachineId !== "") {
      fetchData();
    }
  }, [props.registrationId, selectedMachineId]);

  return (
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
  );
}
