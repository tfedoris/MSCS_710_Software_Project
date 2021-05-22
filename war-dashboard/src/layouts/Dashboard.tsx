import DataFilter from "components/atoms/DataFilter";
import MachineSelector from "components/atoms/MachineSelector";
import React, { ReactElement } from "react";
import { useStyles } from "themes/DynamicDrawerTheme";
import SyncIcon from "@material-ui/icons/Sync";
import { IconButton } from "@material-ui/core";
import { Tooltip } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

interface Props {
  registrationId: string;
}

const iconButtonStyles = makeStyles((theme) => ({
  default: {
    transform: "scaleX(1)",
  },
  rotated: {
    transform: "scaleX(-1)",
  },
}));

export default function Dashboard(props: Props): ReactElement {
  const classes = useStyles();
  const iconButtonClasses = iconButtonStyles();

  const [selectedMachineId, setSelectedMachineId] = React.useState("");
  const [refresh, toggleRefresh] = React.useState(false);
  const [rotate, toggleRotate] = React.useState(false);

  const handleTimeframeChange = (timeframe: Object) => {
    console.log(timeframe);
  };

  return (
    <div className={classes.drawerHeader}>
      <DataFilter refresh={refresh} onChange={handleTimeframeChange} />
      <MachineSelector
        registrationId={props.registrationId}
        onChange={(value: string) => {
          setSelectedMachineId(value);
        }}
      />
      <Tooltip title="Refresh Data">
        <IconButton
          onMouseDown={() => toggleRotate(!rotate)}
          onMouseUp={() => {
            toggleRotate(!rotate);
            toggleRefresh(!refresh);
          }}
        >
          <SyncIcon
            className={
              rotate ? iconButtonClasses.rotated : iconButtonClasses.default
            }
          />
        </IconButton>
      </Tooltip>
    </div>
  );
}
