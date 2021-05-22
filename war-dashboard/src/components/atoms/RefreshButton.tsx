import { IconButton, Tooltip } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import SyncIcon from "@material-ui/icons/Sync";
import React, { ReactElement } from "react";

interface Props {
  onToggleRefresh: () => void;
}

const iconButtonStyles = makeStyles((theme) => ({
  default: {
    transform: "scaleX(1)",
  },
  rotated: {
    transform: "scaleX(-1)",
  },
}));

export default function RefreshButton({
  onToggleRefresh,
}: Props): ReactElement {
  const iconButtonClasses = iconButtonStyles();
  const [rotate, toggleRotate] = React.useState(false);
  return (
    <Tooltip title="Refresh">
      <IconButton
        onMouseDown={() => toggleRotate(!rotate)}
        onMouseUp={() => {
          toggleRotate(!rotate);
          onToggleRefresh();
        }}
      >
        <SyncIcon
          className={
            rotate ? iconButtonClasses.rotated : iconButtonClasses.default
          }
          fontSize="large"
        />
      </IconButton>
    </Tooltip>
  );
}
