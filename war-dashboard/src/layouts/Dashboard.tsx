import DataFilter from "components/atoms/DataFilter";
import React, { ReactElement } from "react";
import { useStyles } from "themes/DynamicDrawerTheme";

interface Props {
  registrationId: string;
}

export default function Dashboard(props: Props): ReactElement {
  const classes = useStyles();
  return (
    <div className={classes.drawerHeader}>
      <DataFilter />
    </div>
  );
}
